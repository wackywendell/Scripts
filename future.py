"""future.py - implements a class to run a single function in its own thread.

Instantiate with futurefunc = Future(function, arg1, arg2, ..)
then futurefunc() will block until the function returns, and then return the functions results

Taken from http://code.activestate.com/recipes/84317/
with heavy modifications
"""

from threading import *
import copy

class Future:

    def __init__(self,func,*param, **kwargs):
        # Constructor
        self.__done=0
        self.__result=None
        self.__status='working'

        self.__C=Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T=Thread(target=self.Wrapper,args=(func,param, kwargs))
        self.__T.setName("FutureThread")
        self.__T.start()
        self.__excpt = None

    def __repr__(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
        # We deepcopy __result to prevent accidental tampering with it.
        if self.__excpt:
            raise self.__excpt[0], self.__excpt[1], self.__excpt[2]

        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self, func, param, kwargs):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result = func(*param, **kwargs)
        except:
            self.__result = "Exception raised within Future"
            self.__excpt = sys.exc_info()

        self.__done=1
        self.__status=`self.__result`
        self.__C.notify()
        self.__C.release()
