import matplotlib.pyplot as plt
import pandas as pd


def id_figs(data, x_min, x_max, y_min, y_max, id_figs_path):
    new_data = data.groupby('Obj_ID')
    for ID, value in new_data:
        pos_ID_x = value['Obj_DistLat']
        pos_ID_y = value['Obj_DistLong']
        plt.axis([x_min, x_max, y_min, y_max])
        plt.plot(pos_ID_x, pos_ID_y)
    plt.show()


# 画每个Obj_ID对应的轨迹图,每个图含其所有sub_id对应的轨迹图
def sub_id_figs(data, x_min, x_max, y_min, y_max, sub_id_figs_path):
    groups = data.groupby('Obj_ID')
    for Obj_ID, group in groups:
        data1 = group
        for new_id, sub_group in data1.groupby('new_id'):
            pos_x = sub_group['Obj_DistLat']
            pos_y = sub_group['Obj_DistLong']
            plt.plot(pos_x, pos_y)
        plt.title(str(Obj_ID))
        plt.axis([x_min, x_max, y_min, y_max])
        plt.legend()
        plt.savefig(sub_id_figs_path + str(Obj_ID) + '_GT' + '.png')
        plt.clf()


if __name__ == '__main__':
    gt_data = pd.read_csv('E:\\intern\\20200727\\data\\gt_data_2_new.csv')
    xmin = min(gt_data['Obj_DistLat'])
    xmax = max(gt_data['Obj_DistLat'])
    ymin = min(gt_data['Obj_DistLong'])
    ymax = max(gt_data['Obj_DistLong'])
    # id_figs(gt_data, xmin, xmax, ymin, ymax, 'E:\\intern\\20200727\\plot\\fig')
    sub_id_figs(gt_data, xmin, xmax, ymin, ymax, 'E:\\intern\\20200727\\plot\\fig\\')
