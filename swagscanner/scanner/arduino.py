import logging
import time

class Arduino():
    '''Arduino object

    '''

    def __init__(self, is_active=True):
        self.is_active = is_active
        if is_active:
            try:
                # TODO: Do bluetooth stuff to connect to arduino
                logging.info("Arduino sucessfully connected!")
            except:
                logging.warning("Oh shit...the arduino is not connecting")
