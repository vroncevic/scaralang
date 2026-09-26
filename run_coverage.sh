#!/bin/bash
#
# @brief   scaralang
# @version 1.0.0
# @date    Sat Sep 26 10:20:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py scaralang
pylint scaralang > scaralang.report
echo "Done"
