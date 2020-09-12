import time

class Timer:
    
    """ Jeff Preshing's timer context manager:
        http://preshing.com/20110924/timing-your-code-using-pythons-with-statement/ """
    
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.total = self.end - self.start

timer = Timer()

