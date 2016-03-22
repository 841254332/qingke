import IO
from math import log
__author__ = 'admin'


def get_data_set():
    sql = 'SELECT * FROM data_investor_feature'
    result = IO.get_data_from_db(sql, 'test')
    data_set = []
    for rows in result:
        row = (rows[1], float(rows[2]), float(rows[3]), float(rows[4]), float(rows[5]), float(rows[6]), float(rows[7]),
               float(rows[8]), float(rows[9]), float(rows[10]), float(rows[11]), float(rows[12]), float(rows[13]),
               float(rows[14]), float(rows[15]), float(rows[16]),float(rows[17]), float(rows[18]), float(rows[19]),
               float(rows[20]), float(rows[21]), float(rows[22]), float(rows[23]), float(rows[24]))
        data_set.append(row)
    return data_set


def entropy(data_set):
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    count_7 = 0
    count_8 = 0
    count_9 = 0
    for row in data_set:
        if row[0] == '1':
            count_1 += 1
        elif row[0] == '2':
            count_2 += 1
        elif row[0] == '3':
            count_3 += 1
        elif row[0] == '4':
            count_4 += 1
        elif row[0] == '5':
            count_5 += 1
        elif row[0] == '6':
            count_6 += 1
        elif row[0] == '7':
            count_7 += 1
        elif row[0] == '8':
            count_8 += 1
        else:
            count_9 += 1
    # print count_1, count_2, count_3, count_4, count_5, count_6, count_7, count_8, count_9
    total = float(count_1 + count_2 + count_3 + count_4 + count_5 + count_6 + count_7 + count_8 + count_9)
    entropy_s = -((count_1 / total) * log((count_1 / total), 2)) - ((count_2 / total) * log((count_2 / total), 2)) - \
                (count_3 / total) * log(count_3 / total, 2) - (count_4 / total) * log(count_4 / total, 2) - \
                (count_5 / total) * log(count_5 / total, 2) - (count_6 / total) * log(count_6 / total, 2) - \
                (count_7 / total) * log(count_7 / total, 2) - (count_8 / total) * log(count_8 / total, 2) - \
                (count_9 / total) * log(count_9 / total, 2)
    return entropy_s


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


def get_split_node(data_set, mid=None, index=None):
    gain_ratio_feature_list = []
    for i in range(1, 24):
        count_list = []
        entropy_feature_s_list = []
        split_s_list = []
        for row in data_set:
            count_list.append(row[i])
        count_list = get_mid(count_list)
        for mid in count_list:
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
            for row in data_set:
                value = row[i]
                if value > mid:
                    if row[0] == '1':
                        p_count_1 += 1
                    elif row[0] == '2':
                        p_count_2 += 1
                    elif row[0] == '3':
                        p_count_3 += 1
                    elif row[0] == '4':
                        p_count_4 += 1
                    elif row[0] == '5':
                        p_count_5 += 1
                    elif row[0] == '6':
                        p_count_6 += 1
                    elif row[0] == '7':
                        p_count_7 += 1
                    elif row[0] == '8':
                        p_count_8 += 1
                    else:
                        p_count_9 += 1
                else:
                    if row[0] == '1':
                        n_count_1 += 1
                    elif row[0] == '2':
                        n_count_2 += 1
                    elif row[0] == '3':
                        n_count_3 += 1
                    elif row[0] == '4':
                        n_count_4 += 1
                    elif row[0] == '5':
                        n_count_5 += 1
                    elif row[0] == '6':
                        n_count_6 += 1
                    elif row[0] == '7':
                        n_count_7 += 1
                    elif row[0] == '8':
                        n_count_8 += 1
                    else:
                        n_count_9 += 1
            p_total = float(p_count_1 + p_count_2 + p_count_3 + p_count_4 + p_count_5 + p_count_6 + p_count_7 + p_count_8 + p_count_9)
            n_total = float(n_count_1 + n_count_2 + n_count_3 + n_count_4 + n_count_5 + n_count_6 + n_count_7 + n_count_8 + n_count_9)
            total = p_total + n_total
            entropy_feature_s = ((n_total / total) * (-(n_count_1 / n_total) * log((n_count_1 / n_total), 2) -
                                                       (n_count_2 / n_total) * log((n_count_2 / n_total), 2) -
                                                       (n_count_3 / n_total) * log((n_count_3 / n_total), 2) -
                                                       (n_count_4 / n_total) * log((n_count_4 / n_total), 2) -
                                                       (n_count_5 / n_total) * log((n_count_5 / n_total), 2) -
                                                       (n_count_6 / n_total) * log((n_count_6 / n_total), 2) -
                                                       (n_count_7 / n_total) * log((n_count_7 / n_total), 2) -
                                                       (n_count_8 / n_total) * log((n_count_8 / n_total), 2) -
                                                       (n_count_9 / n_total) * log((n_count_9 / n_total), 2))) + \
                                   ((p_total / total) * (-(p_count_1 / p_total) * log((p_count_1 / p_total), 2) -
                                                       (p_count_2 / p_total) * log((p_count_2 / p_total), 2) -
                                                       (p_count_3 / p_total) * log((p_count_3 / p_total), 2) -
                                                       (p_count_4 / p_total) * log((p_count_4 / p_total), 2) -
                                                       (p_count_5 / p_total) * log((p_count_5 / p_total), 2) -
                                                       (p_count_6 / p_total) * log((p_count_6 / p_total), 2) -
                                                       (p_count_7 / p_total) * log((p_count_7 / p_total), 2) -
                                                       (p_count_8 / p_total) * log((p_count_8 / p_total), 2) -
                                                       (p_count_9 / p_total) * log((p_count_9 / p_total), 2)))
            entropy_feature_s_list.append(entropy_feature_s)
            split_s = -(n_total / total) * log((n_total / total), 2) - (p_total / total) * log((p_total / total), 2)
            split_s_list.append(split_s)
            # print 'entropy_area_count_S:', entropy_area_count_S
            # gain_area_count_S = entropy_s - entropy_area_count_S
            # print 'gain_area_count_S:', gain_area_count_S
            # gain_ratio_area_count = gain_area_count_S / split_area_count_S
            # print 'gain_ratio_area_count:', gain_ratio_area_count
        for j in range(0, entropy_feature_s_list.__len__()):
            if entropy_feature_s_list[j] is min(entropy_feature_s_list):
                entropy_s = entropy(data_set)
                gain_feature = entropy_s - entropy_feature_s_list[j]
                gain_ratio_feature = gain_feature / split_s_list[j]
                gain_ratio_feature_list.append(gain_ratio_feature)
    for j in range(0, gain_ratio_feature_list.__len__()):
        if gain_ratio_feature_list[j] is max(gain_ratio_feature_list):
            print i, gain_ratio_feature_list[j], count_list[j]
data_set = get_data_set()
get_split_node(data_set)
