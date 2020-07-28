import pandas as pd
import copy
import time


# 根据相对速度v_x, v_y及时间差计算出理想位置
def compute_ideal_pos(data):
    # list_lat = copy.deepcopy(data['Obj_DistLat'])
    # list_long = copy.deepcopy(data['Obj_DistLong'])
    # data['Obj_DistLat'], data['Obj_DistLong'] = list_long, list_lat
    dis_x_ideal, dis_y_ideal = [], []
    dis_x_ideal.append(data['Obj_DistLat'].values[0])
    dis_y_ideal.append(data['Obj_DistLong'].values[0])

    for index in range(len(data)-1):
        d_t = data['app_stamp'][index+1]-data['app_stamp'][index]
        d_vx, d_vy = data['Obj_VrelLat'][index], data['Obj_VrelLong'][index]
        # 获取index对应的x,y位置
        dis_now_x, dis_now_y = data['Obj_DistLat'][index], data['Obj_DistLong'][index]
        # 解码后时间和之前的倍数关系
        scale = 0.00001
        # 理想的x,y前进距离
        d_dx = d_t*d_vx*scale
        d_dy = d_t*d_vy*scale
        # 理想位置
        dis_next_x = dis_now_x + d_dx
        dis_next_y = dis_now_y + d_dy
        dis_x_ideal.append(dis_next_x)
        dis_y_ideal.append(dis_next_y)
    data['ideal_DisLat'] = dis_x_ideal
    data['ideal_DisLong'] = dis_y_ideal
    return data


# 对比实际位置和compute_ideal_pos得到的理想位置，分出sub_ID
def add_sub_ID(data, least_point, bias_range):
    sub = 0
    sub_list = []
    for index in range(len(data)):
        # bias为实际x, y位置和理想的差
        bias_x = abs(data['Obj_DistLat'][index]-data['ideal_DisLat'][index])
        bias_y = abs(data['Obj_DistLong'][index]-data['ideal_DisLong'][index])
        if bias_x > bias_range or bias_y > bias_range:
            # 超出范围，sub_id加一
            sub = sub + 1
        sub_list.append(str(int(data['Obj_ID'][index]))+'_'+str(sub))
    # 插入sub_ID
    data['sub_ID'] = sub_list
    sub_ID_count = []
    for i in range(len(sub_list)):
        sub_ID_count.append(sub_list.count(sub_list[i]))
    data['sub_ID_count'] = sub_ID_count
    # 去除不足least_point的轨迹
    data = data.loc[data['sub_ID_count'] >= least_point]
    return data


if __name__ == '__main__':
    gt_data = pd.read_csv('E:\\intern\\20200727\\data\\gt_data_1.csv')
    s = time.time()
    gt_data = gt_data.drop_duplicates(subset=['Obj_DistLat', 'Obj_DistLong'], keep='first', inplace=False)\
        .reset_index(drop=True)
    e = time.time()
    interval = e - s
    print(interval)
    gt_data1 = compute_ideal_pos(gt_data)
    e = time.time()
    interval = e - s
    print('interval of compute_ideal_pos:', interval)
    least__point = 5
    bias__range = 10
    gt_data2 = add_sub_ID(gt_data1, least__point, bias__range)
    e = time.time()
    interval = e - s                                  
    print('interval of add_sub_ID:', interval)
    gt_data2.to_csv('E:\\intern\\20200727\\data\\gt_data_2.csv')




