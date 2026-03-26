from mfrc522 import MFRC522
import utime

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

print("Bring TAG closer...")
print("")

detecting = False

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if detecting == False:
        if stat == reader.OK:
            detecting= True
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                print("CARD ID: "+str(card))

    elif detecting == True:
        if stat == reader.NOTAGERR:
            detecting = False
        else::
                card = int.from_bytes(bytes(uid),"little",False)
                print("CARD ID: "+str(card))

    utime.sleep_ms(50)

