import math
import os.path
from PIL import Image


def get_big_map(dir):
    """
    get the big map stored on the UAV locally.
    :param dir: stored path.
    :return: big map paths and center coordinates.
    """
    paths = []
    labels = []

    file_path = os.listdir(dir)
    print(len(file_path))
    for file in file_path:
        full_file_path = os.path.join(dir, file)
        paths.append(full_file_path)
        file = file[:-4]
        file = file.split(',')
        labels.append(list(map(eval, [file[0], file[1]])))

    return paths, labels


def screenshot(paths, labels, number, new_lat, new_lon, dir):
    # new frame path
    path = dir + '/' + str(number) + "," + str(new_lat) + "," + str(new_lon) + '.png'
    if os.path.exists(path) is False:
        min_dis = math.inf
        idx = -1

        for i in range(0, len(labels)):
            lat_dis = (new_lat - labels[i][0]) * 111000
            lon_dis = (new_lon - labels[i][1]) * 111000 * math.cos(labels[i][0] / 180 * math.pi)

            dis = math.sqrt(lat_dis * lat_dis + lon_dis * lon_dis)
            if dis < min_dis:
                min_dis = dis
                idx = i

        # latitude: 1000 m
        # longitude: 1000 m
        # 1400, 1400
        # 0.714286 m / pixel
        # 0.714286 m / pixel
        # find the most match big map and screenshot
        lat_dis = (new_lat - labels[idx][0]) * 111000
        lon_dis = (new_lon - labels[idx][1]) * 111000 * math.cos(labels[idx][0] / 180 * math.pi)
        lat_pixel_dis = lat_dis / 1000 * 1400
        lon_pixel_dis = lon_dis / 1000 * 1400
        # 截图中心点的像素偏移量
        center_lat_pixel = 700 - lat_pixel_dis
        center_lon_pixel = 700 + lon_pixel_dis

        # 截图的像素大小
        edge = 300 / 1000 * 1400
        # If the center of the new image is out of bounds
        if center_lat_pixel + edge // 2 < 0:
            return -1
        if center_lat_pixel - edge // 2 > 1400:
            return -1
        if center_lon_pixel + edge // 2 < 0:
            return -1
        if center_lon_pixel - edge // 2 > 1400:
            return -1

        pic = Image.open(paths[idx])
        pic = pic.crop((center_lon_pixel - edge // 2, center_lat_pixel - edge // 2,
                        center_lon_pixel + edge // 2, center_lat_pixel + edge // 2))
        pic = pic.resize((224, 224))
        pic.save(path)

    # new screenshot image
    return path


# def generate_circle_path(center_lat=23.4, center_lon=120.3,
#                          big_map_dir="../../../mnt/nfs/wyx/bigmap/",
#                          taiwan_dir="../../../mnt/nfs/wyx/taiwan/",
#                          num_nodes=100,
#                          radius=10000,
#                          step=100,
#                          noise_step=50):
#     points = []
#     paths, labels = get_big_map(big_map_dir)
#     if os.path.exists(taiwan_dir) is False:
#         os.mkdir(taiwan_dir)
#
#     # 计算每个点之间的角度间隔
#     angle_step = 2 * math.pi / num_nodes
#
#     # 生成坐标点
#     for i in range(0, num_nodes):
#         angle = i * angle_step
#         lat = round(center_lat + radius * math.sin(angle) / 111000, 6)
#         lon = round(center_lon + radius * math.cos(angle) / 111000 / math.cos(lat / 180 * math.pi), 6)
#         # 添加到坐标集合
#         points.append((lat, lon))
#
#     for i in range(0, num_nodes):
#         for j in range(i + 1, num_nodes):
#             print(str(i) + "," + str(j))
#             if j == i:
#                 continue
#
#             start_point = points[i]
#             end_point = points[j]
#             lat_diff = (end_point[0] - start_point[0]) * 111000
#             lon_diff = (end_point[1] - start_point[1]) * 111000 * math.cos(start_point[0] / 180 * math.pi)
#             diff = math.sqrt(lat_diff * lat_diff + lon_diff * lon_diff)
#             sin = float(lat_diff / diff)
#             cos = float(lon_diff / diff)
#
#             # 每隔100米走一步
#             num = diff / step
#
#             for noise in range(0, 1):
#                 if os.path.exists(taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise)) is False:
#                     os.mkdir(taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise))
#                 else:
#                     continue
#
#                 for n in range(0, int(num)):
#                     new_lat = round(start_point[0] + n * step * sin / 111000, 6)
#                     new_lon = round(start_point[1] + n * step * cos / 111000 / math.cos(new_lat / 180 * math.pi), 6)
#
#                     res = screenshot(paths, labels, n, new_lat, new_lon,
#                                dir=taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise))
#                     if res == -1:
#                         print("xxxxxxxxxxxxxxx")
#
#             for noise in range(1, 20):
#                 if os.path.exists(taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise)) is False:
#                     os.mkdir(taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise))
#                 else:
#                     continue
#
#                 for n in range(0, int(num)):
#                     new_lat = start_point[0] + n * step * sin / 111000
#                     new_lon = start_point[1] + n * step * cos / 111000 / math.cos(new_lat / 180 * math.pi)
#                     new_lat = round(new_lat +
#                                     random.uniform(a=-1, b=1) * noise_step / 111000, 6)
#                     new_lon = round(new_lon +
#                                     random.uniform(a=-1, b=1) * noise_step / 111000 / math.cos(new_lat / 180 * math.pi),
#                                     6)
#
#                     res = screenshot(paths, labels, n, new_lat, new_lon,
#                                dir=taiwan_dir + "path" + str(i) + str(",") + str(j) + str(",") + str(noise))
#                     if res == -1:
#                         print("xxxxxxxxxxxxxxx")
#
#     return points
#
#
# def calculate_img_num(taiwan_dir="../../../mnt/nfs/wyx/taiwan/",
#                       num_nodes=100):
#     num = 0
#     dir_num = 0
#     for i in range(0, num_nodes):
#         for j in range(i + 1, num_nodes):
#             for k in range(0, 20):
#                 full_dir = os.path.join(taiwan_dir, "path" + str(i) + "," + str(j) + "," + str(k))
#                 if os.path.exists(full_dir):
#                     print(full_dir)
#                     files = os.listdir(full_dir)
#                     dir_num += 1
#                     num += len(files)
#     print(dir_num)
#     print(num)


def generate_class_data(left_down_lat=23.31, left_down_lon=120.21,
                        big_map_dir="../../../mnt/nfs/wyx/bigmap/",
                        taiwan_dir="../../../mnt/nfs/wyx/large/",
                        num_per_class=1024):
    points = []
    paths, labels = get_big_map(big_map_dir)
    if os.path.exists(taiwan_dir) is False:
        os.mkdir(taiwan_dir)

    lat_diff = 1000 / 111000

    # 南北方向20个方格，方格1000米*1000米
    for i in range(0, 20):
        per_left_down_lat = round(left_down_lat + i * lat_diff, 8)

        # 东西方向18个方格，方格1000米*1000米，相邻方格中心点距离1000米，无重复
        for j in range(0, 20):
            lon_diff = lat_diff / math.cos(per_left_down_lat / 180 * math.pi)
            per_left_down_lon = round(left_down_lon + j * lon_diff, 8)
            points.append([per_left_down_lat, per_left_down_lon])

    num_per_line = int(math.sqrt(num_per_class))
    step = 800 / num_per_line

    for i in range(int(0.8 * len(points)), int(1 * len(points))):
        print(i)
        if os.path.exists(taiwan_dir + "class" + str(i)) is False:
            os.mkdir(taiwan_dir + "class" + str(i))

        for j in range(0, num_per_line):
            # 从方格的左下角，一张图片300米，需要提前减掉这部分
            center_lat = round(points[i][0] + (100 + j * step) / 111000, 8)

            for k in range(0, num_per_line):
                # 从方格的左下角，一张图片300米，需要提前减掉这部分
                center_lon = round(points[i][1] + (100 + k * step) / 111000 \
                                                / math.cos(center_lat / 180 * math.pi), 8)
                # print(center_lat)
                # print(center_lon)
                res = screenshot(paths, labels, j * num_per_line + k, center_lat, center_lon,
                           dir=taiwan_dir + "class" + str(i))
                if res == -1:
                    print("xxxxxxxxxxxxxxx")

    return points


def calculate_class_img_num(large_dir="../../../mnt/nfs/wyx/large/",
                      num_nodes=400):
    tnum = 0
    for i in range(0, num_nodes):
        class_path = os.path.join(large_dir, "class" + str(i))
        print(class_path)
        pic_paths = os.listdir(class_path)
        num = len(pic_paths)
        tnum += num
        print(num)
    print(tnum)


if __name__ == '__main__':
    if os.path.exists("../../../mnt/nfs/wyx/large/") is False:
        os.mkdir("../../../mnt/nfs/wyx/large/")

    points = generate_class_data()
    # 打印结果
    for point in points:
        print(f"Latitude: {point[0]}, Longitude: {point[1]}")
    calculate_class_img_num()
