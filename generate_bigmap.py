import math
import os.path
import time
from PIL import Image
from selenium import webdriver


# 生成大地图
def generate_bigmap(lat, lon, dir):
    # 谷歌浏览器设置
    zoom = "0a,1700d,35y,0h,0t,0r"
    DRIVER = 'chromedriver'

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    # option.add_argument('start-maximized')

    driver = webdriver.Chrome(executable_path=DRIVER, options=option)  # 调用带参数的谷歌浏览器
    driver.set_window_size(1800, 1400)  # 自定义窗口大小

    if os.path.exists(dir) is False:
        os.mkdir(dir)

    # 大地图1000米*1000米，相邻大地图中心点距离600米，重复400米，以覆盖一张图像300米
    # 需要保证放大到300米能看清；需要保证相邻大地图重复超过300米，才能覆盖一张图像300米

    lat_diff = (500 + 500 - 400) / 111000

    # 南北方向92个大地图，相邻大地图中心点距离600m
    for i in range(0, 92):
        print(i)
        center_lat = round(lat - i * lat_diff, 6)

        # 东西方向34个大地图，相邻大地图中心点距离600m
        for j in range(0, 34):
            lon_diff = (500 + 500 - 400) / 111000 / math.cos(center_lat / 180 * math.pi)
            center_lon = round(lon + j * lon_diff, 6)

            coords = str(center_lat) + "," + str(center_lon)
            path = dir + str(i * 34 + j) + "," + coords + '.png'

            if os.path.exists(path):
                continue

            # 调用浏览器，输入url
            url = "https://earth.google.com/web/@" + coords + "," + zoom
            driver.get(url)

            time.sleep(10)
            # driver.quit()
            # 保存截图
            driver.save_screenshot(path)

            # 裁剪图片
            pic = Image.open(path)
            w, h = pic.size
            pic = pic.crop((w // 2 - 700, h // 2 - 700, w // 2 + 700, h // 2 + 700))
            pic.save(path)


if __name__ == '__main__':
    # 大地图和截取路径是两套东西，互不干扰
    # 大地图1000米*1000米，相邻大地图中心点距离600米，重复400米
    # 需要保证放大到300米能看清；需要保证相邻大地图重复超过300米，才能覆盖一张图像300米

    # 40km * 15km
    # 左上角23.8, 120.2
    # 右上角：23.8, 120.4
    # 左下角：23.3, 120.2
    # 右下角：23.3, 120.4
    if os.path.exists("../../../mnt/nfs/wyx/large/") is False:
        os.mkdir("../../../mnt/nfs/wyx/large/")
    # generate_bigmap(lat=23.8, lon=120.2, dir="../../../mnt/nfs/wyx/bigmap/")
