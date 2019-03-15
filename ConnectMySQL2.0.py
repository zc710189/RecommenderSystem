# -*- coding: utf-8 -*-
import pymysql as pm
import re
db_name = "RecommendSystem_db"  # 数据库名称
show_db_sql = "SHOW DATABASE;"  # 显示所有数据库的sql语句
show_table_sql = "SHOW TABLES;"  # 显示所有表的sql语句
create_db_sql = "CREATE DATABASE " + db_name + " CHARACTER SET UTF8;"  # 创建数据库的sql语句
select_db_sql = "USE " + db_name + ";"  # 选择数据库的sql语句
# 创建表的sql语句
problem = """CREATE TABLE PROBLEM (
             TITLE_NUMBER INT PRIMARY KEY,
             QUESTION_TYPE  CHAR(50) NOT NULL,
             TOTAL_SCORE  INT NOT NULL)"""
users = """CREATE TABLE USERS (
             ACCOUNT_NUMBER  CHAR(20) PRIMARY KEY,
             PASSWORD  CHAR(20) NOT NULL,
             ID  CHAR(10) NOT NULL,
             NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1) )"""
Mistaken_questions = """CREATE TABLE MISTAKEN_QUESTIONS (
             TITLE_NUMBER INT PRIMARY KEY,
             QUESTION_TYPE  CHAR(50) NOT NULL,
             TOTAL_SCORE  INT NOT NULL,
             SCORE INT NOT NULL )"""
TablesN = ["problem", "users", "mistaken_questions"]  # 表名的list
Tables = [problem, users, Mistaken_questions]  # 创建表sql语句的list
ConnectDatabase = pm.connect(host='localhost', user='root', passwd='123456', charset='utf8')  # 连接数据库
GetCursor = ConnectDatabase.cursor()  # 获取光标


def detection_db(database_name):  # 检测数据库是否存在的函数
    GetCursor.execute(show_db_sql)  # 显示所有数据库
    dbs = [GetCursor.fetchall()]  # 将所有数据库名称导出
    db_list = re.findall('(\'.*?\')', str(dbs))  # 使用正则表达式分割出数据库名称
    db_list = [re.sub("'", '', each) for each in db_list]  # 使用正则表达式去掉引号
    if database_name in db_list:  # 判断传入的数据库名称是否已存在，存在返回1，不存在返回0
        return 1
    else:
        return 0


def detection_table(table_name):  # 检测表是否存在的函数
    GetCursor.execute(show_table_sql)  # 显示所有表
    tables = [GetCursor.fetchall()]  # 将所有表名称导出
    table_list = re.findall('(\'.*?\')', str(tables))  # 使用正则表达式分割出表名称
    table_list = [re.sub("'", '', each) for each in table_list]  # 使用正则表达式去掉引号
    if table_name in table_list:  # 判断传入的表名称是否已存在，存在返回1，不存在返回0
        return 1
    else:
        return 0


def find_table():  # 查看数据库是否存在某表，存在返回表名，不存在则重新输入
    while True:
        GetCursor.execute(show_table_sql)  # 显示所有表
        tables = [GetCursor.fetchall()]  # 将所有表名称导出
        table_list = re.findall('(\'.*?\')', str(tables))  # 使用正则表达式分割出表名称
        table_list = [re.sub("'", '', each) for each in table_list]  # 使用正则表达式去掉引号
        for TN in table_list:  # 循环显示表名
            print(TN)
        table_name = input("请选择的表名：")  # 输入表名
        if table_name in table_list:  # 判断输入的表名称是否已存在，存在返回表名，不存在重新选择
            return table_name
        else:
            print("请重新选择：")


def find_attribute(table_name):  # 查看表table_name的全部字段，将字段名存在temp_attribute
    show_field_sql = "SHOW COLUMNS FROM " + table_name + " FROM " + db_name + ";"  # 显示db_name.table_name中所有字段的sql语句
    GetCursor.execute(show_field_sql)  # 显示db_name.table_name中所有字段
    table_field = [GetCursor.fetchall()]  # 将所有字段信息导出
    temp_list = re.findall('(\'.*?\')', str(table_field))  # 使用正则表达式分割出表名称
    temp_list = [re.sub("'", '', each) for each in temp_list]  # 使用正则表达式去掉引号
    attribute = []  # 创建一个临时存储字段名的list
    for AN in range(int(len(temp_list) / 5)):  # 通过验证知道temp_list中每五个数据表示一个字段的信息，并在第一个存储字段名
        attribute.append(temp_list[AN * 5])  # 将字段名添加至attribute
    return attribute


