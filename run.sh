#!/bin/bash
#
# @brief   scaralang
# @version 1.1.1
# @date    Sat Sep 26 10:20:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

set -e

for scara_file in examples/*.scara; do
    if [[ "${scara_file}" == *"_decompiled.scara"* ]] || [[ "${scara_file}" == *"_decmpiled.scara"* ]]; then
        continue
    fi

    base_name="${scara_file%.scara}"
    bin_file="${base_name}.bin"
    decompiled_file="${base_name}_decompiled.scara"
    dis_file="${base_name}.dis"

    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    printf "║  Script: %-67s ║\n" "${scara_file}"
    echo "╠══════════════════════════════════════════════════════════════════════════════╣"
    printf "║  * Compile:     %-60s ║\n" "${bin_file}"
    printf "║  * Decompile:   %-60s ║\n" "${decompiled_file}"
    printf "║  * Disassemble: %-60s ║\n" "${dis_file}"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""

    echo "▶ Compiling ${scara_file} -> ${bin_file}..."
    python3 main.py compile --script "${scara_file}" --output "${bin_file}" --dump-frames --verbose

    echo "▶ Decompiling ${bin_file} -> ${decompiled_file}..."
    python3 main.py decompile --file "${bin_file}" --output "${decompiled_file}"

    echo "▶ Disassembling ${bin_file} -> ${dis_file}..."
    python3 main.py disassemble --file "${bin_file}" --output "${dis_file}"

    echo ""
    echo "────────────────────────────────────────────────────────────────────────────────"
done

echo "Done"
