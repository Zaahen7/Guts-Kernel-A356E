# Guts-Kernel-A356E
¡Buen punto de partida! Con KernelSU + susfs ya integrados, tenés margen para tocar cosas más profundas del kernel sin depender de root visible. Para tu objetivo (batería primero, sin destruir el rendimiento), yo priorizaría en este orden:

1. Gobernador de CPU (lo más rentable primero)
Si ya usás schedutil (lo normal en kernels GKI 5.15), no lo cambies por ondemand o similares viejos, schedutil con EAS es más eficiente.
Ajustá los parámetros de schedutil: up_rate_limit_us y down_rate_limit_us. Subir un poco el "down_rate_limit" (por ejemplo de 20ms a 40-50ms) hace que baje de frecuencia más rápido tras un pico, sin sentirse "trabado" en uso normal.
Revisá las tablas de frecuencia/voltaje del Exynos 1380 (s5e8835). A diferencia de Qualcomm, en Exynos el undervolt suele estar más atado al firmware/PMIC y es más arriesgado (mayor probabilidad de freezes que en Snapdragon). Si te animás, hacé pruebas de UV muy conservadoras (2-3 pasos, no más) y testeá estabilidad con estrés prolongado antes de confiar en la build.
2. GPU (Mali-G68, DVFS)
El gobernador de GPU en Exynos suele ser bastante agresivo subiendo de clock ante cualquier touch. Revisá el driver Mali (mali_kbase) y ajustá los umbrales de "utilization" para que no salte a frecuencias altas tan rápido.
Bajar el clock máximo de GPU un escalón (si tu SoC lo permite) suele dar ahorro notable en batería con pérdida de rendimiento mínima en uso diario (no gaming pesado).
3. Scheduler / EAS
Revisá el modelo de energía (energy model) que usa el kernel para el "task placement" entre cluster little/mid/big. Si el modelo está mal calibrado (común en ports/kernels no oficiales), el scheduler manda tareas livianas a núcleos grandes innecesariamente.
Ajustar sched_boost y los umbrales de "touch boost" (Samsung suele inyectar boost agresivo al tocar la pantalla) puede ahorrar bastante sin que se note en la fluidez.
4. cpuidle / suspensión profunda
Confirmá que los estados de idle profundos (C-states, "arm,idle-states" en el device tree) estén habilitados y que el kernel entra correctamente en ellos. Muchos kernels custom de Exynos tienen mal calibrados los "residency" mínimos, lo que hace que la CPU nunca llegue al estado más profundo.
5. Wakelocks y wakeup sources
Antes de tocar nada agresivo, corré unos días con /sys/kernel/debug/wakeup_sources (o /sys/power/wakeup_sources) para identificar qué está despertando el SoC innecesariamente. No conviene bloquear wakelocks a ciegas, mejor identificar el proceso/driver culpable.
6. Memoria: zram/zswap
Si no está activo zram con compresión zstd (mejor ratio que lz4 con costo de CPU aceptable en un SoC de gama media), activalo. Ajustá el tamaño (típicamente 25-50% de la RAM) y el swappiness según cuánta RAM tenga tu variante del A35 (4/6/8GB).
7. I/O scheduler
Para UFS, mq-deadline suele ser más eficiente energéticamente que kyber en cargas normales de teléfono. Probá ambos y medí.
8. Compilación
Asegurate de compilar con LTO (al menos "thin LTO") y un toolchain Clang reciente (idealmente el mismo que usa AOSP para esa versión de kernel). Esto no cambia comportamiento en runtime pero mejora eficiencia de código generado.
Desactivá configs de debug que no necesites (CONFIG_DEBUG_*, tracing extra) — consumen ciclos y memoria sin beneficio para vos.
Metodología (importante)

Cambiá una cosa a la vez y medí con algo objetivo: dumpsys batterystats, Battery Historian, o simplemente horas de pantalla en uso real durante 2-3 días por cada cambio. Con Exynos, muchos ajustes "copiados" de kernels Qualcomm no aplican igual, así que confirmá que cada nodo/sysfs que tocás realmente exista y tenga efecto en tu driver.

¿Querés que empecemos por algo específico, por ejemplo el ajuste del gobernador de CPU o la calibración del modelo de energía?
