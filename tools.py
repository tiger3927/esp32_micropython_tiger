
import ubinascii
import os

from machine import Pin,ADC
from adc1_cal import ADC1Cal

statvfs_fields = ['bsize','frsize','blocks','bfree','bavail','files','ffree',]

print(dict(zip(statvfs_fields, os.statvfs('/'))))
import gc
print("mem left ",gc.mem_free())

#bsize：即block size 块大小,文件存取的最小单位，4096即表示文件存取的最小单位为4K.
#bfree：即block free 剩余块.
#所以剩余空间可以计算:bsize*bfree(单位是bytes).
#gc.mem_free()输出的单位是bytes.



#ADC.atten(attenuation)
#这个函数允许设置ADC输入的衰减量。这允许更大的输入电压范围，但代价是精度(现在相同的比特数代表更大的范围)。可能的衰减选项是：
#ADC.ATTN_0DB: 0dB 衰减,最大输入电压为1v，这是默认配置
#ADC.ATTN_2_5DB: 2.5dB 衰减, 最大输入电压约为1.34v
#ADC.ATTN_6DB: 6dB 衰减, 最大输入电压约为2.00v
#ADC.ATTN_11DB: 11dB 衰减, 最大输入电压约3.6v


ADC_PIN   = 35                # ADC input pin no.
DIV       = 1                 # div = V_measured / V_input; here: no input divider
AVERAGING = 10                # no. of samples for averaging (default: 10)

# vref = None -> V_ref calibration value is read from efuse
ubatt = ADC1Cal(Pin(ADC_PIN, Pin.IN), DIV, None, AVERAGING, "ADC1 eFuse Calibrated")

# set ADC result width
ubatt.width(ADC.WIDTH_12BIT)

# set attenuation
ubatt.atten(ADC.ATTN_11DB)

print('ADC Vref: {:4}mV'.format(ubatt.vref))
print('Voltage:  {:4.1f}mV'.format(ubatt.voltage))

