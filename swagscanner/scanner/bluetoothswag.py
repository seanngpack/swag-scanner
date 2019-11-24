import logging
import time
import uuid

import Adafruit_BluefruitLE


# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)

# Define service and characteristic UUIDs used by the UART service.
UART_SERVICE_UUID       = uuid.UUID('5ffba521-2363-41da-92f5-46adc56b2d37')
ROTATE_TABLE_CHAR       = uuid.UUID('5ffba522-2363-41da-92f5-46adc56b2d37')
TABLE_POSITION_CHAR     = uuid.UUID('5ffba523-2363-41da-92f5-46adc56b2d37')
IS_TABLE_ROTATING_CHAR  = uuid.UUID('5ffba524-2363-41da-92f5-46adc56b2d37')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print(f'Using adapter: {adapter.name}')

    print('Disconnecting any connected UART devices...')
    ble.disconnect_devices([UART_SERVICE_UUID])

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        device = ble.find_device(service_uuids=[UART_SERVICE_UUID])
        print(f'device found: {device}')

        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    device.connect()
    print('Connected: ' + str(device.is_connected))
    print('Advertised services: ' + str(device.advertised))

    try:
        print('Discovering services...')
        device.discover([UART_SERVICE_UUID], [ROTATE_TABLE_CHAR, TABLE_POSITION_CHAR, IS_TABLE_ROTATING_CHAR])
        
        uart = device.find_service(UART_SERVICE_UUID)
        rotate_table = uart.find_characteristic(ROTATE_TABLE_CHAR)
        table_position = uart.find_characteristic(TABLE_POSITION_CHAR)
        is_table_rotating = uart.find_characteristic(IS_TABLE_ROTATING_CHAR)

        rotate_table.write_value((3).to_bytes(1, byteorder='big'))

        def received(data):
            print(f'Received: {data}')

        # Turn on notification of RX characteristics using the callback above.
        print('Subscribing to is_table_rotating characteristic changes...')
        is_table_rotating.start_notify(received)
        table_position.start_notify(received)
        time.sleep(1)
        print(table_position.read_value())
        rotate_table.write_value((3).to_bytes(1, byteorder='big'))
        time.sleep(4)
        rotate_table.write_value((3).to_bytes(1, byteorder='big'))
        
        time.sleep(60)

    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()



# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)