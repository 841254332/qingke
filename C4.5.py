import IO
import math
__author__ = 'admin'


class FirmFeature:
    name = ''
    goal = ''
    area_count = 0
    invest_time = 0
    on_market_ratio = 0
    invest_amount = 0
    company_age_avg = 0
    finance = 0
    tourism = 0
    hardware = 0
    auto_traffic = 0
    corporate_services = 0
    local_life = 0
    e_commerce = 0
    education = 0
    advertising = 0
    game = 0
    culture = 0
    health = 0
    estate = 0
    SNS = 0
    mobile = 0
    tool_software = 0
    unknown = 0

    def __init__(self, name, goal, area_count, invest_time, on_market_ratio, invest_amount, company_age_avg, finance,
                 tourism, hardware, auto_traffic, corporate_services, local_life, e_commerce, education, advertising,
                 game, culture, health, estate, SNS, mobile, tool_software, unknown):
        self.name = name
        self.goal = goal
        self.area_count = area_count
        self.invest_time = invest_time
        self.on_market_ratio = on_market_ratio
        self.invest_amount = invest_amount
        self.company_age_avg = company_age_avg
        self.finance = finance
        self.tourism = tourism
        self.hardware = hardware
        self.auto_traffic = auto_traffic
        self.corporate_services = corporate_services
        self.local_life = local_life
        self.e_commerce = e_commerce
        self.education = education
        self.advertising = advertising
        self.game = game
        self.culture = culture
        self.health = health
        self.estate = estate
        self.SNS = SNS
        self.mobile = mobile
        self.tool_software = tool_software
        self.unknown = unknown


firm_feature_list = []
area_count_list = []
gain_ratio_list = []
sql = 'SELECT * FROM data_investor_feature'
result = IO.get_data_from_db(sql, 'test')
for rows in result:
    firm_feature = FirmFeature(rows[0], rows[1], float(rows[2]), float(rows[3]), float(rows[4]), float(rows[5])
                               , float(rows[6]), float(rows[8]), float(rows[9]), float(rows[10]), float(rows[11])
                               , float(rows[12]), float(rows[13]), float(rows[14]), float(rows[15]), float(rows[16])
                               , float(rows[17]), float(rows[18]), float(rows[19]), float(rows[20]), float(rows[21])
                               , float(rows[22]), float(rows[23]), float(rows[24]))
    firm_feature_list.append(firm_feature)
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0
count_7 = 0
count_8 = 0
count_9 = 0
for firm_feature in firm_feature_list:
    if firm_feature.goal == '1':
        count_1 += 1
    elif firm_feature.goal == '2':
        count_2 += 1
    elif firm_feature.goal == '3':
        count_3 += 1
    elif firm_feature.goal == '4':
        count_4 += 1
    elif firm_feature.goal == '5':
        count_5 += 1
    elif firm_feature.goal == '6':
        count_6 += 1
    elif firm_feature.goal == '7':
        count_7 += 1
    elif firm_feature.goal == '8':
        count_8 += 1
    else:
        count_9 += 1
# print count_1, count_2, count_3, count_4, count_5, count_6, count_7, count_8, count_9
total = float(count_1 + count_2 + count_3 + count_4 + count_5 + count_6 + count_7 + count_8 + count_9)
entropy_S = -((count_1 / total) * math.log((count_1 / total), 2)) - ((count_2 / total) * math.log((count_2 / total), 2)) - \
            (count_3 / total) * math.log(count_3 / total, 2) - (count_4 / total) * math.log(count_4 / total, 2) - \
            (count_5 / total) * math.log(count_5 / total, 2) - (count_6 / total) * math.log(count_6 / total, 2) - \
            (count_7 / total) * math.log(count_7 / total, 2) - (count_8 / total) * math.log(count_8 / total, 2) - \
            (count_9 / total) * math.log(count_9 / total, 2)
print 'entropy_S:', entropy_S


def get_mid(arg):
    results = []
    length = arg.__len__()
    arg.sort()
    for i in range(0, length - 1):
        mid = (arg[i] + arg[i + 1]) / 2
        results.append(mid)
    results = list(set(results))
    results.sort()
    return results

all_feature_list = ('area_count', 'invest_time', 'on_market_ratio', 'invest_amount', 'company_age_avg',
                    'finance', 'tourism', 'hardware', 'auto_traffic', 'corporate_services', 'local_life', 'e_commerce',
                    'education', 'advertising','game', 'culture', 'health', 'estate', 'SNS', 'mobile', 'tool_software',
                    'unknown')
