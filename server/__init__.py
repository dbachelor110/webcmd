from server.route import server
import threading
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import ctypes
from waitress import serve

def run(port:int = 52010, debug=True):
    """Do: serve(self.server,host='0.0.0.0',port = 52010)"""
    if debug: server.run(host='0.0.0.0',port = port,debug=debug)
    else: serve(server,host='0.0.0.0',port = port)

class ServerThread(threading.Thread):
    """設計執行 serve(self.server,host='0.0.0.0',port = 52010) 的 Thread"""

    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.server = server
    
    def waitressRun(self):
        """Do: serve(self.server,host='0.0.0.0',port = 52010)"""
        run()

    def run(self):
        """Do: self.waitressRun()"""
        print('thread start\n')
        self.waitressRun()  # blocking
        print('thread done\n')

    def get_id(self):
        """returns id of the respective thread"""
        if hasattr(self, '_thread_id'):
            return self._thread_id
        
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def exit(self):
        """kill the thread"""
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')