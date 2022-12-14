umqtt_simple  一个简单的mqtt类
ap_webserver 作为ap站点，提供web，用于接收wifi的ssid和password设置
ble_advertising.py 蓝牙基础文件
ble_simple_peripheral.py 数据蓝牙的一个应用
config 读写文件等基础
tiger_mqtt  连接自己的mqtt服务





ADC
###############################################################################
# adc1_cal.py
#
# This module provides the ADC1Cal class
#
# MicroPython ESP32 ADC1 conversion using V_ref calibration value 
#
# The need for calibration is described in [1] and [4].
#
# Limitations of the current implementation ("works for me"):
# - only ADC1 is supported (as the name says)
# - only "V_ref"-calibration
#
# For a full discussion of the three different calibration options see [1]
#
# The V_ref calibration value can be read with the tool espefuse.py [1]
# Example:
# $ espefuse.py --port <port> adc_info
# Detecting chip type... ESP32
# espefuse.py v3.0
# ADC VRef calibration: 1065mV
#
# This is now done in the constructor if its argument <vref> is None.
#
# The ESP32 documentation is very fuzzy concerning the ADC input range,
# full scale value or LSB voltage, respectively.
# The MicroPython quick reference [3] is also (IMHO) quite misleading. 
# A good glimpse is provided in [4]. 
# 
# - "Per design the ADC reference voltage is 1100 mV, however the true
#   reference voltage can range from 1000 mV to 1200 mV amongst different
#   ESP32s." [1]
#
# - Attenuation and "suggested input ranges" [1]
#   +----------+-------------+-----------------+
#   |          | attenuation | suggested range |
#   |    SoC   |     (dB)    |      (mV)       |
#   +==========+=============+=================+
#   |          |       0     |    100 ~  950   |
#   |          +-------------+-----------------+
#   |          |       2.5   |    100 ~ 1250   |
#   |   ESP32  +-------------+-----------------+
#   |          |       6     |    150 ~ 1750   |
#   |          +-------------+-----------------+
#   |          |      11     |    150 ~ 2450   |
#   +----------+-------------+-----------------+
#   |          |       0     |      0 ~  750   |
#   |          +-------------+-----------------+
#   |          |       2.5   |      0 ~ 1050   |
#   | ESP32-S2 +-------------+-----------------+
#   |          |       6     |      0 ~ 1300   |
#   |          +-------------+-----------------+
#   |          |      11     |      0 ~ 2500   |
#   +----------+-------------+-----------------+
#
#
# Please refer to the section "Minimizing Noise" in [1].
#
# The calibration algorithm and constants are based on [2].
#
# [1] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html#adc-calibration
# [2] https://github.com/espressif/esp-idf/blob/master/components/esp_adc_cal/esp_adc_cal_esp32.c
# [3] https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
# [4] https://esp32.com/viewtopic.php?t=1045 ([Answered] What are the ADC input ranges?)
#
# created: 04/2021 updated: 12/2021
#
# This program is Copyright (C) 04/2021 Matthias Prinke
# <m.prinke@arcor.de> and covered by GNU's GPL.
# In particular, this program is free software and comes WITHOUT
# ANY WARRANTY.
#
# History:
#
# 20210418 Created
# 20210510 Ported calibration from esp_adc_cal_esp32.c [2]
# 20210511 Added internal reading of efuse calibration value
#          Fixed usage example
# 20210512 Modified class ADC1Cal to inherit from machine.ADC class
#          All bit widths are supported now
#          Removed rounding of the result in voltage()   
#          Added support of 0/2.5/6 dB attenuation
# 20211206 Merged pull request by codemee: added support for ATTN_11DB
#
# ToDo:
# - add support of "Two Point Calibration" 
#
#   https://github.com/matthias-bs/MicroPython-ADC_Cal
###############################################################################
