import os
import socket
import threading
import sys
import time

class FtpClient(object):
    def __init__(self, ADDR):
        self.Socket = socket.socket()
        self.addr = ADDR
    def Menu(self):
        print('=' * 40 + '命令集' + '=' * 40)
        print('*' * 37 + '1、查看目录' + '*' * 38)
        print('*' * 37 + '2、下载文件' + '*' * 38)
        print('*' * 37 + '3、上传文件' + '*' * 38)
        print('*' * 37 + '4、退    出' + '*' * 38)
    def Exit(self):
        self.Socket.send('exit'.encode())
        sys.exit('客户端退出!')
    def View(self):
        self.Socket.send('view'.encode())
        data = self.Socket.recv(40000)
        print()
        print()
        print('文件目录如下:')
        filelist = data.decode().split('#')
        self.filedict = {}
        count = 1
        for i in filelist:
            self.filedict[count] = i
            print(count, '、', i,sep = '')
            count += 1
    def DownLoad(self):
        self.Socket.send('download'.encode())
        self.View()
        cmd = input('你想下载哪个文件，输入序号:')
        try:
            filename = self.filedict[int(cmd)]                    #通过字典索引文件名
            print(filename)
            self.Socket.send(filename.encode())
        except:
            print('输入有误，已跳回主菜单!')
            return None
        try:
            f = open(filename,'wb')
        except:
            print('打开文件失败!')
        else:
            while True:
                data = self.Socket.recv(1024)
                if data == b'######':
                    break
                f.write(data)
            f.close()
    def UpLoad(self):
        self.Socket.send('upload'.encode())
        FileList = os.listdir()
        for i in FileList:
            print(FileList.index(i) + 1 , '、' , i)
        print('文件列表已列出，你想传哪一个文件至云端?\n由于制作简陋，不支持文件夹上传，请上传有后缀的文件!')
        file = input()
        filename = FileList[int(file) - 1]                         #获取已上传的文件名
        self.Socket.send(filename.encode())
        try:
            f = open(filename,'rb')
        except:
            print('打开文件失败,返回主菜单！')
        else:#循环读取文件，并上传到云端
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.Socket.send('##'.encode())
                    break
                self.Socket.send(data)
            f.close()
        print('上传完毕！\n\n')
    def client_forever(self):
        try:
            self.Socket.connect(self.addr)
        except:
            sys.exit('连接服务器失败，已退出!')
        self.Socket.send('R'.encode())
        data = self.Socket.recv(1024)
        if data.decode() == 'ok':
            while True:
                self.Menu()
                cmd = input('输入你的指令:')
                if cmd == '1':
                    self.View()
                if cmd == '2':
                    self.DownLoad()
                if cmd == '3':
                    self.UpLoad()
                if cmd == '4':
                    self.Exit()

def main():
    ADDR = ('129.211.125.18',8421)
    A = FtpClient(ADDR)
    A.client_forever()
if __name__ == '__main__':
    main()



