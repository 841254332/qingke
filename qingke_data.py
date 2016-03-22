# -*- coding: utf-8 -*-
__author__ = 'admin'
import urllib2
import re
import time
import random
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()


def fetch(url):
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'Referer': 'http://zdb.pedaily.cn/',
        'Host': 'zdb.pedaily.cn',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Cookie': 'Hm_lvt_25919c38fb62b67cfb40d17ce3348508=1449131967; Hm_lpvt_25919c38fb62b67cfb40d17ce3348508=1449134904; __fromtype=1; __uid=1155040104; __utma=23980325.1166461789.1449131967.1449131967.1449134872.2; __utmc=23980325; __utmz=23980325.1449134872.2.2.utmcsr=pedaily.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; BAIDU_DUP_lcr=http://www.baidu.com/link?url=vix7CcbOweuIVbicWsHppHjNfkdZfLHjvtYuc0Q95sa&wd=&eqid=c0beead40000e5e800000003565fff96; __utmb=23980325.2.10.1449134872; __utmt=1'
    }
    request = urllib2.Request(url, headers=HEADER)
    src = ''
    count = 0
    while 5 > count:
        try:
            count = count + 1
            src = urllib2.urlopen(request, data=None, timeout=5).read()
            break;
        except:
            print '[Error]:', url.decode('gbk').encode('utf-8')
    return src.replace('\r', '').replace('\n', '')


def _filter_html_tag(src):
    regex = '<.*?>'
    res_list = re.findall(regex, src)
    for res in res_list:
        src = src.replace(res, '')
    regex = '&.*?;'
    res_list = re.findall(regex, src)
    for res in res_list:
        src = src.replace(res, '')
    return str(src)


def fetch_firm_link(page):
    url = 'http://zdb.pedaily.cn/company/all/' + str(page)
    src = fetch(url)
    src = str(src).replace('\r\n', '').strip()
    regex = '<div class="company-list">(.*?)</ul>'
    pattern = re.compile(regex)
    firm_list = []
    html = pattern.search(src)
    if html:
        src = html.group()
        regex = 'alt=".*?"/>'
        pattern = re.compile(regex)
        html = pattern.findall(src)
        for firm in html:
            firm_list.append(firm.replace('alt="', '').replace('"/>', ''))
            print(firm.replace('alt="', '').replace('"/>', ''))
    return firm_list


def fetch_company_link(page):
    url = 'http://zdb.pedaily.cn/enterprise/' + str(page)
    src = fetch(url)
    regex = '<div class="company-list">.*?</ul>'
    html = re.search(regex, src)
    company_list = []
    if html:
        html = html.group()
        regex = 'alt=".*?"/>'
        html = re.findall(regex, html)
        for company in html:
            company_list.append(company.replace('alt="', '').replace('"/>', ''))
    return company_list


def fetch_firm_team(src):
    team = []
    regex = '<ul class="list-pics">.*?</ul>'
    pattern = re.compile(regex)
    result = pattern.search(src)
    if result:
        result = result.group().replace('\t', '')
        regex = '<li>.*?</li>'
        manager_list = re.findall(regex, result)
        for manager in manager_list:
            investor = _filter_html_tag(manager)
            investor = investor[:-1]
            team.append(investor)
    return team


def fetch_investor_info(src):
    name = position = label = carrer = intro = ''
    regex = '<!--content-start-->.*?<div class=\"box-content\">'
    html = re.search(regex, src)
    if html:
        result = html.group()
        regex = '<h1>.*?</h1>'
        name = re.search(regex, result)
        if name:
            name = name.group()
            name = _filter_html_tag(name)

        regex = '<p>.*?</p>'
        position = re.search(regex, result)
        if position:
            position = position.group().replace(' ', ',')
            position = _filter_html_tag(position)

        regex = '<div class="button">.*?<div class="box-content">'
        label = re.search(regex, result)
        if label:
            label = label.group()
            label = label.replace(' ', '').replace('</a>', ',')
            label = _filter_html_tag(label)
            label = label[:-1]

    regex = '<!--职业经历start-->.*?<!--职业经历end-->'
    html = re.search(regex, src)
    if html:
        result = html.group()
        regex = '<td.*?</tbody>'
        carrer = re.search(regex, result)
        if carrer:
            carrer = carrer.group().replace('<td class="td2">', '-').replace('<td class="td3">', '-').replace('</tr>', ',')
            carrer = _filter_html_tag(carrer).replace(' ', '')
            carrer = carrer[:-1]

    regex = '<!-- JiaThis Button END -->.*?<!--content-end-->'
    html = re.search(regex, src)
    if html:
        intro = html.group().replace('\t', '').replace('　', '').replace(' ', '')
        intro = _filter_html_tag(intro)

    investor = Investor(name, position, label, carrer, intro)
    return investor


