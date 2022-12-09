import math
import re

import pandas
from scipy.stats import kstest
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import pandas as pd
from numpy import std, mean


def find_NaN(data):#找空值nan,null,NA,NaN,""，面向全表
    # 查看哪些值缺失
    li = []
    valueLis = []
    for i in range(data.shape[1]):#列循环
        for j in range(data.shape[0]):#行循环
            value = data.iloc[j,i]
            if pd.isna(value):
                tmp = (j,i)
                li.append(tmp)
                valueLis.append(value)
    return set(valueLis),li

def value_judge(data,column_name,lis):#列值判断，不忽略大小写，假设某列的值来源于若干值中的一个，把源值当成一个列表入参
    temp = []
    result = []
    iterable = set(data[column_name])
    for i in iterable:
        if i not in lis:
            temp.append(i)
    for j in temp:
        row = data[data.values == j].index.tolist()
        ind = data.columns.get_indexer([column_name,]).tolist()[0]
        items = [ind for k in range(len(row))]
        result += list(zip(row, items))
    return set(temp),list(set(result))

def range_judge(data,column,floor,ceiling):#根据业务规则的上下限，找出大于上限或低于下限的异常值，针对某列数值
    temp = []
    result = []
    iterable = set(data.iloc[:,column])
    for i in iterable:
        if float(i) < float(floor) or float(i) > float(ceiling):
            temp.append(i)
    for j in temp:
        row = data[data.values == j].index.tolist()
        items = [column for k in range(len(row))]
        result += list(zip(row, items))
    return set(temp),list(set(result))

def regular_expression(data,column,pattern):#指定某列要符合正则表达式的匹配
    # print(pattern)
    temp = []
    result = []
    iterable = set(data.iloc[:, column])
    for i in iterable:
        res = re.match(pattern,i)
        if res == None:
            temp.append(i)
    for j in temp:
        row = data[data.values == j].index.tolist()
        items = [column for k in range(len(row))]
        result += list(zip(row, items))
    return set(temp),list(set(result))

def duplicate_row(data,subset):#查找行重复数据，整行subset=None,多列subset=[0,1],单列subset=[1]
    re = data.duplicated(subset=subset,keep='last')
    row = re[re.values == True].index.tolist()
    valueLis = list(map(lambda x: np.array(data.iloc[x]).tolist(), row))
    if subset == None:
        return valueLis, row
    else:
        ind = data.columns.get_indexer(subset).tolist()
        items = [ind for k in range(len(row))]
        li = list(zip(row,items))
        return valueLis,li

def relation_judge(data,result_column,judge_column,condition,judge_value,true_value,false_value):#关联列判断，两列存在关联关系,目前仅支持单条件判断，"relation_judge": "(12,10,>=,1,正,负)"
    li = []
    valueLis = []
    conditions = 'data.iloc[:,judge_column].astype(float)' + condition + 'judge_value'
    judge = np.where(eval(conditions), true_value, false_value)
    for i in range(judge.size):
        if data.iloc[i,result_column] != judge[i]:
            tmp = (i,result_column)
            valueLis.append(data.iloc[i,result_column])
            li.append(tmp)
    return set(valueLis),li

def normal_distribution_3(data,column_name):#当数据服从正态分布：距离平均值大于3δ，则认定该样本为异常值。
# 也叫拉依达准则（3σ准则），对于大于μ+3σ或小于μ-3σ的实验数据，视为异常数据。
# 假定p<=0.05 则服从正态分布，否则不服从。
    li = []
    values = []
    dt = data[column_name].astype(float)
    # 计算均值
    data_mean = mean(dt)
    # 计算标准差
    standard = std(dt)
    # 计算P值
    p = kstest(dt, 'norm', (data_mean, standard))[1]
    # 判断p值是否服从正态分布，p<=0.05 则服从正态分布，否则不服从。
    if p<=0.05:
        print('该列数据服从正态分布p=%s------------' % p)
        print('均值为：%.3f，标准差为：%.3f' % (data_mean, standard))
        print('------------------------------')
        lower_limit = data_mean - standard * 3
        upper_limit = data_mean + standard * 3
        # print(lower_limit,upper_limit)
        for outlier in dt:
            if outlier > upper_limit or outlier < lower_limit:
                row = data[dt.values == outlier].index.tolist()
                ind = data.columns.get_indexer([column_name, ]).tolist()[0]
                tmp = (row[0], ind)
                values.append(outlier)
                li.append(tmp)
        return set(values), li
    else:
        print('该列数据不服从正态分布p=%s------------' % p)
        print('------------------------------')
        return 0

