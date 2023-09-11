from queue import Queue
from threading import Event, Thread, local

class ActorExit(Exception):
    pass

class Actor():

    thread_id = local()

    def __init__(self, max_thread=5):
        self._mail_box = Queue()
        self._max_thread = max_thread

    def start(self):
        self._terminated = [Event() for _ in range(self._max_thread)]
        for i in range(self._max_thread):
            t = Thread(target=self._bootstrap_thread, args=(i,))
            t.daemon = True
            t.start()

    def stop(self):
        for _ in range(self._max_thread):
            self.send(ActorExit)

    def send(self, msg):
        # no explicit yielding, wait for the interpreter to interupt
        # the execution and the OS to schedule threads
        self._mail_box.put(msg)

    def recv(self):
        msg = self._mail_box.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def run(self):
        msg = self.recv()
        print(msg)

    def _bootstrap_thread(self, tid):
        thread_id = tid
        try:
            while True:
                self.run()
        except ActorExit:
            # catch the ActorExit exception only
            # allow other exceptions to go through
            pass
        finally:
            self._terminated[thread_id].set()
    
    def terminate(self):
        for i in range(self._max_thread):
            self._terminated[i].wait()


act = Actor(max_thread=5)
act.start()
act.send('haha')
act.send('hehe')
act.stop()
act.terminate()