def add():  # 添加函数1.0
    print("请从以下表中选择添加数据的表：")
    table_name = find_table()  # 调用find_table()函数选择并返回添加数据的表名table_name
    attribute = find_attribute(table_name)  # 调用find_attribute(table_name)函数返回表table_name的字段名list
    attributes = ""  # 创建一个存储字段名的字符串
    for AN in range(len(attribute)):  # 通过循环将字段名以“字段名，字段名，……”的形式连接起来
        if 0 != AN:  # 判断是否的第一个，第一个前面不加“,”
            attributes += ","
        attributes += attribute[AN]  # 添加
    temp = ""  # 创建一个存储字段对应%s的字符串
    for i in range(len(attribute)):  # 通过循环将%s以“%s，%s，……”的形式连接起来
        if 0 != i:  # 判断是否的第一个，第一个前面不加“,”
            temp += ","
        temp += "%s"  # 添加
    while True:  # 循环输入添加信息
        insert_sql = "INSERT INTO " + table_name + "(" + attributes + ") VALUES (" + temp + ");"  # 添加数据的sql语句
        temp_data = []
        for AN in range(len(attribute)):
            print("请输入%s：" % (attribute[AN]))
            temp = input("")
            temp_data.append(temp)
        try:
            GetCursor.execute(insert_sql, temp_data)
            ConnectDatabase.commit()
            print('添加成功！')
            break
        except Exception as e:
            print('出错回滚完成', e)
            ConnectDatabase.rollback()
            GetCursor.close()
            ConnectDatabase.close()


# 删除函数
def delete():
    print("请从以下表中选择删除数据的表：")
    table_name = find_table()
    print("请从以下属性中选择：")
    attribute = find_attribute(table_name)
    for A in attribute:
        print(A)
    select_attribute = input("请选择属性：")
    attribute_value = input("请选择属性值：")
    sql_delete = "DELETE FROM " + table_name + " where " + select_attribute + "='" + attribute_value + "'"
    GetCursor.execute(sql_delete)


# 查询函数
def lookup():
    print("请从以下表中选择查看数据的表：")
    TableName = find_table()
    sql_select = "SELECT * FROM " + TableName
    Attribute = find_attribute(TableName)
    num = GetCursor.execute(sql_select)
    data_all = GetCursor.fetchall()
    for i in range(num + 1):
        for j in range(len(Attribute)):
            if 0 == i:
                print(Attribute[j], end=" ")
            else:
                print(data_all[i - 1][j], end=" ")


# 更改函数
def change():
    print("请从以下表中选择修改数据的表：")
    TableName = find_table()
    print("请从以下属性中选择：")
    Attribute = find_attribute(TableName)
    for i in Attribute:
        print(i)
    while True:
        LookupSelAttribute = input("请选择查找属性：")
        LookupAttributeValue = input("请选择查找属性值：")
        sql_Lookup = "SELECT * FROM " + TableName + " WHERE " + LookupSelAttribute + "='" + LookupAttributeValue + "'"
        if 0 == GetCursor.execute(sql_Lookup):
            print("没有该字段！请重新输入")
            continue
        else:
            break
    ModSelAttribute = input("请选择修改属性：")
    ModAttributeValue = input("请选择修改属性值：")
    sql_update = "UPDATE " + TableName + " SET " + ModSelAttribute + "=" + ModAttributeValue + " WHERE " + LookupSelAttribute + "='" + LookupAttributeValue + "'"
    GetCursor.execute(sql_update)


if detection_db(db_name) != 1:  # 判断RecommenderSystem_db数据库是否存在,不存在就创建
    print("数据库不存在，创建！")
    GetCursor.execute(create_db_sql)  # 创建数据库
    print("创建成功！")
else:
    print(db_name, "数据库已存在！")
GetCursor.execute(select_db_sql)  # 选择数据库
for i in range(len(Tables)):  # 循环遍历每个表
    if detection_table(TablesN[i]) != 1:  # 判断表是否存在,不存在就创建
        print("表不存在，创建！")
        GetCursor.execute(Tables[i])  # 创建表
        print("创建成功！")
    else:
        print(TablesN[i], "表已存在！")
#发现django架构自带数据库操作，放弃2.0版本
sql = "show tables;"
GetCursor.execute(sql)
tables = [GetCursor.fetchall()]
table_list = re.findall('(\'.*?\')', str(tables))
table_list = [re.sub("'", '', each) for each in table_list]
for i in table_list:
    delsql="DROP TABLE "+i
    GetCursor.execute(delsql)
delsql="DROP DATABASE "+db_name
GetCursor.execute(delsql)