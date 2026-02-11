##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // test_k.py 
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
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder

Builder.load_file('ui.kv')

class TestK01App(App):
    def build(self):
        return Button(text="Hi",
                      background_color = ( 0,0, 1,1 ),
                      font_size=150)


if __name__ == "__main__":
    TestK01App().run()




class StrongDMX(App):
    def build(self):
       pass


if __name__ == "__main__":
    StrongDMX().run()
