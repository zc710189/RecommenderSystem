# -*- coding: utf-8 -*-
import MySQLdb as Mdb
import pymysql as pm
import re

con = pm.connect(host='localhost', user='root', passwd='123456', charset='utf8')
cur = con.cursor()

def Build_db():
    cur.execute("create database RS_db character set utf8;")
    cur.execute("use RS_db;")
    cur.close()
    con.close()

def Create_table(con, table_name):
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0

def Create_databases(db_name):
    sql = "show databases;"
    cur.execute(sql)
    dbs = [cur.fetchall()]
    db_list = re.findall('(\'.*?\')', str(dbs))
    db_list = [re.sub("'", '', each) for each in db_list]
    if db_name in db_list:
        return 1
    else:
        return 0

db_name = "rs_db"
if(Create_databases(db_name) != 1):
    Build_db()
problem = """CREATE TABLE PROBLEM (
             QUESTION_TYPE  CHAR(50) NOT NULL,
             TOTAL_SCORE  INT NOT NULL)"""
users = """CREATE TABLE USERS (
             ACCOUNT_NUMBER  CHAR(20) PRIMARY KEY NOT NULL,
             PASSWORD  CHAR(20) NOT NULL,
             ID  CHAR(10) NOT NULL,
             NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1) )"""
Mistaken_questions = """CREATE TABLE MISTAKEN_QUESTIONS (
             QUESTION_TYPE  CHAR(50) NOT NULL,
             TOTAL_SCORE  INT NOT NULL,
             SCORE INT NOT NULL )"""
TablesN=["problem","users","mistaken_questions"]
Tables=[problem,users,Mistaken_questions]


connect = pm.connect(host='localhost', user='root', passwd='123456', db='RS_db', charset='utf8')
con = connect.cursor()
for i in range(len(Tables)):
    if(Create_table(con,TablesN[i]) != 1):
        print("表不存在，添加一张")
        con.execute(Tables[i])
#test部分
"""sqladd1 = "INSERT INTO PROBLEM(QUESTION_TYPE, TOTAL_SCORE) VALUES ('chen', 10)"
sqladd2 = "INSERT INTO PROBLEM(QUESTION_TYPE, TOTAL_SCORE) VALUES ('zhen', 20)"
sqladd3 = "INSERT INTO MISTAKEN_QUESTIONS(QUESTION_TYPE, TOTAL_SCORE ,SCORE) VALUES ('1234321', 10 ,6)"

con.execute(sqladd1)
con.execute(sqladd2)
con.execute(sqladd3)
sqlR = "show columns from RS_db.MISTAKEN_QUESTIONS;"
con.execute(sqlR)
TableField = [con.fetchall()]
db_list = re.findall('(\'.*?\')', str(TableField))
db_list = [re.sub("'", '', each) for each in db_list]
test_list = []
for i in range(len(db_list)/5):
    test_list.append(db_list[i*5])
print(test_list)
data_one = cur.fetchone()
print(data_one)
data_many = con.fetchmany(1)
print(data_many)
data_all = con.fetchall()
print(data_all)
print(TableField)
print(db_list)
sql_select = "SELECT * FROM PROBLEM"
con.execute(sql_select)
data_all = con.fetchall()
data_list = re.findall('(\'.*?\')', str(data_all))
data_list = [re.sub("'", '', each) for each in data_list]
print(data_all)
LookupSelAttribute = raw_input("请选择查找属性：")
LookupAttributeValue = raw_input("请选择查找属性值：")
sql_Lookup = "SELECT * FROM MISTAKEN_QUESTIONS WHERE "+LookupSelAttribute+"='"+LookupAttributeValue+"'"
print(con.execute(sql_Lookup))
sqldel1 = "DELETE FROM PROBLEM WHERE QUESTION_TYPE='chen'"
sqldel2 = "DELETE FROM PROBLEM WHERE QUESTION_TYPE='zhen'"
sqldel3 = "DELETE FROM MISTAKEN_QUESTIONS WHERE QUESTION_TYPE='1234321'"
con.execute(sqldel1)
con.execute(sqldel2)
con.execute(sqldel3)"""
#test部分

