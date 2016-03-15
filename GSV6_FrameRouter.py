# -*- coding: utf-8 -*-
__author__ = 'Dennis Rump'
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Dennis Rump
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

import logging
import threading
from Queue import Queue
from GSV6_MessFrameHandler import MessFrameHandler

class FrameRouter(threading.Thread):
    lock = threading.Lock()

    #def __init__(self, frameQueue, antwortQueue, messertRotatingQueue, gsv6Lib):
    def __init__(self, frameQueue, antwortQueue, _lastMesswert, gsv6Lib):
        threading.Thread.__init__(self)
        self.frameQueue = frameQueue
        self.antwortQueue = antwortQueue
        # self.messertRotatingQueue = messertRotatingQueue
        self.lastMesswert = _lastMesswert
        self.gsv6 = gsv6Lib
        self.running = False

        # self.messFrameEventHandler = MessFrameHandler(self.messertRotatingQueue, self.gsv6)
        self.messFrameEventHandler = MessFrameHandler(self.lastMesswert, self.gsv6)
        # self.antwortFrameEventHandler = AntwortFrameHandler(self.gsv6, self.antwortQueue, self.messFrameEventHandler)

        # fallback, this flag kills this thread if main thread killed
        self.daemon = True

    def run(self):
        # arbeits Thread: router -> routen von AntwortFrames und MessFrames
        FrameRouter.lock.acquire()
        self.running = True
        FrameRouter.lock.release()
        logging.getLogger('gsv8.FrameRouter').info('started')

        # enter rooter loop
        while self.running:
            try:
                # newFrame = self.frameQueue.popleft()
                newFrame = self.frameQueue.get()
            except IndexError:
                pass
            except Queue.Empty:
                pass
            else:
                logging.getLogger('gsv8.FrameRouter').debug('new Frame: ' + newFrame.toString())
                if newFrame.getFrameType() == 0:
                    # MesswertFrame
                    logging.getLogger('gsv8.FrameRouter').debug('Messwert erhalten')
                    self.messFrameEventHandler.computeFrame(newFrame)
                elif newFrame.getFrameType() == 1:
                    logging.getLogger('gsv8').debug("Antwort eralten.")
                    # AntwortFrame
                    # self.antwortFrameEventHandler.computeFrame(newFrame)
                    self.antwortQueue.put(newFrame)
                else:
                    # error
                    logging.getLogger('gsv8.FrameRouter').debug(
                        'nothing to do with an FrameType != Messwert/Antwort')

        logging.getLogger('gsv8.FrameRouter').debug('exit')

    def stop(self):
        FrameRouter.lock.acquire()
        self.running = False
        FrameRouter.lock.release()

    def startCSVRecording(self, csvFilepath, prefix):
        self.messFrameEventHandler.startRecording(csvFilepath, prefix)

    def stopCSVRecording(self):
        self.messFrameEventHandler.stopRecording()

    def isRecording(self):
        return self.messFrameEventHandler.doRecording