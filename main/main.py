from ota_updater import OTAUpdater


def download_and_install_update_if_available():
    ota_updater = OTAUpdater('url-to-your-github-project')
    ota_updater.download_and_install_update_if_available('wifi-ssid', 'wifi-password')

def start():
    from network import LoRa
    import socket
    import time
    import binascii
    import pycom

    # Turn the light white
    pycom.heartbeat(False)
    pycom.rgbled(0x111111)

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

    # timestamp = time.now()

    while True:
        # Turn the light red
        pycom.rgbled(0x110000)

        s.setblocking(True)
        s.settimeout(10)

        # for testing new code, remove try/except

        try:
            s.send('Hello LoRa')
            # send the data from the sensor
            # ************************
        except:
            print ('timeout in sending')
        # Turn the light green
        pycom.rgbled(0x001100)

        try:
            data = s.recv(64)
            print(data)
            # Turn the light blue
            pycom.rgbled(0x000011)
        except:
            print ('nothing received')
            # Turn the light off
            pycom.rgbled(0x000000)

        # if time.now() - timestamp > 1 heure :
        #   ota_updater.check_for_update_to_install_during_next_reboot()

        s.setblocking(False)
        time.sleep (30)

def boot():
    download_and_install_update_if_available()
    start()


boot()
