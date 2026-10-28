#!/usr/bin/env python3
# Busca y muestra todos los .rej dentro de kernel_source
import os, sys

root = sys.argv[1] if len(sys.argv) > 1 else "kernel_source"
rejs = []

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d != ".git"]  # no entrar a .git
    for fn in filenames:
        if fn.endswith(".rej"):
            rejs.append(os.path.join(dirpath, fn))

if not rejs:
    print("No hay archivos .rej")
    sys.exit(0)

print(f"Se encontraron {len(rejs)} archivo(s) .rej\n")

for p in sorted(rejs):
    print("=" * 70)
    print(p)
    print("=" * 70)
    with open(p, encoding="utf-8", errors="replace") as f:
        print(f.read())
