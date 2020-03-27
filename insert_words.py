import pymysql
import re
db = pymysql.connect(
    host = 'localhost',user = 'root', passwd = '123456',database = 'stu',charset = 'utf8'
)
cur = db.cursor()
dict = []
with open('dict.txt','r') as f:
    for line in f:
        dict.append(line)
f.close()
for i in dict:
    word = re.search(r'\S+',i).group()
    explan = re.findall(r' (\S+)',i)
    explan = ' '.join(explan)
    sql = 'insert into dictionary (word,explan) values(%s,%s)'
    try:
        cur.execute(sql,[word,explan])
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        break
print('插入完毕')
cur.close()
db.close()
