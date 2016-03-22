# -*- coding: utf-8 -*-
import os
import pandas as pd
import sys
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn import svm
from sklearn import metrics

'''

    数据的维数为(1952, 24)
    使用决策树分类模型

'''

reload(sys)
sys.setdefaultencoding('utf-8')
feature_cols = ['所投公司存活时间', '所投公司创业人数', '所投公司管理层毕业于世界500强大学占比', '所投公司在一线城市占比',
                '所投公司在二线城市占比', '金融占比', '旅游占比', '硬件占比', '汽车交通占比', '企业服务占比', '本地生活占比',
                '电子商务占比', '教育占比', '广告营销占比', '游戏占比', '文化娱乐体育占比', '医疗健康占比', '房产服务占比',
                'SNS社交网络占比', '移动互联网占比', '工具软件占比', '未知领域占比']


def read_data():
    path_1 = 'data\\data_0101_cluster.csv'
    path_2 = 'data\\data_feature_final_cluster.csv'
    df = pd.read_csv(path_1)
    print 'data:',
    print df.shape
    return df


df = read_data()


def get_y():
    y = df['聚类结果']
    return y


def get_x():
    x = df[feature_cols]
    return x


def tree_classify():
    x = get_x()
    y = get_y()
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    print 'train_set:', x_train.shape
    print 'test_set:', x_test.shape
    # clf = svm.SVC()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    accuracy_score = metrics.accuracy_score(y_pred, y_test)
    print accuracy_score
    # with open("test1.dot", 'w') as f:
    #     tree.export_graphviz(clf, out_file=f)
    vector = ()
tree_classify()