def save_to_db(sql, values):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
    except MySQLdb.Error, e:
        print e
    conn.commit()
    cur.close
    conn.close()


def save_to_mysql(sql):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except MySQLdb.Error, e:
        print e
    conn.commit()
    cur.close
    conn.close()


def get_data_from_sql(table):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    link_list = []
    try:
        cur.execute('SELECT * FROM ' + table + ' WHERE update_time !=\'2016-01-11\'')
        results = cur.fetchall()
        for link in results:
            if link[3] is None:
                link_list.append(link[1])
        return link_list
    except MySQLdb.Error, e:
        print "MySql Error %d: %s" % (e.args[0], e.args[1])


def get_data_from_db(table):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    result = ''
    try:
        cur.execute('SELECT * FROM ' + table + ' WHERE update_time !=\'2016-01-11\'')
        result = cur.fetchall()
        return result
    except MySQLdb.Error, e:
        print "MySql Error %d: %s" % (e.args[0], e.args[1])


class Firm:
    __name = ''
    __regist_date = ''
    __regist_address = ''
    __centre = ''
    __website = ''
    __intro = ''

    def check(self):
        if self.__name == '':
            return 0
        else:
            return 1

    def show(self):
        print 'name:', self.__name
        print 'regist_date:', self.__regist_date
        print 'regist_address:', self.__regist_address
        print 'centre:', self.__centre
        print 'website:', self.__website
        print 'intro:', self.__intro

    def get_name(self):
        return self.__name

    def __init__(self, name, regist_date, regist_address, centre, website, intro):
        self.__name = name
        self.__regist_date = regist_date
        self.__regist_address = regist_address
        self.__centre = centre
        self.__website = website
        self.__intro = intro


class Company:
    project_name = ''
    company_name = ''
    reg_date = ''
    centre = ''
    area = ''
    website = ''
    fax = ''
    tel = ''
    ZIP_code = ''
    address = ''
    intro = ''

    def check(self):
        if self.project_name == '':
            return 0
        else:
            return 1

    def show(self):
        print self.project_name
        print self.company_name
        print self.reg_date
        print self.centre
        print self.area
        print self.website
        print self.fax
        print self.tel
        print self.ZIP_code
        print self.address
        print self.intro

    def __init__(self, project_name, company_name, reg_date, centre, area, website, fax, tel, ZIP_code, address, intro):
        self.project_name = project_name
        self.company_name = company_name
        self.reg_date = reg_date
        self.centre = centre
        self.area = area
        self.website = website
        self.fax = fax
        self.tel = tel
        self.ZIP_code = ZIP_code
        self.address = address
        self.intro = intro


class InvestmentEvent:
    __invest_firm_name = ''
    __project_name = ''
    __invest_time = ''
    __round = ''
    __amount = ''
    __area = ''

    def setname(self, name):
        self.__invest_firm_name = name

    def show(self):
        print self.__invest_firm_name
        print self.__project_name
        print self.__invest_time
        print self.__round
        print self.__amount
        print self.__area

    def __init__(self, invest_firm_name, project_name, invest_time, round, amount, area):
        self.__round = round
        self.__invest_firm_name = invest_firm_name
        self.__area = area
        self.__amount = amount
        self.__invest_time = invest_time
        self.__project_name = project_name


class Investor:
    investor_name = ''
    position = ''
    label = ''
    intro = ''
    career = ''

    def show(self):
        print self.investor_name
        print self.position
        print self.label
        print self.career
        print self.intro

    def check(self):
        if self.investor_name == "":
            return 0
        else:
            return 1

    def __init__(self, investor_name, position, label, career, intro):
        self.investor_name = investor_name
        self.position = position
        self.label = label
        self.career = career
        self.intro = intro


