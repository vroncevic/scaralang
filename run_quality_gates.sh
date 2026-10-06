#!/bin/bash
#
# @brief   scaralang
# @version 1.0.6
# @date    Sat Sep 26 10:20:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py scaralang
python3 gates/gates/isp_checker.py scaralang
python3 gates/gates/limits_checker.py scaralang
python3 gates/gates/srp_checker.py scaralang

echo "Done"
