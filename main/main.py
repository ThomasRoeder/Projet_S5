import os
import main.ota_updater as ota_updater
from main.config import GITHUB_URL, WIFI_SSID, WIFI_PW, UPDATE_ORDER
import main.data_sensor as data_sensor
from machine import I2C
import time

def download_and_install_update_if_available(my_ota_updater):
    my_ota_updater.download_and_install_update_if_available(WIFI_SSID, WIFI_PW)

def start(my_ota_updater):
    from network import LoRa
    import socket
    import time
    import binascii
    import pycom

    # Turn the light red # blue
    pycom.heartbeat(False)
    pycom.rgbled(0x110000) # 0x000011


    # Initialise LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN)

    print ("devEUI {}".format(binascii.hexlify(lora.mac())))

    app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ',''))
    app_key = binascii.unhexlify('11 22 33 44 55 66 77 88 11 22 33 44 55 66 77 88'.replace(' ',''))

    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key),  timeout=0)

    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not yet joined...')

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    #s.bind(5)
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setsockopt(socket.SOL_LORA,  socket.SO_CONFIRMED,  False)

    timestamp = time.time()

    # setup for the data sending
    i2c = I2C(0, I2C.MASTER, baudrate=400000)
    print (i2c.scan())
    bme = data_sensor.BME280(i2c=i2c)
    ob = 0

    while True:
        # Turn the light green
        pycom.rgbled(0x001100)

        s.setblocking(True)
        s.settimeout(10)

        # reading data
        ar = bme.read_raw_temp()
        a = bme.read_temperature()
        br = bme.read_raw_pressure()
        b = bme.read_pressure()
        cr = bme.read_raw_humidity()
        c = bme.read_humidity()
        # print ("temp", ar,  a, "° - hum", cr,  c, "% - pres", br,
        #     "pres", b, "hPa [delta", ob - br, "]" )
        ob = br
        # for testing new code, remove try/except
        message_to_send = "Temp : " + str(a) + "°C - Hum : " + str(c) + "% - Pres : " + str(b) + "hPa"
        print(message_to_send)
        try:
            # send the data from the sensor
            s.send(message_to_send)
        except:
            print ('timeout in sending')
        # Turn the light red
        pycom.rgbled(0x110000)

        try:
            data_received = s.recv(64)
            print(data_received)
            # Turn the light white
            pycom.rgbled(0x111111)
        except:
            print ('nothing received')
            data_received = ""
            # Turn the light off
            pycom.rgbled(0x000000)

        # regularly check for a new update
        print("pre if")
        if data_received :
            data_received = str(data_received)[2:-1]
            print(data_received)
            if data_received == UPDATE_ORDER :
                print("if before")
                my_ota_updater.check_for_update_to_install_during_next_reboot(WIFI_SSID, WIFI_PW)
                # turn wifi off
                print("if after")


        # s.setblocking(False)
        print("sleep")
        time.sleep (10)


def boot():
    my_ota_updater = ota_updater.OTAUpdater(GITHUB_URL, main_dir="main")
    # download_and_install_update_if_available(my_ota_updater)
    start(my_ota_updater)


boot()
