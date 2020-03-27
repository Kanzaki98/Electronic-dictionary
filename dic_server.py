from socket import *
import signal
import sys
from threading import Thread
from operation_db import *
from time import sleep
#全局变量
ADDR = ('0.0.0.0',8888)


#服务端请求
class Server:
    pass

def do_login(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


def do_register(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')

def do_query(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    #插入历史记录
    db.insert_history(name,word)
    explan = db.query(word)
    if explan:
        msg = "%s : %s"%(word,explan)
        c.send(msg.encode())
    else:
        c.send(b'None')

def do_history(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    r = db.history(name)
    if not r:
        c.send(b'None')
        return
    c.send(b'OK')
    for i in r:
        msg = '%s   %s   %s'%i
        sleep(0.1) #防止粘包
        c.send(msg.encode())

    sleep(0.1)
    c.send(b'##')


def handle(c,db):
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_history(c,db,data)

def main():
    #创建数据库连接对象
    db = Database()

    #创建tcp套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)


    print('Listen the port 8888...')
    while True:
        try:
            c,addr = sockfd.accept()
            print('connect from:',addr)
        except KeyboardInterrupt as e:
            sockfd.close()
            db.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        # 创建线程处理请求
        client = Thread(target=handle, args=(c,db))
        client.setDaemon(True)
        client.start()

if __name__ == '__main__':
    main()


