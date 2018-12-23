#-*- coding:utf-8 -*-
"""
Author: @Z4HD
Only can run on Windows 7+
"""
import random
import json
import sys
import os
import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.config import Config
kivy.require('1.10.0')

# 加载设置和初始化
rCount = 1
if getattr(sys, 'frozen', False):  # we are running in a |PyInstaller| bundle
    basedir = sys._MEIPASS
    Config.set('kivy', 'log_level', 'info')  # disable debug mode
else:  # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)
    Config.set('kivy', 'log_level', 'debug')  # enable debug mode

try:
    with open(
            os.path.normpath(basedir + '\\ui.kv'), 'r',
            encoding='UTF-8') as f1:
        kv_str = f1.read()
except FileNotFoundError:
    Logger.critical("Kv Loader: 无法读取ui.kv，文件可能不存在或被其他程序占用。")
    raise
try:
    with open('config.json', mode='r', encoding='UTF-8') as f2:
        conf = json.loads(f2.read())
except FileNotFoundError:
    Logger.critical("Config Loader: 无法读取config.json，文件可能不存在或被其他程序占用。")
    input('按任意键退出...')
    raise
except json.JSONDecodeError:
    Logger.critical("Config Loader: 无法加载config.json，文件可能存在语法错误。")
    input('按任意键退出...')
    raise
else:
    Logger.info("Config Loader: config loaded!")


def getRandomInt(a, b, noInts):
    bol = True
    while bol:
        re = random.randint(a, b)
        if noInts:
            for noInt in noInts:
                if re == noInt:
                    bol = True
                    break
            else:
                bol = False
        else:
            bol = False
    return re


# 构建主窗体


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # self.ids['powSlider'].bind(value=self.svColor)
        Window.bind(on_key_down=self._on_key_down)
        self.exitMsgBox = Factory.ExitPopup()

    global conf
    avoidList = ListProperty(conf['delList'])  # set black list

    def _on_key_down(self, keyboard, keycode, text, modifiers, *args):
        global rCount
        Logger.debug("KBC :keyboard: %s" % keyboard)
        Logger.debug("KBC :keycode: %s" % keycode)
        # q & esc to exit
        if keycode == 113 or keycode == 27:
            try:
                if self.exitMsgBox.status == 'open':
                    self.exitMsgBox.dismiss()
                else:
                    self.exitMsgBox.open()
            except AttributeError:
                self.exitMsgBox.open()
            return True
        # enter to start a rand process
        elif keycode == 271 or keycode == 13 or keycode == 32:
            if rCount != 1:
                Logger.info("KBC :a rand_ex() process already running")
                return
            else:
                Logger.info(
                    "KBC :a rand_ex() process start by <Enter> or <Space>")
                self.startBtnClick()

    def startBtnClick(self):
        global rCount
        rCount = 1
        Logger.info("BTN: Start btn Pressed!")
        self.rand_ex()

    def rand_ex(self):
        global rCount
        global conf
        # 按id获取控件实例
        sb1 = self.ids['startBtn']
        pow1 = self.ids['powSlider'].value
        lb = self.ids['numberLabel']
        powBox = self.ids['powBox']
        pLabel = self.ids['proverbLabel']
        # 开始设置
        powBox.disabled = True
        sb1.disabled = True
        pLabel.text = ''
        lb.text = str(
            getRandomInt(conf['randomRange'][0], conf['randomRange'][1],
                         self.avoidList))  # Get random INT
        if rCount == pow1:
            # 结束设置
            rCount = 1
            powBox.disabled = False
            sb1.disabled = False
            pLabel.text = random.choice(conf['proverb'])
            return False
        else:
            rCount += 1
        Clock.schedule_once(lambda xx: self.rand_ex())

    def svColor(self, *args):
        #ss = self.ids['powSlider']
        v = self.ids['powSlider'].value
        lb = self.ids['powLabel']
        Logger.debug("svColor: init with %s,args:%s" % (v, args))
        if v < 25:
            lb.color = [255, 1, 1, 1]
        elif v >= 25 and v < 50:
            lb.color = [116, 60, 181, 1]
        elif v >= 50 and v <= 75:
            lb.color = [1, 103, 255, 1]
        elif v > 75:
            lb.color = [38, 255, 217, 1]
        else:
            Logger.warning("powSlider: 无法匹配到配色规则，value=%s" % v)


class MainApp(App):
    """
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.mainBox1 = MainWidget()
    """

    def build(self):
        global conf
        Config.set('kivy', 'exit_on_escape', 0)
        Config.set('kivy', 'default_font', [
            'WenQuanYi',
            os.path.normpath(basedir + '\\fonts\\wqy-microhei.ttc')
        ])
        # 野蛮Kivy API参考坑害我。Must be one of: [True, False, 'auto', 'fake']
        Window.fullscreen = conf['fullscreen']
        Window.size = tuple(conf['size'])
        self.title = "Kv科技为了我，巨大多抽号脚本。的确随机春欠缺，考英文无药可救。"
        return MainWidget()


def main():
    Builder.load_string(kv_str)  # 载入界面配置文件，必须在App（）实例化之前载入。
    MainApp().run()


if __name__ == '__main__':
    main()