def box_figure(data,column_name):#箱形图（英文：Box plot），又称为盒须图、盒式图、盒状图或箱线图，是一种用作显示一组数据分散情况资料的统计图
    # 大于或小于箱型图设定的上下界的数值即为异常值,上下四分位/上下界为动态设定；上限=Q3+1.5IQR，下限=Q1-1.5IQR
    # 上四分位数Q1=前一项小数占比×前一项+后一项小数占比×后一项；#下四分位数Q3=前一项小数占比×前一项+后一项小数占比×后一项；四分位距IQR=Q3-Q1
    li = []
    valueLis = []
    dt = data[column_name].astype(float)
    sort = dt.sort_values(ascending=True)#升序排列
    # li_s = list(sort)
    des = sort.describe()
    Q1 = des.loc['25%']#上四分位的值
    Q3 = des.loc['75%']#下四分位的值
    # print(Q1,Q3)
    # # 上四分位位置
    # upper_quartile = len(dt) * 0.25
    # # 下四分位位置
    # lower_quartile = len(dt) * 0.75
    # #获取小数部分
    # uq_dec = upper_quartile - math.floor(upper_quartile)
    # lq_dec = lower_quartile - math.floor(lower_quartile)
    # Q1 = uq_dec * li_s[math.floor(upper_quartile) - 1] + (1 - uq_dec) * li_s[math.ceil(upper_quartile) - 1]  # 上四分位数Q3=前一项小数占比×前一项+后一项小数占比×后一项
    # Q3 = lq_dec * li_s[math.floor(lower_quartile) - 1] + (1 - lq_dec) * li_s[math.ceil(lower_quartile) - 1]#下四分位数Q3=前一项小数占比×前一项+后一项小数占比×后一项；
    IQR = Q3 - Q1
    for i in range(len(dt)):
        #上界为Q3+1.5*IQR，下界为Q1-1.5*IQR
        if dt[i] > Q3+1.5*IQR or dt[i] < Q1-1.5*IQR:
            ind = data.columns.get_indexer([column_name, ]).tolist()[0]
            tmp = (i, ind)
            valueLis.append(dt[i])
            li.append(tmp)
    return set(valueLis),li

def moving_averages(data,column_name,n):#动态阈值-移动平均法
    #异常数据识别：确定固定移动窗口n，以过去n个窗口的指标平均值作为下一个窗口的预测值；以过去n个窗口的指标的平均值加减3倍方差作为监控的上下界。
    #统计中的方差（样本方差）是各个样本数据和平均数之差的 平方和 的平均数的开方
    #使用范围：数据无周期性，数据比较平稳。
    li = []
    valueLis = []
    dt = data[column_name].astype(float)
    for i in range(n,len(dt)):#从第n位开始预测
        su = 0
        sumOfSquares = 0
        # 平均值
        for j in range(i-n,i):#计算前面n位的和
            su += dt[j]
        average = su / n
        # 方差
        for k in range(i-n,i):# 计算前面n位的平方和
            da = dt[k] - average
            sumOfSquares += math.pow(da, 2)
        variance = math.sqrt(sumOfSquares / n)
        # 比较
        #上界(average + 3 * variance),下界(average - 3 * variance)
        if dt[i] > (average + 3 * variance) or dt[i] < (average - 3 * variance):
            ind = data.columns.get_indexer([column_name, ]).tolist()[0]
            tmp = (i, ind)
            valueLis.append(dt[i])
            li.append(tmp)
    return set(valueLis),li


if __name__ == '__main__':
    dt = pd.read_csv('data1.txt', encoding='utf-8', sep=',', header=None)
    # relation_judge(dt,12,10,'>=',1,'正','负')
    # print(duplicate_row(dt,None))
    # range_judge(dt,1,-10,500)
    # value_judge(dt,12,['男','女','其他','man','woman','1','0'])
    # duplicate_row(dt,[5],)
    print(normal_distribution_3(dt,9,))
    # print(box_figure(dt,10,))
    # print(moving_averages(dt,11,3))
