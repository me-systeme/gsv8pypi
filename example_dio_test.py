# -*- coding: utf-8 -*-
"""
Datum 01.2016
@author: ME-Meßsysteme GmbH, Dennis Rump
@version 1.2
"""
__author__ = 'Dennis Rump'
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015 ME-Meßsysteme GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Hiermit wird unentgeltlich, jeder Person, die eine Kopie der Software
# und der zugehörigen Dokumentationen (die "Software") erhält, die
# Erlaubnis erteilt, uneingeschränkt zu benutzen, inklusive und ohne
# Ausnahme, dem Recht, sie zu verwenden, kopieren, ändern, fusionieren,
# verlegen, verbreiten, unter-lizenzieren und/oder zu verkaufen, und
# Personen, die diese Software erhalten, diese Rechte zu geben, unter
# den folgenden Bedingungen:
#
# Der obige Urheberrechtsvermerk und dieser Erlaubnisvermerk sind in
# alle Kopien oder Teilkopien der Software beizulegen.
#
# DIE SOFTWARE WIRD OHNE JEDE AUSDRÜCKLICHE ODER IMPLIZIERTE GARANTIE
# BEREITGESTELLT, EINSCHLIESSLICH DER GARANTIE ZUR BENUTZUNG FÜR DEN
# VORGESEHENEN ODER EINEM BESTIMMTEN ZWECK SOWIE JEGLICHER
# RECHTSVERLETZUNG, JEDOCH NICHT DARAUF BESCHRÄNKT. IN KEINEM FALL SIND
# DIE AUTOREN ODER COPYRIGHTINHABER FÜR JEGLICHEN SCHADEN ODER SONSTIGE
# ANSPRUCH HAFTBAR ZU MACHEN, OB INFOLGE DER ERFÜLLUNG VON EINEM
# VERTRAG, EINEM DELIKT ODER ANDERS IM ZUSAMMENHANG MIT DER BENUTZUNG
# ODER SONSTIGE VERWENDUNG DER SOFTWARE ENTSTANDEN.
#
###############################################################################

from gsv8 import gsv8
from datetime import datetime
import curses

if __name__ == '__main__':
    # construct device
    # Unix
    dev1 = gsv8("/dev/ttyACM0",115200)
    # Windows
    # dev1 = gsv8("COM26", 115200)
    # dev1 = gsv8("COM22", 115200)

    # print "test: " + ' '.join(format(x, '02x') for x in bytearray(dev1.isPinHigh(1)))

    # DIO Gruppe 1 als Input Konfigurieren ( IOPin 1..4 (1.1 - 1.4) )
    dev1.setDIOgroupToInput(1)
    # DIO Gruppe 2 als Input Konfigurieren ( IOPin 5..8 (2.1 - 2.4) )
    result = dev1.setDIOgroupToInput(2)
    # DIO Gruppe 3 als Input Konfigurieren ( IOPin 9..12 (3.1 - 3.4) )
    result = dev1.setDIOgroupToInput(3)
    # DIO Gruppe 4 als Input Konfigurieren ( IOPin 13..16 (4.1 - 4.4) )
    result = dev1.setDIOgroupToInput(4)

    # build console window
    #start
    stdscr = curses.initscr()
    # Keine Anzeige gedrückter Tasten
    curses.noecho()
    # Kein line-buffer
    curses.cbreak()
    # Escape-Sequenzen aktivieren
    stdscr.keypad(1)
    # getch nonblocking
    stdscr.nodelay(1)
    # kein curser
    curses.curs_set(0)
    # farben
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    begin_x = 0; begin_y = 0
    height = 20; width = 70
    win = curses.newwin(height, width, begin_y, begin_x)
    win.addstr(2, 2, "GSV8 DIO Inputtest")
    win.addstr(2, 40, "cycle time:")
    win.addstr(4, 4, "Pin01")
    win.addstr(4, 12, "Pin02")
    win.addstr(4, 20, "Pin03")
    win.addstr(4, 28, "Pin04")
    win.addstr(4, 36, "Pin05")
    win.addstr(4, 44, "Pin06")
    win.addstr(4, 52, "Pin07")
    win.addstr(4, 60, "Pin08")

    win.addstr(10, 4, "Pin09")
    win.addstr(10, 12, "Pin10")
    win.addstr(10, 20, "Pin11")
    win.addstr(10, 28, "Pin12")
    win.addstr(10, 36, "Pin13")
    win.addstr(10, 44, "Pin14")
    win.addstr(10, 52, "Pin15")
    win.addstr(10, 60, "Pin16")

    # dev1.startCSVrecording(10.0, './messungen')

    actTime = lastTime = datetime.now()
    diffTime = actTime - lastTime

    c = -1
    # abort while-loop by ESC
    while(c != 27):
        c = stdscr.getch()
        actTime = datetime.now()
        diffTime = actTime - lastTime

        '''
        # option 1: alle Kanaele einzeln auslesen ca. 16-17ms
        win.addstr(6,6, str(dev1.getDIOlevel(1)))
        win.addstr(6,14, str(dev1.getDIOlevel(2)))
        win.addstr(6,22, str(dev1.getDIOlevel(3)))
        win.addstr(6,30, str(dev1.getDIOlevel(4)))
        win.addstr(6,38, str(dev1.getDIOlevel(5)))
        win.addstr(6,46, str(dev1.getDIOlevel(6)))
        win.addstr(6,54, str(dev1.getDIOlevel(7)))
        win.addstr(6,62, str(dev1.getDIOlevel(8)))

        win.addstr(12,6, str(dev1.getDIOlevel(9)))
        win.addstr(12,14, str(dev1.getDIOlevel(10)))
        win.addstr(12,22, str(dev1.getDIOlevel(11)))
        win.addstr(12,30, str(dev1.getDIOlevel(12)))
        win.addstr(12,38, str(dev1.getDIOlevel(13)))
        win.addstr(12,46, str(dev1.getDIOlevel(14)))
        win.addstr(12,54, str(dev1.getDIOlevel(15)))
        win.addstr(12,62, str(dev1.getDIOlevel(16)))
        '''

        # option 2: alle Kanaele zusammen auslesen ca. 1-2ms
        tmpDIOChannels = dev1.getDIOlevel(0)
        for i in range(0, 8):
            if ((tmpDIOChannels>>i)&0x0001) == 0:
                win.addstr(6,6+(8*i), str((tmpDIOChannels>>i)&0x0001), curses.color_pair(2))
            else:
                win.addstr(6,6+(8*i), str((tmpDIOChannels>>i)&0x0001), curses.color_pair(1))


        for i in range(0, 8):
            if ((tmpDIOChannels>>(i+8))&0x0001) == 0:
                win.addstr(12,6+(8*i), str((tmpDIOChannels>>(i+8))&0x0001), curses.color_pair(2))
            else:
                win.addstr(12,6+(8*i), str((tmpDIOChannels>>(i+8))&0x0001), curses.color_pair(1))


        win.addstr(2, 52, "{:3d} ms".format(diffTime.microseconds/1000))

        lastTime = actTime
        win.refresh()

    # destruct device
    dev1 = None

    # Ende - console wiederherstellen
    curses.nocbreak()
    #stdscr.keypad(0)
    curses.echo()
    curses.endwin()
