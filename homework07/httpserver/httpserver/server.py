import socket
import threading
import typing as tp

import os

from .handlers import BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        # @see: https://stackoverflow.com/questions/36594400/what-is-backlog-in-tcp-connections
        if backlog_size < 0:
            backlog_size = 0

        if os.name == "nt" and backlog_size > 5:
            backlog_size = 5
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout: tp.Optional[float] = timeout
        self._threads: tp.List[threading.Thread] = []
        self._thread_limiter = threading.BoundedSemaphore(self.max_workers)

    def serve_forever(self) -> None:
        # @see: http://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html
        # @see: https://en.wikipedia.org/wiki/Thundering_herd_problem
        # @see: https://stackoverflow.com/questions/17630416/calling-accept-from-multiple-threads
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.bind((self.host, self.port))
        s.listen(self.backlog_size)
        try:
            while True:
                # establish connection with client
                try:
                    c, addr = s.accept()
                    c.settimeout(self.timeout)
                    my_thread = threading.Thread(target=self.handle_accept, args=(c, addr))
                    my_thread.daemon = True
                    my_thread.start()
                except (socket.timeout, BlockingIOError):
                    pass
        except:
            pass
        finally:
            s.close()

    def handle_accept(self, socket: socket.socket, addr: tp.Tuple[str, int]) -> None:
        self.request_handler_cls(socket, addr, self).handle()


class HTTPServer(TCPServer):
    pass
