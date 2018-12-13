import pymysql
pymysql.install_as_MySQLdb()

'''
在 python2 中，使用 pip install mysql-python 进行安装连接MySQL的库，使用时 import MySQLdb 进行使用

在 python3 中，改变了连接库，改为了 pymysql 库，使用pip install pymysql 进行安装，直接导入import pymysql使用

本来在上面的基础上把 python3 的 pymysql 库安装上去就行了，但是问题依旧

经过查阅得知， Django 依旧是使用 py2 的 MySQLdb 库的，得到进行适当的转换才行

在__init__.py 文件中添加以下代码

import pymysql
pymysql.install_as_MySQLdb()


'''