# -*- coding: utf-8 -*-
__author__ = 'admin'
import MySQLdb


class Manager:
    manager_name = ''
    position = ''
    location = ''
    work_company = ''
    education = ''

    def show(self):
        print self.manager_name, self.position, self.location, self.work_company, self.education

    def __init__(self, manager_name, position, location, work_company, education):
        self.manager_name = manager_name
        self.work_company = work_company
        self.location = location
        self.education = education
        self.position = position


class Project:
    project_name = ''
    company_name = ''
    registration_time = ''
    registration_amount = ''
    location = ''
    project_stage = ''
    area = ''
    sub_area = ''
    manager_team = ''

    def show(self):
        print self.project_name, self.company_name, self.registration_time, self.registration_amount, self.location,\
            self.project_stage, self.area, self.sub_area, self.manager_team

    def __init__(self, project_name, company_name, registration_time, registration_amount, location, project_stage, area, sub_area, manager_team):
        self.project_name = project_name
        self.company_name = company_name
        self.registration_time = registration_time
        self.registration_amount = registration_amount
        self.location = location
        self.project_stage = project_stage
        self.area = area
        self.sub_area = sub_area
        self.manager_team = manager_team


class Firm:
    firm_name = ''

    def __init__(self, firm_name):
        self.firm_name = firm_name


def get_data_from_db(sql):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='lapose', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
    except MySQLdb.Error, e:
        print "MySql Error %d: %s" % (e.args[0], e.args[1])

sql = "select * FROM project_feature"
project_feature_table = get_data_from_db(sql)
features = []
for project_feature in project_feature_table:
    project_name = project_feature[0]
    company_name = project_feature[1]
    registration_time = project_feature[2]
    registration_amount = project_feature[3]
    location = project_feature[4]
    features.append(location)
    project_stage = project_feature[5]
    area = project_feature[6]
    sub_area = project_feature[7]
    manager_team = project_feature[8]
    project = Project(project_name, company_name, registration_time, registration_amount, location, project_stage, area, sub_area, manager_team)
    project.show()
    manager_list = manager_team.replace(' ', '').split(',')
    for manager in manager_list:
        manager_feature_table = get_data_from_db('select * from manager_feature where manager_name = \'' + manager + '\'')
        for manager_feature in manager_feature_table:
            manager_name = manager_feature[0]
            position = manager_feature[1]
            features.append(position)
            location = manager_feature[2]
            work_company = manager_feature[3]
            features.append(work_company)
            education = manager_feature[4]
            features.append(education)
            manager_feature = Manager(manager_name, position, location, work_company, education)
            manager_feature.show()
all_time = open("feature_set\\all_time.txt")
all_value = open("feature_set\\all_value.txt")
time_without1 = open("feature_set\\time_without1.txt")
value_without1 = open("feature_set\\value_without1.txt")
all_feature = open("feature_set\\feature_noRepeat\\all_feature_utf8.txt")
all_feature_list = []
vector = []
lines = all_feature.readlines()
for line in lines:
    all_feature_list.append(line[:-1])
print all_feature_list.__len__()
for i in range(0, all_feature_list.__len__()):
    vector.append(0)
    if all_feature_list[i].decode('utf-8') in features:
        print all_feature_list[i]
        vector[i] = 1
        print i
print vector


