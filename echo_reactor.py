# 陈硕 Linux多线程服务端程序 6.6.2 常见的并发网络服务程序设计方案5 改进
# 使用poll实现 单线程reactor
# Doug Schmidt指出，其实网络编程中有很多是事务性（routine）的工作，可以提取为 公用的框架或库，
# 而用户只需要填上关键的业务逻辑代码，并将回调注册到框架中，就可 以实现完整的网络服务，这正是Reactor模式的主要思想
# 类似注册回调函数的方式
# 应避免在回调中执行耗时操作

import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(('0.0.0.0',15173))
server_socket.listen(5)

poll = select.poll()
connections = {}
handlers = {}

def handle_input(socket, data):
    socket.send(data)

def handle_request(fileno, event):
    if event & select.POLLIN:
        client_socket = connections[fileno]
        data = client_socket.recv(4096)
        if data:
            print('recv data ',data)
            handle_input(client_socket, data)
        else:
            poll.unregister(fileno)
            client_socket.close()
            del connections[fileno]
            del handlers[fileno]

def handle_accept(fileno, event):
    (client_socket, client_address) = server_socket.accept()
    print('got connection from ',client_address)
    poll.register(client_socket.fileno(), select.POLLIN) # 把tcp客户端连接的文件号 注册到poll里 这样就会收到 接收数据事件
    connections[client_socket.fileno()] = client_socket
    handlers[client_socket.fileno()] = handle_request

poll.register(server_socket.fileno(), select.POLLIN) # 把server_socket文件号 注册到poll里 这样就会收到事件 连接进入的事件
handlers[server_socket.fileno()] = handle_accept

while True:
    events = poll.poll(10000) # 10 seconds 在没有事件时 线程会在这里等待
    for fileno, event in events:
        handler = handlers[fileno]
        handler(fileno,event)
