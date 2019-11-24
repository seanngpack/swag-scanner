from threading import Thread
import time
 
# A class that extends the Thread class
class FileLoaderThread(Thread):
   def __init__(self, fileName, encryptionType):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.fileName = fileName
       self.encryptionType = encryptionType
 
 
   # Override the run(0 function of Thread class
   def run(self):
       print('Started loading contents from file : ', self.fileName)
       print('Encryption Type : ', self.encryptionType)
       for i in range(5):
           print('Loading ... ')
           time.sleep(1)
       print('Finished loading contents from file : ', self.fileName)
 
 
 
 
def main():
 
   # Create an object of Thread
   th = FileLoaderThread('users.csv','ABC')
 
   # start the thread
   th.start()
 
   # print some logs in main thread
   for i in range(5):
       print('Hi from Main Function')
       time.sleep(1)
 
   # wait for thread to finish
   th.join()
 
 
if __name__ == '__main__':
   main()