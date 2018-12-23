# -*- coding:utf-8 -*-
"""
Author: @Z4HD
Only can run on Windows 7+
"""
import json
import os
import pprint
import random
import sys

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
# from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.10.0')
versionStr = "v251"
Logger.info("randEX: Version: "+versionStr)

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
    Logger.critical("conf Loader: 无法读取config.json，文件可能不存在或被其他程序占用。")
    input('按任意键退出...')
    raise
except json.JSONDecodeError:
    Logger.critical("conf Loader: 无法加载config.json，文件可能存在语法错误。")
    input('按任意键退出...')
    raise
else:
    Logger.info("conf Loader: config loaded!")

# Random tools

class ZRandom():
    '''
    Provider -> Handler -> get()
    '''

    def __init__(self, config):
        """
        config: json dict about RandomProvider
        """
        self.config = config
        self.avoidList = []
        if self.config['type'] == 'range':
            self.randomList = self._rangeProvider()
        else:
            raise ValueError('Unsupport provider type')
        # highlighting
        self.randomList = self._highlightHandler(self.randomList)

    def _fileProvider(self, parameter_list):
        "TODO: get random objs from file"
        pass

    def _rangeProvider(self):
        rangeSettings = self.config['rangeSettings']
        rl = range(rangeSettings['range'][0], rangeSettings['range'][1])
        rl = list(rl)
        return rl

    def _highlightHandler(self, rl):
        if self.config.setdefault('Highlights'):
            self.HighlightsSettings = self.config['Highlights']
            for h in self.config['Highlights']:
                # 超级加倍
                if h.setdefault('quantity'):
                    i = int(h['quantity'])
                    if i < -1:
                        raise ValueError(
                            "[%s]'s quantity must >= 0" % h['obj'])
                    elif i == -1:
                        rl.remove(h['obj'])
                        self.avoidList.append(h['obj'])
                    elif i == 0:
                        pass
                    elif i > 0:
                        while i != 0:
                            rl.append(h['obj'])
                            i -= 1
        else:
            self.HighlightsSettings = None
        return rl

    def getObj(self):
        'Return a random obj'
        r = random.choice(self.randomList)
        return r

    def getProverb(self, randomObj=None):
        '''
        Return a proberb str.
        randomObj only use to get priv_proverbs
        '''
        r = random.choice(self.config['proverbs'])
        if self.HighlightsSettings:
            for h in self.HighlightsSettings:
                if randomObj == str(h['obj']):
                    if h.setdefault('priv_proverbs'):
                        r = random.choice(h['priv_proverbs'])
        return r


# 构建主窗体


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # self.ids['powSlider'].bind(value=self.svColor)
        Window.bind(on_key_down=self._on_key_down)
        self.exitMsgBox = Factory.ExitPopup()
        self.debugMsgBox = Factory.DebugPopup()
        try:
            self.zr = ZRandom(conf['RandomProvider'])
        except KeyError as e:
            Logger.critical("ZRandom: " + pprint.pformat(e))
            raise
        if self.zr.avoidList:
            Logger.info('ZRandom: %s has been removed.' % self.zr.avoidList)
        # self.debugMsgBox.text = pprint.pformat(self.zr.HighlightsSettings)

    global conf
    global versionStr
    version = versionStr

    def _on_key_down(self, keyboard, keycode, text, modifiers, *args):
        global rCount
        Logger.debug("KBC: keyboard: %s" % keyboard)
        Logger.debug("KBC: keycode: %s" % keycode)
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
                Logger.info("KBC: a rand_ex() process already running")
                return
            else:
                Logger.info(
                    "KBC: a rand_ex() process start by <Enter> or <Space>")
                self.startBtnClick()
        elif keycode == 100:
            try:
                if self.debugMsgBox.status == 'open':
                    self.debugMsgBox.dismiss()
                else:
                    self.debugMsgBox.open()
            except AttributeError:
                self.debugMsgBox.open()
            return True

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
        lb.text = str(self.zr.getObj())  # Get random INT
        if rCount == pow1:
            # 结束设置
            rCount = 1
            powBox.disabled = False
            sb1.disabled = False
            pLabel.text = self.zr.getProverb(lb.text)
            return False
        else:
            rCount += 1
        Clock.schedule_once(lambda xx: self.rand_ex())

    def svColor(self, *args):
        # ss = self.ids['powSlider']
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

    def set_debug_text(self, popup):
        popup.ids['debugText'].text = json.dumps(
            conf['RandomProvider']['Highlights'], indent=4, ensure_ascii=False)


def main():
    Builder.load_string(kv_str)  # 载入界面配置文件，必须在App（）实例化之前载入。
    MainApp().run()


if __name__ == '__main__':
    main()
