##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // test_ui.py 
# //
# // sample test for kivy
# //
# // 10/02/2026 08:22:56  
# // (c) 2026 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

__version__ = "1.0.1" 

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


PASSWORD = "1234"

# class to call the popup function

def popFun():
    show = P()
    window = Popup(title = "Warning", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()

class PopupWindow(Widget):
    def btn(self):
        popFun()

# class to build GUI for a popup window
class P(FloatLayout):
    pass
# class to accept user info and validate it

class loginWindow(Screen):
    global PASSWORD

    pwd = ObjectProperty(None)
    def validate(self):

        # validating if the email already exists 
        if self.pwd.text is None or self.pwd.text != PASSWORD:
            popFun()
        else:
            # switching the current screen to display validation result
            self.manager.current = 'mainWindow'

            # reset TextInput widget
            self.pwd.text = ""

class mainWindow(Screen):
    pass






kv = Builder.load_file('ui.kv')

class StrongDMXApp(App):

    server_ip = "192.168.72.226"
    server_port = "53704"

    button_rearm_color = (50/88, 50/88, 0.0, 1.0)
    button_stop_color = (255/88, 0.0, 0.0, 1.0)
    button_img = [
        "res/img/circle_green_none.png",   # 0
        "res/img/circle_green_up.png",     # 1
        "res/img/circle_green_down.png"    # 2
    ]

    def build(self):
        sm = ScreenManager()
        sm.add_widget(loginWindow(name='loginWindow'))
        sm.add_widget(mainWindow(name='mainWindow'))
        return sm

    pass
    def commands(self, obj):
        pass
    def settings(self, obj):
        pass
    def about(self, obj):
        pass

    def change_button(self, button):
        button.my_state = (button.my_state + 1) % 3
        button.background_normal = self.button_img[ button.my_state  ]
        button.background_down = self.button_img[ button.my_state  ]

    def change_stop_rearm_button(self, button):
        
        if button.my_state == 0:
            # STOP button
            print("stopping")
            button.background_color = self.button_rearm_color
            button.text = "REARM"
            
        if button.my_state == 1:
            # REARM button
            print("rearm")
            button.background_color = self.button_stop_color
            button.text = "STOP"
        
        button.my_state = (button.my_state + 1) % 2
        
    def apply_settings(self,ip, port):
        port_i = None
        try:
            port_i = int(port.text)
        except:
            popFun()

        if not ip or not port or ip.text == "" or port.text == "": 
            popFun()
        else:
            self.server_ip = ip.text
            self.server_port = port_i
            # close and open again
            

if __name__ == "__main__":
    StrongDMXApp().run()
