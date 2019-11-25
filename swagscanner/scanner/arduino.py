import logging
import threading
import time
import uuid

import Adafruit_BluefruitLE

UART_SERVICE_UUID = uuid.UUID('5ffba521-2363-41da-92f5-46adc56b2d37')
ROTATE_TABLE_CHAR_UUID = uuid.UUID('5ffba522-2363-41da-92f5-46adc56b2d37')
TABLE_POSITION_CHAR_UUID = uuid.UUID('5ffba523-2363-41da-92f5-46adc56b2d37')
IS_TABLE_ROTATING_CHAR_UUID = uuid.UUID('5ffba524-2363-41da-92f5-46adc56b2d37')


class Arduino(threading.Thread):
    '''Arduino object

    '''

    def __init__(self,
                 uart_service_uuid=UART_SERVICE_UUID,
                 rotate_table_char_uuid=ROTATE_TABLE_CHAR_UUID,
                 table_position_char_uuid=TABLE_POSITION_CHAR_UUID,
                 is_table_rotating_char_uuid=IS_TABLE_ROTATING_CHAR_UUID):
        super(Arduino, self).__init__()
        self._uart_service_uuid = uart_service_uuid
        self._rotate_table_char_uuid = rotate_table_char_uuid
        self._table_position_char_uuid = table_position_char_uuid
        self._is_table_rotating_char_uuid = is_table_rotating_char_uuid

        self._rotate_table_char = None
        self._table_position_char = None
        self._is_table_rotating_char = None

        self._adapter = None
        self._device = None

        # Services notifications
        self._is_rotating = False
        self._table_position = 0

        self._initialize_ble()

    def run(self):
        '''Runs in background thread, will establish connection with the Arduino,
        find the service, find the characteristics and give the class instance a
        rotate_table_char

        '''

        self._initialize_device()

    def _initialize_ble(self):
        ''' Start up the BLE system
        Initializes a new ble object, clears the cache, finds a suitable
        bluetooth adapter, and disconnect previous uart devices

        '''

        # Get the BLE provider for the current platform.
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()
        self.ble.clear_cached_data()
        self.adapter = self.ble.get_default_adapter()
        self.adapter.power_on()

        print('Disconnecting any connected UART devices...')
        self.ble.disconnect_devices([UART_SERVICE_UUID])

    def _initialize_device(self):
        '''Set up the arduino and find its services and characteristics,
        then subscribe to the notify characteristics

        '''
        # Scan for UART devices.
        print('Searching for UART device...')
        try:
            self.adapter.start_scan()
            self.device = self.ble.find_device(
                service_uuids=[UART_SERVICE_UUID])
            print(f'device found: {self.device}')

            if self.device is None:
                raise RuntimeError('Failed to find UART device!')
        finally:
            self.adapter.stop_scan()
            self.device.connect()
            print('Connected: ' + str(self.device.is_connected))

        print('Discovering services...')
        self.device.discover([self._uart_service_uuid], [self._rotate_table_char_uuid,
                                                         self._table_position_char_uuid,
                                                         self._is_table_rotating_char_uuid])

        # find the services & characteristics
        uart = self.device.find_service(UART_SERVICE_UUID)
        rotate_table = uart.find_characteristic(self._rotate_table_char_uuid)
        table_position = uart.find_characteristic(
            self._table_position_char_uuid)
        is_table_rotating = uart.find_characteristic(
            self._is_table_rotating_char_uuid)

        # set the instance characteristic for rotate table
        self._rotate_table_char = rotate_table
        self._table_position_char = table_position
        self._is_table_rotating_char = is_table_rotating

        def received_position(data):
            data = int.from_bytes(data, byteorder='big')
            self._table_position = data
            print(f'table is at position: {self._table_position} degrees')

        def received_rotating(data):
            data = int.from_bytes(data, byteorder='big')

            if data == 0:
                self._is_rotating = False
            elif data == 1:
                self._is_rotating = True
            else:
                print(type(data))
                print(
                    f'is_table_rotating characteristic returning non binary output wtf? {data}')
            print(f'is table rotating: {self._is_rotating}')

        # Turn on notifications from the notifying characteristics
        print('Subscribing to table_position notifications...')
        table_position.start_notify(received_position)
        print('Subscribing to is_table_rotating notifications...')
        is_table_rotating.start_notify(received_rotating)

    def rotate_table(self, degs: int) -> int:
        '''Rotate the scanner bed

        Args:
            degs (uint): degrees you want the table to rotate

        Returns: 
            the number of degrees you rotated the table by

        '''

        print(f'sending rotation of {degs} degrees')
        self._rotate_table_char.write_value(
            (degs).to_bytes(1, byteorder='big'))
        return degs

    def disconnect_device(self):
        ''' Disconnect the current device when we're done

        '''

        print('disconnecting arduino...')
        self.device.disconnect()

    def get_position(self)->int:
        '''Access the table's current position in degrees

        Returns:
            Table's current position in degrees

        '''

        return self._table_position

    def is_rotating(self)->bool:
        '''Is the table still rotating?

        # TODO: Thread this function so you can actually see if the table
        is still rotating while the bed is moving

        Returns:
            True if the table is still rotating and false otherwise

        '''

        return self._is_table_rotating_char.read_value()


def main():
    arduino = Arduino()
    arduino.daemon = True
    arduino.setName('Arduino Thread')
    arduino.start()

    while True:
        user_input = input("Enter degrees: ")

        if user_input is "q":
            arduino.disconnect_device()
            break
        else:
            arduino.rotate_table(int(user_input))


if __name__ == "__main__":
    main()