def FindTable():
    while True:
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        for i in table_list:
            print(i)
        TableName = raw_input("请选择的表名：")
        if TableName in table_list:
            return TableName
        else:
            print("请重新选择：")
def FindAttribute(TableName):
    sql = "show columns from " + TableName + " from RS_db"
    FieldNum = con.execute(sql)
    TableField = [con.fetchall()]
    temp_list = re.findall('(\'.*?\')', str(TableField))
    temp_list = [re.sub("'", '', each) for each in temp_list]
    Attribute = []
    for i in range(len(temp_list) / 5):
        Attribute.append(temp_list[i * 5])
    return Attribute
def Add():
    print("请从以下表中选择添加数据的表：")
    TableName = FindTable()
    Attribute = FindAttribute(TableName)
    Attributes = ""
    for i in range(len(Attribute)):
        if 0 != i:
            Attributes += ","
        Attributes += Attribute[i]
    temp = ""
    for i in range(len(Attribute)):
        if 0 != i:
            temp += ","
        temp += "%s"
    while True:
        sql_insert = "INSERT INTO "+TableName+"("+Attributes+") VALUES ("+temp+")"
        temp_data = []
        for i in range(len(Attribute)):
            print("请输入%s："%(Attribute[i]))
            temp=raw_input("")
            temp_data.append(temp)
        try:
            con.execute(sql_insert, temp_data)
            connect.commit()
            print('添加成功！')
            break
        except Exception as e:
            print('出错回滚完成', e)
            connect.rollback()
            con.close()
            connect.close()
def Delelt():
    print("请从以下表中选择删除数据的表：")
    TableName = FindTable()
    print("请从以下属性中选择：")
    Attribute = FindAttribute(TableName)
    for i in Attribute:
        print(i)
    SelAttribute = raw_input("请选择属性：")
    AttributeValue = raw_input("请选择属性值：")
    sql_delete = "DELETE FROM "+TableName+" where "+SelAttribute+"='"+AttributeValue+"'"
    con.execute(sql_delete)
def Lookup():
    print("请从以下表中选择查看数据的表：")
    TableName = FindTable()
    sql_select = "SELECT * FROM "+TableName
    con.execute(sql_select)
    data_all = con.fetchall()
    data_list = re.findall('(\'.*?\')', str(data_all))
    data_list = [re.sub("'", '', each) for each in data_list]
    print(data_all)
    print(data_list)
def Change():
    print("请从以下表中选择修改数据的表：")
    TableName = FindTable()
    print("请从以下属性中选择：")
    Attribute = FindAttribute(TableName)
    for i in Attribute:
        print(i)
    while True:
        LookupSelAttribute = raw_input("请选择查找属性：")
        LookupAttributeValue = raw_input("请选择查找属性值：")
        sql_Lookup = "SELECT * FROM "+TableName+" WHERE "+LookupSelAttribute+"='"+LookupAttributeValue+"'"
        if 0==con.execute(sql_Lookup):
            print("没有该字段！请重新输入")
            continue
        else:
            break
    ModSelAttribute = raw_input("请选择修改属性：")
    ModAttributeValue = raw_input("请选择修改属性值：")
    sql_update = "UPDATE "+TableName+" SET "+ModSelAttribute+"="+ModAttributeValue+" WHERE "+LookupSelAttribute+"='"+LookupAttributeValue+"'"
    con.execute(sql_update)


while True:
    print("1.添加")
    print("2.删除")
    print("3.查找")
    print("4.修改")
    print("5.退出")
    num=int(input("请输入1-5的数字选择功能："))
    if 1==num:
        Add()
    elif 2==num:
        Delelt()
    elif 3==num:
        Lookup()
    elif 4==num:
        Change()
    elif 5==num:
        break
    else:
        print("请输入1-5的数字！")


