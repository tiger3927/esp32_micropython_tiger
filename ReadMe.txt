umqtt_simple  一个简单的mqtt类
ap_webserver 作为ap站点，提供web，用于接收wifi的ssid和password设置
ble_advertising.py 蓝牙基础文件
ble_simple_peripheral.py 数据蓝牙的一个应用
config 读写文件等基础
tiger_mqtt  连接自己的mqtt服务

先：
烧录系统
esptool -p COM4 erase_flash
esptool --chip esp8266 --port COM4 --baud 115200 write_flash --flash_size=detect 0 "D:\Cloud\SDK\ESP32 ESP8266 开发板\固件\esp8266-1m-20220618-v1.19.1.bin"

然后：
u工具，逐个放入py文件

1 esp8266_bcff4df960f8
2 esp8266_bcff4df9a604
3 esp8266_bcff4df960a4
4 esp8266_c8c9a363bf5c
5 esp8266_bcff4df96143
6 esp8266_c8c9a3696760
7 esp8266_c45bbe50499d
8 esp8266_c8c9a357c5bb
9 esp8266_bcff4df961fe
10 esp8266_c8c9a357f398
11 esp8266_e8db84af5732
12 esp8266_bcff4df95ec0
13 esp8266_bcff4df961e7
14 esp8266_c45bbe63af54
15 esp8266_bcff4df960d9

