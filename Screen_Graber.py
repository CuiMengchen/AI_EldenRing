import pygetwindow as gw
import pyautogui
from PIL import Image
import matplotlib.pyplot as plt
#
# # 步骤1：找到目标应用窗口
# target_window = gw.getWindowsWithTitle('ELDEN RING™')[0]
#
# # 步骤2：获取窗口的位置和尺寸
# if target_window:
#     left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height
#
#     # 步骤3：捕获指定区域的屏幕图像
#     screenshot = pyautogui.screenshot(region=(left, top, width, height))
#
#     # 步骤4：使用PIL显示图像
#     screenshot.show()
#     # 或者使用matplotlib显示图像
#     # plt.imshow(screenshot)
#     # plt.show()
# else:
#     print("未找到目标窗口。")

import numpy as np
import win32gui, win32ui, win32con, win32api
import pygetwindow as gw
import matplotlib.pyplot as plt
import cv2


def capture_window(window_title):
    target_window = None
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        target_window = windows[0]
    else:
        print("未找到目标窗口。")
        return None

    if target_window:
        # 获取窗口的位置和尺寸
        left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height

        # 设置捕获区域
        region = (left, top, left + width, top + height)

        # 开始捕获
        hwin = win32gui.GetDesktopWindow()
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (height, width, 4)

        # 清理资源
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return img

window_title = "ELDEN RING™"
img = capture_window(window_title)
if img is not None:
    # 将BGRA转换为RGBA
    print("图像捕获成功，图像尺寸：", img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    # 显示图像
    plt.figure(figsize=(10, 8))  # 可以根据需要调整图片大小
    plt.imshow(img)
    plt.axis('off')  # 不显示坐标轴
    plt.show()
