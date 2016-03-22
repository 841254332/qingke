# coding=utf-8
import os

__author__ = 'cao'

import pandas as pd
import sys
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn import metrics

'''

    数据的维数为(1952, 24)
    使用决策树分类模型

'''

reload(sys)
sys.setdefaultencoding('utf-8')

DATA_PATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'data')
INVESTOR_PATH = os.path.join(DATA_PATH, 'data_investor_feature.csv')
# feature_cols = ['领域数量', '投资次数', '上市率', '投资总额', '所投企业平均年龄', '所投企业后续获得平均投资轮数', '金融占比',
#                 '旅游占比', '硬件占比', '汽车交通占比', '企业服务占比', '本地生活占比', '电子商务占比', '教育占比', '广告营销占比',
#                 '游戏占比', '文化娱乐体育占比', '医疗健康占比', '房产服务占比', 'SNS社交网络占比', '移动互联网占比', '工具软件占比',
#                 '未知领域占比']
feature_cols = ['领域数量', '投资次数', '投资总额', '金融占比', '旅游占比', '硬件占比', '汽车交通占比', '企业服务占比',
                '本地生活占比', '电子商务占比', '教育占比', '广告营销占比', '游戏占比', '文化娱乐体育占比', '医疗健康占比',
                '房产服务占比', 'SNS社交网络占比', '移动互联网占比', '工具软件占比','未知领域占比']


def read_data():
    df = pd.read_csv('data\\data_feature_final_cluster.csv')
    print 'the shape of data is ',
    print df.shape
    return df


df = read_data()


def get_y():
    y = df['聚类结果']
    return y


def get_X():
    X = df[feature_cols]
    return X


def tree_classify():
    X = get_X()
    y = get_y()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    print X_train.shape  # default split is 75% for training ang 25% for testing
    print X_test.shape
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(X_train, y_train)
    # make predictions on the test set
    y_pred = clf.predict(X_test)
    print metrics.accuracy_score(y_test, y_pred)
    # from sklearn.externals.six import StringIO
    with open("vc2startup.dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)

tree_classify()
