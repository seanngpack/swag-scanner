import threading

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
        # Can setup other things before the thread starts
    def run2(self):
        print ("Running")

thread_list = []
for i in range(4):
    thread = MyThread()
    thread_list.append(thread)
    thread.start()
