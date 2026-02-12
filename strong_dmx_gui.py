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
from kivy.clock import Clock

from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from strong_dmx import DMXPacket, LampClient

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
            # start the app idle loop
            self.pwd.text = ""
            self.app.create_client()
    
class mainWindow(Screen):
    pass


kv = Builder.load_file('ui.kv')

class StrongDMXApp(App):

    server_ip = "192.168.72.226"
    server_ip = "192.168.1.92"
    server_port = "53704"

    button_rearm_color = (50/88, 50/88, 0.0, 1.0)
    button_stop_color = (255/88, 0.0, 0.0, 1.0)
    button_img = [
        "res/img/circle_green_none.png",   # 0
        "res/img/circle_green_up.png",     # 1
        "res/img/circle_green_down.png"    # 2
    ]
    button_state_cmd = { 0: 'none', 1: 'up', 2: 'down' }

    def build(self):
        self.sm = ScreenManager()
        lw = loginWindow(name='loginWindow')
        lw.app = self        
        self.sm.add_widget(lw)
        self.sm.add_widget(mainWindow(name='mainWindow'))
        return self.sm

    def change_button(self, button):
        button.my_state = (button.my_state + 1) % 3
        button.background_normal = self.button_img[ button.my_state  ]
        button.background_down = self.button_img[ button.my_state  ]

    def change_stop_rearm_button(self, button):

        mw = self.sm.get_screen("mainWindow")
        if button.my_state == 0:
            # STOP button
            button.background_color = self.button_rearm_color
            button.text = "REARM"
            self.destroy_client()
            print("stopping")
            mw.ids.go_button.disabled = True

        if button.my_state == 1:
            # REARM button
            print("rearm")
            button.background_color = self.button_stop_color
            button.text = "STOP"
            self.create_client()
            mw.ids.go_button.disabled = False
        
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
            self.destroy_client()
            self.create_client()

    ## manager interface
    def destroy_client(self):
        Clock.unschedule(self.client.schedule)
        self.client.disconnect()
        del self.client

    def create_client(self):
        self.client = LampClient(
            src_addr = "0.0.0.0", 
            dst_addr = self.server_ip,
            dst_port = int(self.server_port)
            )
        self.client.connect()
        self.client.schedule = Clock.schedule_interval(self.client.send_keep_alive, self.client.wait_time)
        print("create client done")

    def start_sending_commands(self):
        mw = self.sm.get_screen("mainWindow")
        
        config = [ 
                ( 1, self.button_state_cmd[mw.ids.button_1.my_state] ),
                ( 2, self.button_state_cmd[mw.ids.button_2.my_state] ),
                ( 3, self.button_state_cmd[mw.ids.button_3.my_state] ),
        ]
        Clock.unschedule(self.client.schedule)
        self.client.packet = DMXPacket.cmd(config)
        self.client.schedule = Clock.schedule_interval(self.client.send_cmd_internal, self.client.wait_time)
        

    def stop_sending_commands(self):
        Clock.unschedule(self.client.schedule)
        self.client.schedule = Clock.schedule_interval(self.client.send_keep_alive, self.client.wait_time)

if __name__ == "__main__":
    StrongDMXApp().run()
