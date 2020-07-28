import pandas as pd
import time


def gt_new_id(data, least_point, bias_range):
    sub_id = 0
    new_id = [str(data['Obj_ID'].values[0]) + '_' + str(sub_id)]

    # sub_id increase while position change greatly
    for index in range(1, len(data)):
        if abs(data['Obj_DistLat'].values[index]-data['Obj_DistLat'].values[index-1]) > bias_range or\
                abs(data['Obj_DistLong'].values[index]-data['Obj_DistLong'].values[index-1]) > bias_range:
            sub_id += 1
        new_id.append(str(data['Obj_ID'].values[index]) + '_' + str(sub_id))
    print('len(new_id):', len(new_id))

    # computer new_id_count each line
    new_id_count = []
    for i in range(len(data)):
        new_id_count.append(new_id.count(new_id[i]))

    # add two new columns
    data['new_id'] = new_id
    data['sub_ID_count'] = new_id_count

    # 去除不足least_point的轨迹
    data = data.loc[data['sub_ID_count'] >= least_point]
    return data


if __name__ == '__main__':
    s = time.time()
    gt_data = pd.read_csv('E:\\intern\\20200727\\data\\gt_data_1.csv')
    gt_data = gt_data.drop_duplicates(subset=['Obj_DistLat', 'Obj_DistLong'], keep='first', inplace=False) \
        .reset_index(drop=True)
    data1 = gt_new_id(gt_data, least_point=5, bias_range=10)
    data1.to_csv('E:\\intern\\20200727\\data\\gt_data_2_new.csv')

    e = time.time()
    interval = e - s
    print("add new_id to compare data takes time:", interval)




