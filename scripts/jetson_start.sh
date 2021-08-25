#!/usr/bin/env sh

sudo echo 5000 > /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/crit_current_limit_0
sudo nvpmodel -m 2 && sudo jetson_clocks
# available freq: 1651200 1728000 1804800 1881600 1907200
for i in /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq; do echo 1907200 > $i; done
cd /home/openpilot/openpilot/selfdrive/manager && PASSIVE=0 NOSENSOR=1 USE_MIPI=1 ./manager.py