def fetch_firm_info(src):
    name = reg_date = centre = reg_address = website = intro = ''
    regex = '<!--content-start-->(.*?)<!--content-end-->'
    pattern = re.compile(regex)
    result = pattern.search(src)
    if result:
        result = result.group()
        regex = '<em>.*?</em></h1>'
        pattern = re.compile(regex)
        name = pattern.search(result)
        if name:
            name = _filter_html_tag(name.group())

        regex = '成立时间：.*?</li>'
        pattern = re.compile(regex)
        reg_date = pattern.search(result)
        if reg_date:
            reg_date = reg_date.group().replace('成立时间：', '').replace('</li>', '')

        regex = '机构总部：.*?<'
        pattern = re.compile(regex)
        centre = pattern.search(result)
        if centre:
            centre = centre.group().replace('机构总部：', '').replace('<', '')

        regex = '注册地点：.*?<'
        pattern = re.compile(regex)
        reg_address = pattern.search(result)
        if reg_address:
            reg_address = reg_address.group().replace('注册地点：', '').replace('<', '')

        regex = '官方网站：.*?</li>'
        pattern = re.compile(regex)
        website = pattern.search(result)
        if website:
            website = website.group().replace('官方网站：', '')
            website = _filter_html_tag(website)

        regex = '<!-- JiaThis Button END -->.*?<!--content-end-->'
        pattern = re.compile(regex)
        intro = pattern.search(result)
        if intro:
            intro = intro.group().replace('\t', '').replace(' ', '')
            intro = _filter_html_tag(intro)
    firm = Firm(name, reg_date, reg_address, centre, website, intro)
    return firm


def fetch_company_info(src):
    project_name = company_name = reg_date = centre = area = website = fax = tel = ZIP_code = address = intro = ''
    regex = '<!--content-start-->(.*?)<!--content-end-->'
    result = re.search(regex, src)
    if result:
        result = result.group()
        regex = '<h1>.*?<em>'
        company_name = re.search(regex, result)
        if company_name:
            company_name = company_name.group()
            company_name = _filter_html_tag(company_name)

        regex = '<em>.*?</em></h1>'
        pattern = re.compile(regex)
        project_name = pattern.search(result)
        if project_name:
            project_name = _filter_html_tag(project_name.group())

        regex = '成立时间：.*?</li>'
        pattern = re.compile(regex)
        reg_date = pattern.search(result)
        if reg_date:
            reg_date = reg_date.group().replace('成立时间：', '').replace('</li>', '')

        regex = '机构总部：.*?<'
        pattern = re.compile(regex)
        centre = pattern.search(result)
        if centre:
            centre = centre.group().replace('机构总部：', '').replace('<', '')

        regex = '所属行业：.*?<'
        pattern = re.compile(regex)
        area = pattern.search(result)
        if area:
            area = area.group().replace('所属行业：', '').replace('<', '')

        regex = '官方网站：.*?</li>'
        pattern = re.compile(regex)
        website = pattern.search(result)
        if website:
            website = website.group().replace('官方网站：', '')
            website = _filter_html_tag(website)

        regex = '<!-- JiaThis Button END -->.*?<!--content-end-->'
        pattern = re.compile(regex)
        contacts = pattern.search(result)
        if contacts:
            contacts = contacts.group()
            regex = '传　　真：.*?<'
            fax = re.search(regex, contacts)
            if fax:
                fax = fax.group().replace('传　　真：', '').replace('<', '')

            regex = '联系电话：.*?<'
            tel = re.search(regex, contacts)
            if tel:
                tel = tel.group().replace('联系电话：', '').replace('<', '')

            regex = '邮政编码：.*?<'
            ZIP_code = re.search(regex, contacts)
            if ZIP_code:
                ZIP_code = ZIP_code.group().replace('邮政编码：', '').replace('<', '')

            regex = '详细地址：.*?<'
            address = re.search(regex, contacts)
            if address:
                address = address.group().replace('详细地址：', '').replace('<', '')

            regex = '<p><p>.*?</p>'
            intro = re.search(regex, contacts)
            if intro:
                intro = intro.group()
                intro = _filter_html_tag(intro).replace('\t', '')
    company = Company(project_name, company_name, reg_date, centre, area, website, fax, tel, ZIP_code, address, intro)
    return company


