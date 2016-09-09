# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs
import datetime
import books

#
#   Simplest renderer. Ignores everything except ascii text.
#

class SingleHTMLRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Position
        self.cb = u''    # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Currrent Verse
        self.indentFlag = False
        self.bookName = u''
        self.chapterLabel = 'Chapter'
        self.lineIndent = 0

    def render(self):
        self.loadUSFM(self.inputDir)
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        h = u"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
            <title>Bible</title>
            <style media="all" type="text/css">
            .indent-0 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-1 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-2 {
                margin-left:1em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-3 {
                margin-left:2em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .c-num {
                color:gray;
            }
            .v-num {
                color:gray;
            }
            .tetragrammaton {
                font-variant: small-caps;
            }
            </style>

        </head>
        <body>
        """
        self.f.write(h.encode('utf-8'))
        self.run()
        self.f.write('</body></html>')
        self.f.close()

    def startLI(self):
        self.lineIndent += 1
        return ur'<ul> '

    def stopLI(self):
        if self.lineIndent < 1:
            return u''
        else:
            self.lineIndent -= 1
            return ur'</ul>'

    def escape(self, s):
        return s.replace(u'~',u'&nbsp;')

    def write(self, unicodeString):
        self.f.write(unicodeString.replace(u'~', u' '))

    def writeIndent(self, level):
        self.write(u'\n\n')
        if level == 0:
            self.indentFlag = False
            self.write(u'<p class="indent-0">')
            return
        if not self.indentFlag:
            self.indentFlag = True
            self.write(u'<p>')
        self.write(u'<p class="indent-' + str(level) + u'">')

    def renderID(self, token):
        self.cb = books.bookKeyForIdValue(token.value)
        self.indentFlag = False
        self.write(u'\n\n<h1 id="' + self.cb + u'"></h1>\n')
    def renderH(self, token):       self.bookname = token.value
    def renderTOC2(self, token):
        self.write(u'\n\n<h1>' + token.value + u'</h1>')
    def renderMT(self, token):
        return; #self.write(u'\n\n<h1>' + token.value + u'</h1>') # removed to use TOC2
    def renderMT2(self, token):     self.write(u'\n\n<h2>' + token.value + u'</h2>')
    def renderMT3(self, token):     self.write(u'\n\n<h2>' + token.value + u'</h2>')
    def renderMS1(self, token):     self.write(u'\n\n<h3>' + token.value + u'</h3>')
    def renderMS2(self, token):     self.write(u'\n\n<h4>' + token.value + u'</h4>')
    def renderP(self, token):
        self.indentFlag = False
        self.write(self.stopLI() + u'\n\n<p>')
    def renderPI(self, token):
        self.indentFlag = False
        self.write(self.stopLI() + u'\n\n<p class"indent-2">')
    def renderM(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p>')
    def renderS1(self, token):
        self.indentFlag = False
        self.write(u'\n\n<h5>' + token.getValue() + u'</h5>')
    def renderS2(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p align="center">----</p>')
    def renderC(self, token):
        self.cc = token.value.zfill(3)
        self.write(self.stopLI() + u'\n\n<h2 class="c-num">'+self.chapterLabel+' ' + token.value + u'</h2>')
    def renderV(self, token):
        self.cv = token.value.zfill(3)
        self.write(u' <span class="v-num"><sup><b>' + token.value + u'</b></sup></span>')
    def renderWJS(self, token):     self.write(u'<span class="woc">')
    def renderWJE(self, token):     self.write(u'</span>')
    def renderTEXT(self, token):    self.write(u" " + self.escape(token.value) + u" ")
    def renderQ(self, token):       self.writeIndent(1)
    def renderQ1(self, token):      self.writeIndent(1)
    def renderQ2(self, token):      self.writeIndent(2)
    def renderQ3(self, token):      self.writeIndent(3)
    def renderNB(self, token):      self.writeIndent(0)
    def renderB(self, token):       self.write(self.stopLI() + u'\n\n<p class="indent-0">&nbsp;</p>')
    def renderIS(self, token):      self.write(u'<i>')
    def renderIE(self, token):      self.write(u'</i>')
    def renderNDS(self, token):     self.write(u'<span class="tetragrammaton">')
    def renderNDE(self, token):     self.write(u'</span>')
    def renderPBR(self, token):     self.write(u'<br />')
    def renderSCS(self, token):     self.write(u'<b>')
    def renderSCE(self, token):     self.write(u'</b>')
    def renderFS(self, token):      self.write(u'[Note: ')
    def renderFT(self, token):      self.write(token.value)
    def renderFE(self, token):      self.write(u'')
    def renderQSS(self, token):     self.write(u'<i>')
    def renderQSE(self, token):     self.write(u'</i>')
    def renderEMS(self, token):     self.write(u'<i>')
    def renderEME(self, token):     self.write(u'</i>')
    def renderE(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p>' + token.value + '</p>')

    def renderPB(self, token):     pass
    def renderPERIPH(self, token):  pass

    def renderLI(self, token):       self.f.write( self.startLI() )
    def renderLI1(self, token):      self.f.write( self.startLI() )
    def renderLI2(self, token):      self.f.write( self.startLI() )
    def renderLI3(self, token):      self.f.write( self.startLI() )

    def renderS5(self, token):
        self.write(u'\n<span class="chunk-break"/>\n')
    def renderCL(self, token):       self.chapterLabel = token.value
    def renderQR(self, token):       self.write(u'')
    def renderFQA(self, token):      self.write(u'] ' + token.value)
    def renderFQB(self, token):      self.write(u': ' + token.value)
