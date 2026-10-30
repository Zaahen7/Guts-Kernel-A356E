#!/usr/bin/env python3
"""Extract the FinaSU manager signing certificate and inject it into Kbuild.

Flow:
  1. Pick the official manager APK from the latest LyraVoid/FinaSU release
     (or use --apk for a local file).
  2. Read the first signer certificate (DER) from the APK Signing Block
     (v2 / v3 scheme blocks).
  3. size = len(cert) as 0x%04x, hash = SHA-256 of the cert DER (NOT of the APK).
  4. Inject KSU_EXPECTED_SIZE2 / KSU_EXPECTED_HASH2 / KSU_SECOND_SIGNATURE_RELEASE
     into <ksu-dir>/kernel/Kbuild (idempotent).
  5. Optionally export FINASU_EXPECTED_SIZE / FINASU_EXPECTED_HASH (only if
     --github-env / --github-output are passed; nothing is exported by default).

ksu_post_setup.sh is NOT run here; the action must call it afterwards.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

RELEASE_API = "https://api.github.com/repos/LyraVoid/FinaSU/releases/latest"
USER_AGENT = "Guts-Kernel"

SIG_BLOCK_MAGIC = b"APK Sig Block 42"
SIG_SCHEME_IDS = (0x7109871A, 0xF05368C0)  # v2, v3

MARKER = ("# injected by GKI_FinaSU_SUSFS: trust the official FinaSU manager "
          "via the second signature slot")
ANCHOR = "ccflags-y += -DEXPECTED_HASH="
MANAGED_PREFIXES = ("KSU_EXPECTED_SIZE2 :=", "KSU_EXPECTED_HASH2 :=",
                    "KSU_SECOND_SIGNATURE_RELEASE :=")


class CertError(RuntimeError):
    pass


# --------------------------------------------------------------------------- #
# Network
# --------------------------------------------------------------------------- #
def fetch(url: str, timeout: int = 300, retries: int = 3) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and urlparse(url).hostname == "api.github.com":
        headers["Authorization"] = f"Bearer {token}"
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt < retries:
                print(f"Retrying {url} ({attempt}/{retries}): {exc}")
                time.sleep(5)
    raise CertError(f"Download failed: {url}: {last}")


def pick_apk_asset(release: dict) -> dict:
    assets = [a for a in release.get("assets", [])
              if a.get("name", "").lower().endswith(".apk")]
    if not assets:
        raise CertError("No FinaSU Manager APK found in the latest release")
    # Prefer names containing "finasu", then "release".
    assets.sort(key=lambda a: ("finasu" not in a["name"].lower(),
                               "release" not in a["name"].lower()))
    return assets[0]


# --------------------------------------------------------------------------- #
# APK parsing
# --------------------------------------------------------------------------- #
def _u32(buf: bytes, off: int) -> int:
    if off < 0 or off + 4 > len(buf):
        raise CertError("Truncated APK signing data")
    return struct.unpack_from("<I", buf, off)[0]


def _u64(buf: bytes, off: int) -> int:
    if off < 0 or off + 8 > len(buf):
        raise CertError("Truncated APK signing data")
    return struct.unpack_from("<Q", buf, off)[0]


def _prefixed(buf: bytes, off: int) -> tuple[bytes, int]:
    """Read a uint32 length-prefixed chunk; return (chunk, next_offset)."""
    length = _u32(buf, off)
    start, end = off + 4, off + 4 + length
    if end > len(buf):
        raise CertError("Length-prefixed field exceeds its container")
    return buf[start:end], end


def _signing_block_pairs(data: bytes) -> bytes:
    """Locate the APK Signing Block through the ZIP EOCD and return its ID-value pairs."""
    eocd = data.rfind(b"PK\x05\x06", max(0, len(data) - 65_557))
    if eocd < 0 or eocd + 22 > len(data):
        raise CertError("Not a valid APK/ZIP (EOCD not found)")
    cd_offset = _u32(data, eocd + 16)

    if cd_offset < 32 or data[cd_offset - 16:cd_offset] != SIG_BLOCK_MAGIC:
        raise CertError("APK v2/v3 signing block not found")

    block_size = _u64(data, cd_offset - 24)
    block_start = cd_offset - block_size - 8
    if block_start < 0 or _u64(data, block_start) != block_size:
        raise CertError("Invalid APK signing block")
    return data[block_start + 8:cd_offset - 24]


def extract_cert(data: bytes) -> bytes:
    pairs = _signing_block_pairs(data)
    off = 0
    while off + 8 <= len(pairs):
        pair_len = _u64(pairs, off)
        off += 8
        if pair_len < 4 or off + pair_len > len(pairs):
            raise CertError("Invalid APK signing pair")
        pair_id = _u32(pairs, off)
        payload = pairs[off + 4:off + pair_len]
        off += pair_len
        if pair_id not in SIG_SCHEME_IDS:
            continue

        signers, _ = _prefixed(payload, 0)
        s = 0
        while s < len(signers):
            signer, s = _prefixed(signers, s)
            signed_data, _ = _prefixed(signer, 0)
            _, pos = _prefixed(signed_data, 0)          # skip digests
            certs, _ = _prefixed(signed_data, pos)      # certificates
            if certs:
                cert, _ = _prefixed(certs, 0)
                if cert:
                    return cert
    raise CertError("No signing certificate found")


# --------------------------------------------------------------------------- #
# Kbuild injection
# --------------------------------------------------------------------------- #
def inject_kbuild(kbuild: Path, size: str, digest: str) -> None:
    lines = kbuild.read_text().splitlines()

    # Drop any previous injection so re-runs never duplicate entries.
    lines = [l for l in lines
             if l != MARKER and not l.startswith(MANAGED_PREFIXES)]

    anchors = [i for i, l in enumerate(lines) if l.startswith(ANCHOR)]
    if len(anchors) != 1:
        raise CertError(f"Expected exactly one Kbuild anchor '{ANCHOR}', "
                        f"found {len(anchors)}")

    entries = [f"KSU_EXPECTED_SIZE2 := {size}",
               f"KSU_EXPECTED_HASH2 := {digest}",
               "KSU_SECOND_SIGNATURE_RELEASE := 1"]
    idx = anchors[0] + 1
    lines[idx:idx] = [MARKER, *entries]

    tmp = kbuild.with_name(kbuild.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n")
    os.replace(tmp, kbuild)

    content = kbuild.read_text().splitlines()
    for entry in entries:
        if content.count(entry) != 1:
            raise CertError(f"Kbuild verification failed: {entry}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def append_kv(path: str | None, pairs: dict[str, str]) -> None:
    if not path:
        return
    with open(path, "a") as fh:
        for k, v in pairs.items():
            fh.write(f"{k}={v}\n")


def run(args: argparse.Namespace) -> None:
    ksu_dir = Path(args.ksu_dir)
    kbuild = ksu_dir / "kernel" / "Kbuild"
    if not kbuild.is_file():
        raise CertError(f"FinaSU Kbuild not found: {kbuild}")

    print("::group::Obtain FinaSU Manager APK")
    if args.apk:
        apk_data = Path(args.apk).read_bytes()
        print(f"Using local APK: {args.apk}")
    else:
        release = json.loads(fetch(RELEASE_API, timeout=30))
        asset = pick_apk_asset(release)
        print(f"Release: {release.get('tag_name', '?')}  APK: {asset['name']}")
        apk_data = fetch(asset["browser_download_url"])
    if not apk_data.startswith(b"PK"):
        raise CertError("Downloaded file is not a valid APK")
    print(f"APK size: {len(apk_data)} bytes")
    print("::endgroup::")

    print("::group::Extract Manager Certificate")
    cert = extract_cert(apk_data)
    size = f"0x{len(cert):04x}"
    digest = hashlib.sha256(cert).hexdigest()  # hash of the cert DER, not the APK
    print(f"Certificate size  : {size}")
    print(f"Certificate SHA256: {digest}")
    print("::endgroup::")

    print("::group::Inject FinaSU Secondary Signature")
    inject_kbuild(kbuild, size, digest)
    print(f"KSU_EXPECTED_SIZE2: {size}\nKSU_EXPECTED_HASH2: {digest}\n"
          "KSU_SECOND_SIGNATURE_RELEASE: 1")
    print("::endgroup::")

    values = {"FINASU_EXPECTED_SIZE": size, "FINASU_EXPECTED_HASH": digest}
    append_kv(args.github_env, values)
    append_kv(args.github_output, {"size": size, "hash": digest})
    print("FinaSU Manager certificate configured successfully.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ksu-dir", required=True)
    ap.add_argument("--apk", help="Use a local APK instead of downloading")
    ap.add_argument("--github-env", help="Optional: append FINASU_EXPECTED_* to this file")
    ap.add_argument("--github-output", help="Optional: append size/hash step outputs to this file")
    try:
        run(ap.parse_args())
    except CertError as exc:
        print(f"::error title=FinaSU manager certificate::{exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