def fetch_event_link(url):
    link_list = []
    url = url.encode('gbk') + '/vc/'
    src = fetch(url)
    regex = 'total">.*?<'
    pattern = re.compile(regex)
    pagenum = pattern.search(src)
    if pagenum:
        pagenum = pagenum.group().replace('total">', '').replace('<', '')
        if pagenum:
            num = int(pagenum) / 36 + 1
            for i in range(1, num + 1):
                src = fetch(url + str(i))
                regex = '<div class="box box-content">.*?</table>'
                pattern = re.compile(regex)
                result = pattern.search(src)
                if result:
                    result = result.group()
                    regex = '/inv/show.*?/'
                    showid_list = re.findall(regex, result)
                    for showid in showid_list:
                        link_list.append(showid)
                        print showid
    return link_list


def fetch_investment_event(src):
    project_name = invest_time = project_round = amount = area = ''
    regex = 'zdb-content.*?</div>'
    pattern = re.compile(regex)
    result = pattern.search(src)
    if result:
        result = result.group()
        regex = '投资时间.*?</p>'
        pattern = re.compile(regex)
        invest_time = pattern.search(result)
        if invest_time:
            invest_time = invest_time.group().replace('投资时间：', '')
            invest_time = _filter_html_tag(invest_time)

        regex = '受 资 方.*?">'
        pattern = re.compile(regex)
        project_name = pattern.search(result)
        if project_name:
            project_name = project_name.group().replace('受 资 方：', '')
            project_name = project_name.replace('/">', '')
            regex = '</b>.*/'
            string = re.search(regex, project_name)
            project_name = project_name.replace(string.group(), '')

        regex = '轮　　次.*?</p>'
        pattern = re.compile(regex)
        project_round = pattern.search(result)
        if project_round:
            project_round = project_round.group().replace('轮　　次：', '')
            project_round = _filter_html_tag(project_round)

        regex = '行业分类.*?</p>'
        pattern = re.compile(regex)
        area = pattern.search(result)
        if area:
            area = area.group().replace('行业分类：', '')
            regex = '</a>.*?</p>'
            string = re.search(regex, area)
            area = area.replace(string.group(), '')
            area = _filter_html_tag(area)

        regex = '金　　额.*?</p>'
        pattern = re.compile(regex)
        amount = pattern.search(result)
        if amount:
            amount = amount.group().replace('金　　额：', '')
            amount = _filter_html_tag(amount)
    event = InvestmentEvent(None, project_name, invest_time, project_round, amount, area)
    return event


def fetch_investor_link(url):
    def getnamepage(_url):
        _src = fetch(_url.encode('gbk'))
        _regex = '共搜索到.*?个人物'
        _pagenum = re.search(_regex, _src)
        if _pagenum:
            _pagenum = _pagenum.group().replace('共搜索到', '').replace('个人物', '')
            _pagenum = _filter_html_tag(_pagenum)
            return int(_pagenum)

    pagenum = getnamepage(url) / 20 + 1
    name_list = []
    for i in range(1, pagenum + 1):
        _url = url + '/' + str(i)
        src = fetch(_url)
        regex = '<ul class="news-list">.*?</ul>'
        result = re.search(regex, src)
        if result:
            names = result.group()
            regex = '"f16.*?</a>'
            names = re.findall(regex, names)
            for name in names:
                name = name.replace('"f16">', '')
                name = _filter_html_tag(name)
                name_list.append(name)
    return name_list


def _wait(second):
    sleep_time = second * random.random()
    print '[INFO]', time.ctime(), 'Sleeping for', sleep_time, 'seconds'
    time.sleep(sleep_time)
    print '[INFO]', time.ctime(), 'Wake up!'


def crawl_event_link():
    """
    this part is getting firm links from database and
    fetch their investment event links then save into database
    :return:
    """
    link_list = get_data_from_sql('ped_invest_firm_link')
    for name in link_list:
        url = 'http://zdb.pedaily.cn/company/' + name
        event_list = fetch_event_link(url)
        if event_list:
            sql = 'UPDATE ped_invest_firm_link SET update_time = \'' + time.strftime('%Y-%m-%d', time.localtime(
                time.time())) + '\' WHERE invest_firm_name = \'' + name + '\''
            save_to_mysql(sql)
        for event_link in event_list:
            event_link = 'http://zdb.pedaily.cn' + event_link
            sql = 'INSERT INTO ped_event_link(firm_name, event_link) VALUES (\'' + name + '\',\'' + event_link + '\')'
            save_to_mysql(sql)
        _wait(5)


def crawl_event():
    data = get_data_from_db('ped_event_link')
    for link in data:
        invest_firm_name = link[1]
        src = fetch(link[2])
        event = fetch_investment_event(src)
        event.setname(invest_firm_name)
        event.show()


