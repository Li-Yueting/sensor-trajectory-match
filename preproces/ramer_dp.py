from rdp import rdp
import pandas as pd
import time


def rdp_gt(gt_data, epsilon):
    """
    Simplify trajectories by returning pivot points of them

    :param gt_data:
    :param epsilon:
    :return: pivot_mask

    >> rdp_gt([[2,2], [3,3]], 0,1)
    [True, True]

    """
    new_data = pd.DataFrame({'Unnamed: 0':[], 'Unnamed: 0.1':[], 'app_stamp':[], 'Obj_DistLat':[], 'Obj_DistLong':[],
                             'Obj_VrelLong':[], 'Obj_VrelLat':[], 'Obj_ID':[], 'Obj_DynProp':[], 'Obj_RCS':[],
                             'ideal_DisLat':[], 'ideal_DisLong':[], 'sub_ID':[],'sub_ID_count':[]})
    for sub_ID, sub_data in gt_data.groupby('sub_ID'):
        sub_data = sub_data.reset_index(drop=True)
        sub_x = sub_data['Obj_DistLat']
        sub_y = sub_data['Obj_DistLong']
        pos = pd.concat([sub_x, sub_y], axis=1).values
        mask = rdp(pos, algo="iter", epsilon=epsilon, return_mask=True)
        sub_data_del = sub_data
        for sub_index in range(len(mask)):
            if not mask[sub_index]:
                sub_data_del = sub_data_del.drop(index=sub_index)
                # print(sub_index)
        new_data = pd.merge(new_data, sub_data_del, how='outer')
    return new_data


def rdp_compare(compare_data, epsilon):
    """
    Simplify trajectories by returning pivot points of them

    :param compare_data:
    :param epsilon:
    :return: pivot_mask

    >> rdp_gt([[2,2], [3,3]], 0,1)
    [True, True]

    """
    new_data = pd.DataFrame({'Unnamed: 0': [], 'app_stamp': [], 'ID_tracking': [], 'x_tracking': [],
                             'y_tracking': [], 'z_tracking': [], 'xd': [], 'yd': [], 'type_tracking': [], 'status': [],
                             'tick': [], 'range_tracking': [], 'speed_tracking': [], 'sinAzim_tracking': [],
                             'sinElv_tracking': [], 'new_id': [], 'sub_ID_count': []})
    for sub_ID, sub_data in compare_data.groupby('new_id'):
        sub_data = sub_data.reset_index(drop=True)
        sub_x = sub_data['x_tracking']
        sub_y = sub_data['y_tracking']
        pos = pd.concat([sub_x, sub_y], axis=1).values
        mask = rdp(pos, algo="iter", epsilon=epsilon, return_mask=True)
        sub_data_del = sub_data
        for sub_index in range(len(mask)):
            if not mask[sub_index]:
                sub_data_del = sub_data_del.drop(index=sub_index)
                # print(sub_index)
        new_data = pd.merge(new_data, sub_data_del, how='outer')
    return new_data


if __name__ == '__main__':
    s = time.time()
    # gt__data = pd.read_csv('E:\\intern\\20200727\\data\\gt_data_2.csv')
    # gt_data_rdp = rdp_gt(gt__data, epsilon=0.1)
    # gt_data_rdp.to_csv('E:\\intern\\20200727\\data\\gt_data_rdp.csv')
    interval = time.time() - s
    print(f'gt轨迹抽稀耗时：{interval}s')

    s = time.time()
    compare__data = pd.read_csv('E:\\intern\\20200727\\data\\compare_data_2.csv')
    compare_data_rdp = rdp_compare(compare__data, epsilon=0.1)
    compare_data_rdp.to_csv('E:\\intern\\20200727\\data\\compare_data_rdp.csv')
    interval = time.time() - s
    print(f'compare轨迹抽稀耗时：{interval}s')
