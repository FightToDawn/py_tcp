# 陈硕 Linux多线程服务端程序 6.6.2 常见的并发网络服务程序设计方案0
# 一次只能服务一个客户 不适合长连接

import socket

def handle(client_socket, client_address):
    while True:
        data = client_socket.recv(4096)
        if (data):
            print ('recv data ', data)
            sent = client_socket.send(data)
        else:
            print ('disconnect ', client_address)
            client_socket.close()
            break

if __name__ == "__main__":
    listen_address = ("0.0.0.0", 15173)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(listen_address)
    server_socket.listen(5)

    while True:
        (client_socket, client_address) = server_socket.accept()
        print('got connection from ', client_address)
        handle(client_socket, client_address)