def crawl_firm_link():
    """
    this part is to get firm link from website and
    save into database
    :return:
    """
    for i in range(1, 386 + 1):
        firm_link_list = fetch_firm_link(i)
        _wait(5)
        for firm_link in firm_link_list:
            print firm_link


def crawl_investor_link():
    for i in range(65, 91):
        url = 'http://zdb.pedaily.cn/people/c'
        url = url + chr(i)
        name_list = fetch_investor_link(url)
        for name in name_list:
            investor_link = 'http://zdb.pedaily.cn/people/' + name.replace(' ', '%20')
            print name, investor_link
            sql = 'INSERT INTO ped_investor_link(investor_name, investor_link) VALUES (\'' + name + '\',\'' + investor_link + '\')'
            save_to_mysql(sql)


def crawl_company_link():
    for i in range(1, 865 + 1):
        company_link_list = fetch_company_link(i)
        _wait(5)
        for company_link in company_link_list:
            name = company_link
            link = 'http://zdb.pedaily.cn/enterprise/' + company_link
            sql = 'INSERT INTO ped_company_link(company_name, company_link) VALUES (\'' + name + '\',\'' + link + '\')'
            save_to_mysql(sql)


def crawl_firm_info():
    data = get_data_from_db('ped_invest_firm_link')
    for firm_link in data:
        firm_name = firm_link[0]
        src = fetch(firm_link[1].replace(' ', '%20').encode('gbk'))
        if src:
            firm_info = fetch_firm_info(src)
            firm_team = fetch_firm_team(src)
            if firm_info.check():
                sql = 'UPDATE ped_invest_firm_link SET update_time = \'' + time.strftime('%Y-%m-%d', time.localtime(
                    time.time())) + '\' WHERE invest_firm_name = \'' + firm_name + '\''
                save_to_mysql(sql)
                firm_info.show()
            if firm_team:
                firm_team = set(firm_team)
                for investor in firm_team:
                    print investor.replace(' ', '%20').decode('utf8','ignore').encode('gbk')
                    try:
                        investor_url = 'http://zdb.pedaily.cn/people/' + investor.replace(' ', '%20').decode('utf8','ignore').encode('gbk')
                        investor_src = fetch(investor_url)
                        if investor_src:
                            sql = 'UPDATE ped_investor_link SET update_time = \'' + time.strftime('%Y-%m-%d', time.localtime(
                                time.time())) + '\' WHERE investor_name = \'' + investor + '\''
                            save_to_mysql(sql)
                            investor_info = fetch_investor_info(investor_src)
                            sql = 'INSERT INTO ped_invest_firm_investor(invest_firm_name, investor_name, position, label,' \
                                  ' career, intro)VALUES (%s,%s,%s,%s,%s,%s)'
                            values = (firm_info.get_name(), investor, investor_info.position,
                                      investor_info.label, investor_info.career, investor_info.intro)
                            if investor:
                                save_to_db(sql, values)
                    except Exception as error:
                        print error


def crawl_investor_info():
    db = 'ped_investor_link'
    data = get_data_from_db(db)
    for link in data:
        try:
            url = link[2].encode('gbk')
            src = fetch(url)
            investor = fetch_investor_info(src)
            investor.show()
        except UnicodeEncodeError, e:
            print '[Error]:', link[2]


def crawl_company_info():
    db = 'ped_company_link'
    name_list = get_data_from_sql(db)
    for name in name_list:
        try:
            url = 'http://zdb.pedaily.cn/enterprise/' + name.replace(' ', '%20').encode('gbk')
            src = fetch(url)
            if src:
                sql = 'UPDATE ped_company_link SET update_time = \'' + time.strftime('%Y-%m-%d', time.localtime(
                    time.time())) + '\' WHERE company_name = \'' + name + '\''
                save_to_mysql(sql)
                company = fetch_company_info(src)
                sql = 'insert into ped_project_info(project_name, company_name, reg_date, centre, area, website, fax, tel, ZIP_code, address, intro) VALUES ' \
                      + '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                values = (company.project_name, company.company_name, company.reg_date, company.centre, company.area,
                          company.website, company.fax, company.tel, company.ZIP_code, company.address, company.intro)
                if company.check():
                    save_to_db(sql, values)
        except:
            print '[Error:]', name


if __name__ == '__main__':
    crawl_firm_info()
