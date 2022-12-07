# anomalyDetection
数据异常检测工具

    检查给定的数据里是否存在异常数据，提供以下检测方法：
    1、找空值，find_NaN：nan,null,NA,NaN,""这五种空值会被找到，面向全表
    2、列值判断，不忽略大小写，假设某列的值来源于若干值中的一个，把源值当成一个列表入参
    3、范围判断，range_judge(columnIndex,floor,ceiling)根据业务规则的上下限，找出大于上限或低于下限的异常值，针对某列数值，自定义上下限
    4、正则表达式匹配，regular_expression(columnIndex,pattern):#指定某列要符合正则表达式的匹配，自定义正则表达式
    5、重复行，duplicate_row(subset):#查找行重复数据，可以指定整行subset=None,多列subset=[0,1],单列subset=[1]
    6、关联判断，relation_judge(result_column,judge_column,condition,judge_value,true_value,false_value):#关联列判断，两列存在关联关系，判断列和结果列可以互换位置,目前仅支持单条件判断，如"relation_judge": "(12,10,>=,1,正,负)"
    7、正态分布，normal_distribution_3(columnName):#当数据服从正态分布：距离平均值大于3δ，则认定该样本为异常值。
    8、箱型法，box_figure(columnName):#大于或小于箱型图设定的上下界的数值即为异常值,上下四分位/上下界为动态设定
    9、动态阈值-移动平均法，moving_averages(columnName,n):#异常数据识别：确定固定移动窗口n，以过去n个窗口的指标平均值作为下一个窗口的预测值；以过去n个窗口的指标的平均值加减3倍方差作为监控的上下界。
    
    注：duplicate_row,normal_distribution_3,box_figure,moving_averages以上方法只能传递列名；其余方法传递列索引
    以上方法支持部分选用。





