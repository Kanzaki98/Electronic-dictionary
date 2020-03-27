from socket import *
sockfd = socket()
sockfd.connect(('127.0.0.1', 8888))

def do_query(name):
    while True:
        word = input('单词：')
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        sockfd.send(msg.encode())
        #等待回复
        data = sockfd.recv(2048).decode()
        print(data)

def do_history(name):
    msg = 'H %s' % (name)
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while True:
            data = sockfd.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")


#二级界面
def login(name):
    while True:
        print("===================================")
        print("=============  查单词  =============")
        print("============= 历史记录  ============")
        print("=============== 注销 ==============")
        print("===================================")
        cmd = input('msg:')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print('请输入正确命令！')

#注册
def do_register():
    while True:
        name = input("name:")
        passwd = input("passwd:")
        passwd1 = input("again:")
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s"%(name,passwd)
        #发送请求
        sockfd.send(msg.encode())
        #接受反馈
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return

#登陆
def do_login():
    name = input("name:")
    passwd = input("passwd:")
    msg = "L %s %s"%(name,passwd)
    # 发送请求
    sockfd.send(msg.encode())
    # 接受反馈
    data = sockfd.recv(128).decode()
    if data == 'OK':
        print("登陆成功")
        login(name)
    else:
        print("登陆失败")
    return


def main():
    while True:
        print("===================================")
        print("=============  login  =============")
        print("============= register ============")
        print("=============== quit ==============")
        cmd = input('msg:')
        if cmd == '1':
            do_login()
        elif cmd == '2':
            do_register()
        elif cmd == '3':
            sockfd.send(b'E')
            print("谢谢使用")
            return
        else:
            print('请输入正确命令！')

if __name__ == '__main__':
    main()