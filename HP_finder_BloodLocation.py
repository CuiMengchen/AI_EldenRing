import numpy as np
import cv2
from Screen_Graber import capture_window
import time


# 方法一：灰度化血条
# 弃用版本，灰度化血量精准度不够
# def health_bar_count(health_bar_gray):
#     # 血量条颜色较暗，调整阈值以适应实际情况
#     health_pixels = np.count_nonzero(health_bar_gray < 45)
#     total_pixels = health_bar_gray.size
#     health_percentage = (health_pixels / total_pixels) * 100
#     return health_percentage


# 方法二：将血量条图像从BGR颜色空间转换到HSV颜色空间
def calculate_health_percentage(health_bar_img, color_low, color_high):
    # 将图像转换到HSV颜色空间
    hsv_img = cv2.cvtColor(health_bar_img, cv2.COLOR_BGR2HSV)
    # 创建一个掩膜，选出指定颜色范围内的像素
    mask = cv2.inRange(hsv_img, color_low, color_high)
    # 计算掩膜中的白色像素数量
    white_pixels = cv2.countNonZero(mask)
    # 计算血条的总像素数量
    total_pixels = np.prod(health_bar_img.shape[:2])
    # 返回白色像素占总像素的百分比
    return (white_pixels / total_pixels) * 100


# 方法三：二值化血量条后计算白色像素点百分比
# 弃用，艾尔登法环的血条是渐变的
# def calculate_health_by_adaptive_binary(health_bar_img, display_image=True, save_image=False):
#     # 转换为灰度图像
#     gray_img = cv2.cvtColor(health_bar_img, cv2.COLOR_BGR2GRAY)
#     # 应用自适应阈值处理
#     binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#
#     # 如果需要，显示二值化后的图像
#     if display_image:
#         cv2.imshow("Binary Health Bar", binary_img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#     # 计算白色像素点数量
#     white_pixels = np.sum(binary_img == 255)
#     # 计算血量条区域的总像素数
#     total_pixels = np.prod(binary_img.shape)
#     # 计算白色像素点所占的百分比，即血量百分比
#     health_percentage = (white_pixels / total_pixels) * 100
#     return health_percentage


def main():
    window_title = "ELDEN RING™"
    player_bar_rect = (140, 85, 893, 93)  # 玩家血量条的相对坐标
    boss_bar_rect = (396, 767, 1233, 776)  # Boss血量条的相对坐标
    player_mana_bar_rect = (140, 100, 795, 104)  # 玩家蓝量条的相对坐标
    # 玩家血量HSV阈值
    player_hsv_low = np.array([0, 90, 75])
    player_hsv_high = np.array([150, 255, 125])
    # Boss血量HSV阈值
    boss_hsv_low = np.array([0, 150, 50])
    boss_hsv_high = np.array([10, 255, 200])
    # 玩家蓝量HSV阈值
    player_mana_hsv_low = np.array([90, 100, 50])
    player_mana_hsv_high = np.array([110, 255, 130])

    # # 捕获窗口图像
    # full_window_image = capture_window(window_title)
    # if full_window_image is None:
    #     print("未能捕获窗口。")
    #
    # # 裁剪血条蓝条区域并计算百分比
    # player_health_percentage = calculate_health_percentage(
    #     full_window_image[player_bar_rect[1]:player_bar_rect[3], player_bar_rect[0]:player_bar_rect[2]],
    #     player_hsv_low, player_hsv_high)
    # boss_health_percentage = calculate_health_percentage(
    #     full_window_image[boss_bar_rect[1]:boss_bar_rect[3], boss_bar_rect[0]:boss_bar_rect[2]],
    #     boss_hsv_low, boss_hsv_high)
    # player_mana_percentage = calculate_health_percentage(
    #     full_window_image[player_mana_bar_rect[1]:player_mana_bar_rect[3],
    #     player_mana_bar_rect[0]:player_mana_bar_rect[2]],
    #     player_mana_hsv_low, player_mana_hsv_high)
    #
    # # 在图像上绘制血量条和蓝量条位置的红色框
    # cv2.rectangle(full_window_image, player_bar_rect[:2], player_bar_rect[2:], (0, 0, 255), 2)
    # cv2.rectangle(full_window_image, boss_bar_rect[:2], boss_bar_rect[2:], (0, 0, 255), 2)
    # cv2.rectangle(full_window_image, player_mana_bar_rect[:2], player_mana_bar_rect[2:], (255, 0, 0), 2)
    #
    # # 输出血量百分比巨和蓝量百分比
    # print(f"Player Health: {player_health_percentage:.2f}%")
    # print(f"Boss Health: {boss_health_percentage:.2f}%")
    # print(f"Player Mana: {player_mana_percentage:.2f}%")
    #
    # # 显示带有红色框的血量条和蓝量条图像
    # cv2.imshow('Health Bars', full_window_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 循环没0.5秒捕获一次图像并输出当时boss与玩家血量百分比
    try:
        while True:
            # 捕获窗口图像
            full_window_image = capture_window(window_title)
            if full_window_image is None:
                print("未能捕获窗口。")
                continue

            # 裁剪血条蓝条区域并计算百分比
            player_health_percentage = calculate_health_percentage(
                full_window_image[player_bar_rect[1]:player_bar_rect[3], player_bar_rect[0]:player_bar_rect[2]],
                player_hsv_low, player_hsv_high)
            boss_health_percentage = calculate_health_percentage(
                full_window_image[boss_bar_rect[1]:boss_bar_rect[3], boss_bar_rect[0]:boss_bar_rect[2]],
                boss_hsv_low, boss_hsv_high)
            player_mana_percentage = calculate_health_percentage(
                full_window_image[player_mana_bar_rect[1]:player_mana_bar_rect[3], player_mana_bar_rect[0]:player_mana_bar_rect[2]],
                player_mana_hsv_low, player_mana_hsv_high)

            # # 在图像上绘制血量条和蓝量条位置的红色框
            # cv2.rectangle(full_window_image, player_bar_rect[:2], player_bar_rect[2:], (0, 0, 255), 2)
            # cv2.rectangle(full_window_image, boss_bar_rect[:2], boss_bar_rect[2:], (0, 0, 255), 2)
            # cv2.rectangle(full_window_image, player_mana_bar_rect[:2], player_mana_bar_rect[2:], (255, 0, 0), 2)

            # 输出血量百分比巨和蓝量百分比
            print(f"Player Health: {player_health_percentage:.2f}%")
            print(f"Boss Health: {boss_health_percentage:.2f}%")
            print(f"Player Mana: {player_mana_percentage:.2f}%")

            # # 显示带有红色框的血量条和蓝量条图像
            # cv2.imshow('Health Bars', full_window_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            time.sleep(0.5)  # 控制循环速度，每次循环间隔0.5秒

    except KeyboardInterrupt:
        print("Loop stopped by user.")


if __name__ == "__main__":
    main()
