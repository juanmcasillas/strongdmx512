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
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder

Builder.load_file('ui.kv')

class UILayout(BoxLayout):
    pass

class StrongDMXApp(App):

    server_ip = "192.168.72.226"
    server_port = "53704"

    button_img = [
        "circle_green_none.png",   # 0
        "circle_green_up.png",     # 1
        "circle_green_down.png"    # 2
    ]

    def build(self):
        return UILayout()

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


if __name__ == "__main__":
    StrongDMXApp().run()
