import traceback
import logging

class ServerException(Exception):

    def __init__(self, errorLevel = "Debug", errorMessage = "", log = False):
        logging.basicConfig(filename = "app.log", filemode = "w", format = "{%(asctime)s ==> (%(name)s} -- [%(levelname)s] -- %(message)s", datefmt = "%d-%b-%y %H:%M:%S")
        self.errorLevel = errorLevel
        self.errorMessage = errorMessage
        self.PrintErrorLevel(log)


    def PrintErrorLevel(self, log = False):
        '''
        For printing error level and logging if necessary

        Keyword Arguments:
            log {bool} -- The status for logging (default: {True})
        '''

        print("{%s}: %s" %(self.errorLevel, self.errorMessage))
        if log:
            if self.errorLevel == "Critical":
                logging.critical(self.errorMessage, exc_info = True)
                Exception.__init__(self, self.errorMessage)
                exit(1)
            if self.errorLevel == "Debug":
                logging.debug(self.errorMessage, exc_info = True)
                Exception.__init__(self, self.errorMessage)
            if self.errorLevel == "Warn":
                logging.warning(self.errorMessage, exc_info = True)
                Exception.__init__(self, self.errorMessage)


# Testing
if __name__ == "__main__":
    
    while(True):
        try:
            a = int(input("Enter 1 to cause Critical Error\nEnter 2 to cause Warning\nEnter any other number to cause debug: "))
            if a == 1:
                raise ServerException(errorLevel = "Critical", errorMessage = "Testing Critical", log = True)
            if a == 2:
                raise ServerException(errorLevel = "Warn", errorMessage = "Testing Warning", log = True)
            else:
                raise ServerException(errorLevel = "Debug", errorMessage = "Testing Debug", log = True)
        except ServerException:
            continue
