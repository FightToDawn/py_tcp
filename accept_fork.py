# 陈硕 Linux多线程服务端程序 6.6.2 常见的并发网络服务程序设计方案1和方案2
# accept 然后 fork 子进程处理连接 一个连接对应一个进程
# accept 然后 创建一个线程 处理连接

from socketserver import BaseRequestHandler, TCPServer
from socketserver import ForkingTCPServer, ThreadingTCPServer

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('got connection from ', self.client_address)
        while True:
            data = self.request.recv(4096)
            if data:
                print ('recv data ', data)
                sent = self.request.send(data)
            else:
                print('disconnect', self.client_address)
                self.request.close()
                break

if __name__ == "__main__":
    listen_address = ("0.0.0.0", 15173)
    server = ForkingTCPServer(listen_address, EchoHandler)
    # server = ThreadingTCPServer(listen_address, EchoHandler)
    server.serve_forever()
