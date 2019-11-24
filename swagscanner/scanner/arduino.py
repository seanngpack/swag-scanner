import logging
import time
import uuid

import Adafruit_BluefruitLE

UART_SERVICE_UUID = uuid.UUID('5ffba521-2363-41da-92f5-46adc56b2d37')
ROTATE_TABLE_CHAR_UUID = uuid.UUID('5ffba522-2363-41da-92f5-46adc56b2d37')
TABLE_POSITION_CHAR_UUID = uuid.UUID('5ffba523-2363-41da-92f5-46adc56b2d37')
IS_TABLE_ROTATING_CHAR_UUID = uuid.UUID('5ffba524-2363-41da-92f5-46adc56b2d37')


class Arduino():
    '''Arduino object

    '''

    def __init__(self, is_active=True,
                 uart_service_uuid=UART_SERVICE_UUID,
                 rotate_table_char_uuid=ROTATE_TABLE_CHAR_UUID,
                 table_position_char_uuid=TABLE_POSITION_CHAR_UUID,
                 is_table_rotating_char_uuid=IS_TABLE_ROTATING_CHAR_UUID):
        self.is_active = is_active
        self.__uart_service_uuid = uart_service_uuid
        self.__rotate_table_char = None
        self.__rotate_table_char_uuid = rotate_table_char_uuid
        self.__table_position_char_uuid = table_position_char_uuid
        self.__is_table_rotating_char_uuid = is_table_rotating_char_uuid

        self.device = None

        # Services notifications
        self.is_rotating = False
        self.table_position = 0

        # Get the BLE provider for the current platform.
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()
        # Start the mainloop to process BLE events, and run the provided function in a background thread.
        self.ble.run_mainloop_with(self.run_connection)

    def run_connection(self):
        '''Runs in background thread, will establish connection with the Arduino,
        find the service, find the characteristics and give the class instance a
        rotate_table_char

        '''

        self.ble.clear_cached_data()
        adapter = self.ble.get_default_adapter()
        adapter.power_on()
        print(f'Using adapter: {adapter.name}')

        print('Disconnecting any connected UART devices...')
        self.ble.disconnect_devices([UART_SERVICE_UUID])

        # Scan for UART devices.
        print('Searching for UART device...')
        try:
            adapter.start_scan()
            self.device = self.ble.find_device(service_uuids=[UART_SERVICE_UUID])
            print(f'device found: {self.device}')

            if self.device is None:
                raise RuntimeError('Failed to find UART device!')
        finally:
            adapter.stop_scan()
            self.device.connect()
            print('Connected: ' + str(self.device.is_connected))

        print('Discovering services...')
        self.device.discover([self.__uart_service_uuid], [self.__rotate_table_char_uuid,
                                                          self.__table_position_char_uuid,
                                                          self.__is_table_rotating_char_uuid])

        # find the services & characteristics
        uart = self.device.find_service(UART_SERVICE_UUID)
        rotate_table = uart.find_characteristic(self.__rotate_table_char_uuid)
        table_position = uart.find_characteristic(self.__table_position_char_uuid)
        is_table_rotating = uart.find_characteristic(self.__is_table_rotating_char_uuid)

        # set the instance characteristic for rotate table
        self.__rotate_table_char = rotate_table

        def received_position(data):
            print(f'Received: {data}')
            self.table_position = data

        def received_rotating(data):
            print(f'Received: {data}')
            if data == 0:
                self.is_rotating = False
            if data == 1:
                self.is_rotating = True
            else:
                print(
                    'is_table_rotating characteristic returning non binary output wtf?')

        # Turn on notifications from the notifying characteristics
        print('Subscribing to table_position notifications...')
        table_position.start_notify(received_position)
        print('Subscribing to is_table_rotating notifications...')
        is_table_rotating.start_notify(received_rotating)

    def rotate_table(self, degs: int):
        '''Rotate the scanner bed

        Args:
            degs (uint): degrees you want the table to rotate

        Returns: 
            the number of degrees you rotated the table by

        '''

        print(f'sending rotation of {degs} degrees')
        self.rotate_table.write_value((degs).to_bytes(1, byteorder='big'))
        return degs

    def disconnect_device(self):
        ''' Disconnect the current device when we're done

        '''

        self.device.disconnect()


def main():
    arduino = Arduino()
    arduino.rotate_table(30)
    time.sleep(10)
    arduino.rotate_table(30)
    arduino.disconnect_device()



if __name__ == "__main__":
    main()
