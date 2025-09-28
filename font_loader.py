# -*- coding: utf-8 -*-
"""
字体初始化模块 - 在应用启动时自动加载自定义字体，确保UI能够正常使用腾祥嘉丽大圆简字体
"""

import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets


def _load_font_from_resource(font_db):
    """
    尝试从资源文件加载字体
    """
    try:
        font_data = QtCore.QFile(":/res/TengXiangJiaLiDaYuanJian-1.ttf")
        if font_data.open(QtCore.QIODevice.ReadOnly):
            data = font_data.readAll()
            font_id = font_db.addApplicationFontFromData(data)
            if font_id != -1:
                font_families = font_db.applicationFontFamilies(font_id)
                if font_families and "腾祥嘉丽大圆简" in font_families:
                    print("成功从资源文件加载字体: 腾祥嘉丽大圆简")
                    return True
    except Exception as e:
        print(f"从资源加载字体失败: {e}")
    return False

def _get_font_paths():
    """
    获取所有可能的字体文件路径
    """
    font_paths = [
        "res/TengXiangJiaLiDaYuanJian-1.ttf",
        os.path.join(os.path.dirname(__file__), "res", "TengXiangJiaLiDaYuanJian-1.ttf"),
    ]
    if hasattr(sys, '_MEIPASS'):
        font_paths.append(os.path.join(sys._MEIPASS, "res", "TengXiangJiaLiDaYuanJian-1.ttf"))
    return font_paths

def _load_font_from_filesystem(font_db):
    """
    尝试从文件系统加载字体
    """
    font_paths = _get_font_paths()
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                font_id = font_db.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = font_db.applicationFontFamilies(font_id)
                    print(f"从文件加载字体，字体家族: {font_families}")
                    if font_families:
                        print(f"成功从文件加载字体: {font_path}")
                        return True
        except Exception as e:
            print(f"从文件 {font_path} 加载字体失败: {e}")
    return False

def _print_available_chinese_fonts(font_db):
    """
    打印可用的中文字体，帮助调试
    """
    available_families = font_db.families()
    chinese_fonts = [f for f in available_families if any(ord(c) > 127 for c in f)]
    print(f"可用的中文字体: {chinese_fonts[:10]}")  # 只显示前10个

def load_custom_fonts():
    """
    加载自定义字体
    这个函数会在应用启动时被调用，将字体文件加载到系统中
    """
    font_db = QtGui.QFontDatabase()
    font_loaded = _load_font_from_resource(font_db)
    if not font_loaded:
        font_loaded = _load_font_from_filesystem(font_db)
    if not font_loaded:
        print("警告: 无法加载腾祥嘉丽大圆简字体，将使用系统默认字体")
        _print_available_chinese_fonts(font_db)
    return font_loaded


def setup_high_dpi():
    """
    设置高DPI支持，解决4K屏幕缩放问题
    必须在创建QApplication之前调用
    """
    # 启用高DPI缩放
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # 使用高DPI像素图
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    # 设置高DPI缩放策略
    if hasattr(QtCore.Qt, 'AA_DisableWindowContextHelpButton'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton, True)


def init_application():
    """
    初始化应用程序
    设置高DPI支持和字体加载
    """
    # 设置高DPI支持（必须在QApplication创建之前）
    setup_high_dpi()
    
    print("正在初始化应用程序...")
    return True


def init_fonts_after_app():
    """
    在QApplication创建后初始化字体
    """
    print("正在加载自定义字体...")
    font_loaded = load_custom_fonts()
    return font_loaded