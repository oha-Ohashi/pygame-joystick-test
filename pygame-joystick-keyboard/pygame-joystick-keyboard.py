#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et
#
# This tool runs fine on both Python 2 and Python 3.
#
# https://github.com/denilsonsa/pygame-joystick-test

from __future__ import division
from __future__ import print_function

import sys, math
import pygame
from pygame.locals import *
import json, pyautogui


class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes    = self.joy.get_numaxes()
        self.numballs   = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats    = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


class input_test(object):
    class program:
        "Program metadata"
        name    = "Pygame Joystick Test"
        version = "0.2"
        author  = "Denilson Figueiredo de Sá Maia"
        nameversion = name + " " + version

    def init(self):
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))

    def run(self):
        atb = axis_to_btn()
        output = output_key()
        while True:
            # self.clock.tick(30)
            for event in [pygame.event.wait(), ] + pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
                    self.quit()
                #elif event.type == VIDEORESIZE:
                #    self.screen = pygame.display.set_mode(event.size, RESIZABLE)
                elif event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    #print(event.axis, end=' ')
                    #print(event.value)
                    LR = atb.print_lili([
                        self.joy[event.joy].axis[0],
                        self.joy[event.joy].axis[1]
                    ],[
                        self.joy[event.joy].axis[2],
                        self.joy[event.joy].axis[3]
                    ])
                    if(LR != None):
                        print(LR, end="  ")
                        output.type_stick(LR)
                elif event.type == JOYBALLMOTION:
                    self.joy[event.joy].ball[event.ball] = event.rel
                elif event.type == JOYHATMOTION:
                    self.joy[event.joy].hat[event.hat] = event.value
                    print(event.hat, end=' ')
                    print(event.value)
                elif event.type == JOYBUTTONUP:
                    self.joy[event.joy].button[event.button] = 0
                elif event.type == JOYBUTTONDOWN:
                    self.joy[event.joy].button[event.button] = 1
                    print(event.button, end='  ')
                    output.type_botton(event.button)


    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)

class axis_to_btn:
    pre_axis = [0,0]
    now_axis = [0,0]

    def print_mimi(self, xy):
        self.now_axis = list(map(self.polen, xy))
        if(self.pre_axis != self.now_axis):

            print(self.now_axis)
            self.pre_axis = self.now_axis
    
    def polen(self, x):
        if (x > 0.3):
            return 1
        elif(x > -0.3):
            return 0
        else:
            return -1
    
    naname_flag = False
    def print_lili(self, Lxy, Rxy):
        if(not self.naname_flag and self.dist_enough(Rxy)):
            LR = {
                'L': self.stick8(Lxy),
                'R': self.stick8(Rxy)
            }
            #print (LR)
            self.naname_flag = True
            return LR
        elif(self.naname_flag and not self.dist_enough(Rxy)):
            #print(Rxy)
            self.naname_flag = False

    def dist_enough(self, xy):
        if xy[0]**2 + xy[1]**2 > 0.5:
            return True
        else: 
            return False

    def stick8(self, xy):
        if(not self.dist_enough(xy)):
            return 0
        deg360 = math.degrees(math.atan2(xy[1], xy[0])) + 179
        print (deg360)
        deg8 = self.deg8(deg360)
        return deg8
    def deg8(self, x):
        if ( x<22.5 or x >(360-22.5)):
            res = 0
        else:
            x = x - 22.5
            res = int( x//45 + 1)
        return res + 1

class output_key:
    with open("keymap.json", mode="r") as f:
        keymap = json.load(f)

    def type_botton(self, index):
        c = self.keymap['buttons'][index]
        print(c)
        pyautogui.press(c)
    
    def type_stick(self, LR):
        c = self.keymap['sticks'][LR['L']][LR['R']]
        print(c)
        pyautogui.press(c)
    



if __name__ == "__main__":
    print('hello')
    program = input_test()
    program.init()
    program.run()  # This function should never return
