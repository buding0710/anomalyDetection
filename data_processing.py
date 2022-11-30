#从excel/txt/csv/database里获取数据
import configparser
import datetime
import json
import os
import pandas as pd
import pymysql
from anomalyDetection.find_anomaly import *
from sqlalchemy import create_engine


class DataProcessing():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        self.type = config.get("DataType",'type')
        self.path = config.items('DataPath')
        self.method = config.get('AnomalyMethod','method')
        self.methods = eval(self.method)

    def processing_for_dataframe(self):
        filepath = os.getcwd() +'\\'+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +'.txt'
        for i in range(len(self.methods)):
            method = self.methods[i].split(':')[0]
            param = self.methods[i].split(':')[1]
            if param == "":
                re = eval(method)(self.data)
                with open(filepath, 'a') as file:
                    file.write(method+str(re)+'\n')
            else:
                tup = eval(param)#把带小括号的字符串转换为元组
                re = eval(method)(self.data,*tup)
                with open(filepath, 'a') as file:
                    file.write(method+str(re)+'\n')

    def data_transfor_dataframe(self):
        for i in self.path:
            if 'txt' in i[0]:
                self.data = pd.read_csv(i[1], encoding='utf-8', sep=',', header=None)
                self.processing_for_dataframe()
            elif 'csv' in i[0]:
                self.data = pd.read_csv(i[1], encoding='utf-8', header=None)
                self.processing_for_dataframe()
            elif 'xls' in i[0]:
                self.data = pd.read_excel(i[1],header=None)
                self.processing_for_dataframe()
            elif 'mysql' in i[0]:
                parm = eval(i[1])
                # engine = create_engine("mysql+pymysql://%s:%s@%s/%s?charset=utf8', echo=True" %(parm[1].split(':')[1],parm[2].split(':')[1],parm[0].split(':')[1],parm[3].split(':')[1]))
                # engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset=utf8', echo=True".format(parm[1].split(':')[1],parm[2].split(':')[1],parm[0].split(':')[1],parm[3].split(':')[1]))
                # print(engine)
                # temp_sql = "select * from " + parm[4].split(':')[1] + ";"
                # conn = engine.connect()
                # self.data = pd.read_sql(sql=temp_sql, con=conn)
                # conn.close()
                # engine.dispose()

                conn = pymysql.connect(host=parm[0].split(':')[1],user=parm[1].split(':')[1],password=parm[2].split(':')[1],db=parm[3].split(':')[1])
                temp_sql = "select * from " + parm[4].split(':')[1] + ";"
                self.data = pd.read_sql(sql=temp_sql,con=conn)
                conn.close()
                self.processing_for_dataframe()
            # elif 'db2' in i[0]:
            #     parm = eval(i[1])
            #     conn = ibm_db.connect(database="MICRO_11",hostname="localhost",port=50000,protocol="tcpip",uid="administrator",pwd="wyz","", "")
            #     temp_sql = "select * from" + parm[4].split(':')[1] + ";"
            #     self.data = pd.read_sql(sql=temp_sql, con=conn)
            #     conn.close()
            #     self.processing_for_dataframe()
            # elif 'gassDB' in i[0]:
            #     parm = eval(i[1])
            #     conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port,)
            #     temp_sql = "select * from" + parm[4].split(':')[1] + ";"
            #     self.data = pd.read_sql(sql=temp_sql, con=conn)
            #     conn.close()
            #     self.processing_for_dataframe()



if __name__ == '__main__':
    DataProcessing().data_transfor_dataframe()