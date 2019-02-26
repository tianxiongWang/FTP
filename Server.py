import os
import socket
import threading
import sys
import time
#自定义FTP服务器类
class FtpServer(object):
    def __init__(self, ADDR, PATH):
        self.addr = ADDR
        self.ip = ADDR[0]
        self.port = ADDR[1]
        self.path = PATH
        self.Socket = socket.socket()
    def server_forever(self):
        self.Socket.bind(self.addr)
        print('监听端口%s中' % str(self.addr))
        self.Socket.listen(5)
        while True:
            c, addr = self.Socket.accept()
            print('客户端%s已连接' % str(addr))
            t = threading.Thread(target = self.ThreadServer, args = (c,))
            t.Daemon = True
            t.start()
    def ThreadServer(self, *c):
        c = c[0]
        while True:
#            print('等待客户端命令:')
            request = c.recv(1024)
            request = request.decode()
#            print(request)
            if request == 'R':
#                print('请求连接信息:')
                self.MakeSure(request, c)
            if request == 'view':
                self.View(c)
            if request == 'exit':
                print('客户端已退出，关闭%s线程!' % str(c))
                return None
            if request == 'download':
                self.DownLoad(c)
            if request == 'upload':
                self.UpLoad(c)
            else:
                pass
    def MakeSure(self, request, c):
        time.sleep(0.1)
        c.send('ok'.encode())
#        print('发送OK')
    def View(self, c):
#        print('调用文件列表函数!')
        FtpList = os.listdir(self.path)
        data = '#'.join(FtpList)
        time.sleep(0.1)
        c.send(data.encode())
    def DownLoad(self, c):
        self.View(c)
#        print('准备下载')
        filename = c.recv(1024)
        filename = filename.decode()
        filename = c.recv(1024)
        filename = filename.decode()
#        print(filename)
        try:
            f = open(self.path + filename, 'rb')
        except OSError:
            pass
#            print('文件打开失败!')
        else:
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(1)
                    c.send('######'.encode())
                    break
                time.sleep(0.1)
                c.send(data)
            f.close()
    def UpLoad(self, c):
        print('等待接收文件名...')
        filename = c.recv(1024)
        filename = filename.decode()
        print(filename)
        try:
            f = open(self.path + filename,'wb')
        except:
            print('文件打开失败!')
        else:
            while True:
                data = c.recv(1024)
                if data == b'######':
                    break
                f.write(data)
            f.close()
        print('上传程序完毕!')
def main():
    PATH = "C:\\Users\\Administrator\\Desktop\\Ftp\\FtpFile\\"
    IP = '172.17.0.4'
    PORT = 8421
    ADDR = (IP, PORT)   
    A = FtpServer(ADDR, PATH)
    A.server_forever()

if __name__ == '__main__':
    main()
