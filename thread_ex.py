import threading
import ctypes

class thread_with_exception(threading.Thread):
    def __init__(self, f):
        threading.Thread.__init__(self)
        self.f = f

    def run(self):
        try:
            self.f()
        except Exception as e:
            print('raised')
        finally:
            print('ended')

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id

        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


