import pymysql
import hashlib
import time

class Database:
    def __init__(self, database='stu',
                 host='localhost',
                 user='root',
                 passwd='123456',
                 charset='utf8',
                 table='dictionary'):
        self.database = database
        self.host = host
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.table = table
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    def create_cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def register(self,name,passwd):
        sql  = 'select * from user where name = %s'
        if self.cur.execute(sql,name):
            return False
        #加密处理
        hash = hashlib.md5((name+'the-salt').encode())
        hash.update(passwd.encode())

        sql  = "insert into user (name,passwd) values('%s','%s')"%(name,hash.hexdigest())
        try:
            self.cur.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        sql = 'select * from user where name = %s and passwd = %s'
        # 加密处理
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())
        if self.cur.execute(sql,[name,hash.hexdigest()]):
            return True
        else:
            return False
    #插入历史记录
    def insert_history(self,name,word):
        tm = time.ctime()
        sql = "insert into history(name,word,htime) values('%s','%s','%s')"%(name,word,tm)
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception:
            self.db.rollback()
    #查单词
    def query(self,word):
        sql = "select explan from dictionary where word = '%s'"%word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r :
            return r[0]

    def history(self,name):
        sql = "select name,word,htime from history where name = '%s' order by id desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()