for feature in all_feature_list:
    comp_feature = 'firm_feature1.' + feature
    for firm_feature1 in firm_feature_list:
        area_count_list.append(eval(comp_feature))
    area_count_list = get_mid(area_count_list)
    entropy_area_count_S_list = []
    for mid in area_count_list:
        p_count_1 = 0.0001
        p_count_2 = 0.0001
        p_count_3 = 0.0001
        p_count_4 = 0.0001
        p_count_5 = 0.0001
        p_count_6 = 0.0001
        p_count_7 = 0.0001
        p_count_8 = 0.0001
        p_count_9 = 0.0001
        n_count_1 = 0.0001
        n_count_2 = 0.0001
        n_count_3 = 0.0001
        n_count_4 = 0.0001
        n_count_5 = 0.0001
        n_count_6 = 0.0001
        n_count_7 = 0.0001
        n_count_8 = 0.0001
        n_count_9 = 0.0001
        for firm_feature in firm_feature_list:
            comp_feature = 'firm_feature.' + feature
            value = float(eval(comp_feature))
            if value > mid:
                if firm_feature.goal == '1':
                    p_count_1 += 1
                elif firm_feature.goal == '2':
                    p_count_2 += 1
                elif firm_feature.goal == '3':
                    p_count_3 += 1
                elif firm_feature.goal == '4':
                    p_count_4 += 1
                elif firm_feature.goal == '5':
                    p_count_5 += 1
                elif firm_feature.goal == '6':
                    p_count_6 += 1
                elif firm_feature.goal == '7':
                    p_count_7 += 1
                elif firm_feature.goal == '8':
                    p_count_8 += 1
                else:
                    p_count_9 += 1
            else:
                if firm_feature.goal == '1':
                    n_count_1 += 1
                elif firm_feature.goal == '2':
                    n_count_2 += 1
                elif firm_feature.goal == '3':
                    n_count_3 += 1
                elif firm_feature.goal == '4':
                    n_count_4 += 1
                elif firm_feature.goal == '5':
                    n_count_5 += 1
                elif firm_feature.goal == '6':
                    n_count_6 += 1
                elif firm_feature.goal == '7':
                    n_count_7 += 1
                elif firm_feature.goal == '8':
                    n_count_8 += 1
                else:
                    n_count_9 += 1
        p_total = float(p_count_1 + p_count_2 + p_count_3 + p_count_4 + p_count_5 + p_count_6 + p_count_7 + p_count_8 + p_count_9)
        n_total = float(n_count_1 + n_count_2 + n_count_3 + n_count_4 + n_count_5 + n_count_6 + n_count_7 + n_count_8 + n_count_9)
        total = p_total + n_total
        entropy_area_count_S = ((n_total / total) * (-(n_count_1 / n_total) * math.log((n_count_1 / n_total), 2) -
                                                   (n_count_2 / n_total) * math.log((n_count_2 / n_total), 2) -
                                                   (n_count_3 / n_total) * math.log((n_count_3 / n_total), 2) -
                                                   (n_count_4 / n_total) * math.log((n_count_4 / n_total), 2) -
                                                   (n_count_5 / n_total) * math.log((n_count_5 / n_total), 2) -
                                                   (n_count_6 / n_total) * math.log((n_count_6 / n_total), 2) -
                                                   (n_count_7 / n_total) * math.log((n_count_7 / n_total), 2) -
                                                   (n_count_8 / n_total) * math.log((n_count_8 / n_total), 2) -
                                                   (n_count_9 / n_total) * math.log((n_count_9 / n_total), 2))) + \
                               ((p_total / total) * (-(p_count_1 / p_total) * math.log((p_count_1 / p_total), 2) -
                                                   (p_count_2 / p_total) * math.log((p_count_2 / p_total), 2) -
                                                   (p_count_3 / p_total) * math.log((p_count_3 / p_total), 2) -
                                                   (p_count_4 / p_total) * math.log((p_count_4 / p_total), 2) -
                                                   (p_count_5 / p_total) * math.log((p_count_5 / p_total), 2) -
                                                   (p_count_6 / p_total) * math.log((p_count_6 / p_total), 2) -
                                                   (p_count_7 / p_total) * math.log((p_count_7 / p_total), 2) -
                                                   (p_count_8 / p_total) * math.log((p_count_8 / p_total), 2) -
                                                   (p_count_9 / p_total) * math.log((p_count_9 / p_total), 2)))
        entropy_area_count_S_list.append(entropy_area_count_S)
        split_area_count_S = -(n_total / total) * math.log((n_total / total), 2) - (p_total / total) * math.log((p_total / total), 2)
        # print 'entropy_area_count_S:', entropy_area_count_S
        gain_area_count_S = entropy_S - entropy_area_count_S
        # print 'gain_area_count_S:', gain_area_count_S
        gain_ratio_area_count = gain_area_count_S / split_area_count_S
        # print 'gain_ratio_area_count:', gain_ratio_area_count
    for i in range(0, entropy_area_count_S_list.__len__()):
        if entropy_area_count_S_list[i] is min(entropy_area_count_S_list):
            # print str(feature), area_count_list[i]
            # print 'minimum entropy_area_count_S:', entropy_area_count_S_list[i]
            p_total = 0.0
            n_total = 0.0
            for firm_feature in firm_feature_list:
                comp_feature = 'firm_feature.' + feature
                value = float(eval(comp_feature))
                if value > area_count_list[i]:
                    p_total += 1
                else:
                    n_total += 1
            # print 'p_total:', p_total, 'n_total:', n_total
            split_area_count_S = -(n_total / total) * math.log((n_total / total), 2) - (p_total / total) * math.log((p_total / total), 2)
            gain_area_count_S = entropy_S - entropy_area_count_S_list[i]
            # print 'gain_area_count_S', gain_area_count_S
            # print 'split_area_count_S:', split_area_count_S
            gain_ratio_area_count = gain_area_count_S / split_area_count_S
            print feature,
            print 'gain_ratio_area_count:', gain_ratio_area_count
            print 'mid', area_count_list[i]
            gain_ratio_list.append(gain_ratio_area_count)
    area_count_list = []
    entropy_area_count_S_list = []
for i in range(0, gain_ratio_list.__len__()):
    if gain_ratio_list[i] is max(gain_ratio_list):
        print i, gain_ratio_list[i]