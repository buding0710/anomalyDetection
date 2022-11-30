import math
import re
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import pandas as pd
from numpy import std, mean


def find_NaN(data):#找空值nan,null,NA,NaN,""，面向全表
    li = []
    # 查看哪些值缺失
    for i in range(data.shape[1]):#列循环
        for j in range(data.shape[0]):#行循环
            value = data.iloc[j,i]
            if pd.isna(value):
                tmp = (j,i)
                li.append(tmp)
    return li

def range_judge(data,column,floor,ceiling):#根据业务规则的上下限，找出大于上限或低于下限的异常值，针对某列数值
    li = []
    for j in range(data.shape[0]):#行循环
        value = float(data.iloc[j,int(column)])
        if value >= float(floor) and value <= float(ceiling):
            continue
        else:
            tmp = (j, column)
            li.append(tmp)
    return li

def regular_expression(data,column,pattern):#指定某列要符合正则表达式的匹配
    # print(pattern)
    li = []
    for j in range(data.shape[0]):#行循环
        value = data.iloc[j,column]
        if str(value) == 'nan':
            tmp = (j, column)
            li.append(tmp)
        else:
            res = re.match(pattern,value)
            if res == None:
                tmp = (j, column)
                li.append(tmp)
    return li

def duplicate_row(data,subset):#查找行重复数据，整行subset=None,多列subset=[0,1],单列subset=[1]
    re = data.duplicated(subset=subset,keep=False)
    row = re[re.values == True].index.tolist()
    column = [subset for i in range(len(row))]
    li = list(zip(row,column))
    return li

def relation_judge(data,result_column,judge_column,condition,judge_value,true_value,false_value):#关联列判断，两列存在关联关系，判断列和结果列可以互换位置
    #目前仅支持单条件判断，"relation_judge": "(12,10,>=,1,正,负)"
    li = []
    conditions = 'data.iloc[:,judge_column].astype(float)' + condition + 'judge_value'
    # conditions = '%s %s %s' %(data.iloc[:,judge_column].astype(float),condition,judge_value)
    judge = np.where(eval(conditions), true_value, false_value)
    for i in range(judge.size):
        if data.iloc[i,result_column] != judge[i]:
            tmp = (i,result_column)
            li.append(tmp)
    return li

def normal_distribution_3(data,column):#当数据服从正态分布：距离平均值大于3δ，则认定该样本为异常值。
# 也叫拉依达准则（3σ准则），适用于n>185时的样本判定，对于大于μ+3σ或小于μ-3σ的实验数据，视为异常数据，予以剔除。
# 剔除后，对余下的各测量值重新计算偏差和标准偏差，并继续审查，直到各个偏差均小于3σ为止。
    li = []
    dt = data[column].astype(float)
    standard = std(dt)
    data_mean = mean(dt)
    lower_limit = data_mean - standard * 3
    upper_limit = data_mean + standard * 3
    # print(lower_limit,upper_limit)
    for outlier in dt:
        if outlier > upper_limit or outlier < lower_limit:
            row = data[dt.values==outlier].index.tolist()
            tmp = (row[0],column)
            li.append(tmp)
    return li

def box_figure(data,column):#大于或小于箱型图设定的上下界的数值即为异常值,上下四分位/上下界为动态设定
    li = []
    dt = data[column].astype(float)
    #上四分位
    upper_quartile = math.ceil(len(dt)*0.25)
    #下四分位
    lower_quartile = math.floor(len(dt)*0.75)
    sort = dt.sort_values(ascending=False)
    li_s = list(sort)
    u = li_s[upper_quartile-1]
    if len(dt)%2 == 0:
        l = li_s[lower_quartile-1]
    else:
        l = li_s[lower_quartile]
    for i in range(len(dt)):
        #上界为u+1.5(u-l)，下界为l-1.5(u-l)
        if dt[i] > u+1.5*(u-l) or dt[i] < l-1.5*(u-l):
            tmp = (i, column)
            li.append(tmp)
    return li

def moving_averages(data,column):#动态阈值-移动平均法
    #异常数据识别：确定固定移动窗口n，以过去n个窗口的指标平均值作为下一个窗口的预测值；以过去n个窗口的指标的平均值加减3倍方差作为监控的上下界。
    #使用范围：数据无周期性，数据比较平稳。
    #统计中的方差（样本方差）是各个样本数据和平均数之差的 平方和 的平均数
    # 平均值
    li = []
    su = 0
    dt = data[column].astype(float)
    for i in range(1,len(dt)):#从第二位开始
        su += dt[i-1]
        average = su/i
        # 方差
        sumOfSquares = 0
        variance = 0
        for j in range(0,i):
            da = dt[j] - average
            if da < 0:#这里判断正负的原因为，python会将负数的平方变成正数，因此只能对负数进行平方后再取反
                sumOfSquares += -math.pow(da, 2)
            else:
                sumOfSquares += math.pow(da, 2)
            variance = sumOfSquares / i
        # 比较
        #上界(average + 3 * variance),下界(average - 3 * variance)
        # print(data[column][i],average + 3 * variance,average - 3 * variance)
        if dt[i] > average + 3 * variance or dt[i] < average - 3 * variance:
            tmp = (i, column)
            li.append(tmp)
    return li

if __name__ == '__main__':
    dt = pd.read_csv(r'C:\Users\budin\Desktop\data1.txt', encoding='utf-8', sep=',', header=None)
    # relation_judge(dt,12,10,'>=,'1','正','负')
    # print(duplicate_row(dt,None))
    moving_averages(dt,11)