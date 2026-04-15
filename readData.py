from mfrc522 import MFRC522
from time import sleep
from machine import RTC
import network
import usocket as socket
import secrets # learn how to use

ssid = "placeholder"
password = "placeholder"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connectionTimeout = 10

while connectionTimeout > 0:
    if wlan.status() >= 3:
        break
    connectionTimeout -= 1
    print(f"Connection attempts remaining: {connectionTimeout}")
    sleep(1)

if wlan.status() != 3:
    raise RuntimeError(f"Failed to establish a network connection to {ssid}")
else:
    print("Connetion successful")
    networkInformation = wlan.ifconfig()
    print(f"IP address: {networkInformation[0]}")

print(wlan.isconnected())

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
rtc = RTC()

detecting = False

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)

    # Get date time info
    (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()

    # If we were not previously detecting and we are now detecting then print data and mark previous detection
    if (detecting == False and stat == reader.OK):
        detecting = True
        (stat, uid) = reader.SelectTagSN()
        card = int.from_bytes(bytes(uid),"little",False)
        print("{:04}-{:02}-{:02} @ {:02}:{:02}:{:02} | ID: ".format(year, month, day, hours, minutes, seconds) + str(card) + "\n")

        with open("log.txt", "a") as file:
            file.write("{:04}-{:02}-{:02} @ {:02}:{:02}:{:02} | ID: ".format(year, month, day, hours, minutes, seconds) + str(card) + "\n")

    # If we were detecting and no longer detecting then mark as no longer detecting
    elif (detecting == True and stat == reader.ERR):
        detecting = False

    sleep(.05)

