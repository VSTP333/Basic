#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: mysql.py
@time: 2019-05-09 11:39:44
@desc:操作mysql数据库,提供增删改查方法
'''

from Tools.config import ConFig
import pymysql

class MySql(object):
    "MYSQL数据库操作"

    def __init__(self,envi="pre",port="3306",db="GCMS"):
        if envi=="pre":
            if db=="GCMS":
                self.host = ConFig.DataBasepre.host
                self.username = ConFig.DataBasepre.user
                self.password = ConFig.DataBasepre.passwd
                self.dbName = ConFig.DataBasepre.db
            elif db=="GCBI":
                self.host = ConFig.GCBI_pre.host
                self.username = ConFig.GCBI_pre.user
                self.password = ConFig.GCBI_pre.passwd
                self.dbName = ConFig.GCBI_pre.db
        elif envi=="sit":
            self.host = ConFig.DataBasesit.host
            self.username = ConFig.DataBasesit.user
            self.password = ConFig.DataBasesit.passwd
            self.dbName = ConFig.DataBasesit.db
        elif envi=="xgpre":
            self.host = ConFig.DataBasexgpre.host
            self.username = ConFig.DataBasexgpre.user
            self.password = ConFig.DataBasexgpre.passwd
            self.dbName = ConFig.DataBasexgpre.db
        self.port = port

    def __connectSql(self,act,sqls):
        "连接数据库并对数据库进行操作"
        try:
            db = pymysql.connect(self.host,self.username,self.password,self.dbName)
            cursor = db.cursor()  #创建游标
            cursor.execute(sqls)
            if act == 'search':
                data = cursor.fetchall()
                return data
            else:
                db.commit()
        except Exception as e:
            return e
        db.close()
        return None

    def searchs(self,sqls):
        """
        查询数据库操作
        :param sqls: sql语句
        :return: 返回查询结果
        """
        result = self.__connectSql("search",sqls)
        return result

    def updates(self,sqls):
        """
        更新数据库操作
        :param sqls: sql语句
        :return: 返回None
        """
        print(sqls)
        result = self.__connectSql("update", sqls)
        return result

    def inserts(self,sqls):
        """
        更新数据库操作
        :param sqls: sql语句
        :return: 返回None
        """
        print(sqls)
        result = self.__connectSql("insert", sqls)
        return result

    def deletes(self,sqls):
        """
        删除数据库操作
        :param sqls: sql语句
        :return: 返回None
        """
        result = self.__connectSql("delete", sqls)
        return result