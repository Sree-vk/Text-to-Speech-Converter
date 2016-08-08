#!/usr/bin/python

import sys  #for cmd line argv
import time #for delay
import pygst    #for playing mp3 stream
import gst      #" "
#import os   #for finding file size
import fnmatch

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
	
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


class Tts_converter :

	def __init__(self,input_string) :
		self.input_string = input_string
		#remove the program name from the argv list
		self.input_string.pop(0)
		#Extract the file name from the arg list
		self.input_file = input_string.pop(0)
		if fnmatch.fnmatch(self.input_file, '*.pdf'):
			self.text = convert_pdf_to_txt(self.input_file)
			self.file_name='f1.txt'
			file_desc = open(self.file_name,'w')
			file_desc.write(self.text)
			file_desc.close()
			self.input_file = self.file_name
			
	def file_Read(self,file_desc) :
		file_content = file_desc.read(100)
		return file_content
			
	def tts_String(self,file_content) :
		#convert to google friendly url (with + replacing spaces)
		tts_string = '+'.join(file_content.split())
		return tts_string

	def music_Stream_Gen(self,tts_string) :
		#use string in combination with the translate url as the stream to be played
		music_stream_uri = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&q='
        	music_stream_uri += tts_string + "&client=tw-ob"		
		return music_stream_uri

	def play_Speech(self,music_stream_uri) :
		player = gst.element_factory_make("playbin","player")
                player.set_property('uri',music_stream_uri)
                player.set_state(gst.STATE_PLAYING)


#take command line args as the input string
tts_Obj = Tts_converter(sys.argv)

#print 'Input File name is :' + tts_Obj.input_file

file_desc = open(tts_Obj.input_file,'r')

file_content = tts_Obj.file_Read(file_desc)

while file_content != '' :

	if not file_content.endswith(' ') :
		file_list = file_content.rsplit(' ',1)
		if len(file_list) == 2 :
			offset = len(file_list[1])
			file_desc.seek(-offset,1)
		file_content = file_list[0]
	print 'file content is  :' +  file_content

	tts_string = tts_Obj.tts_String(file_content)
	music_stream_uri = tts_Obj.music_Stream_Gen(tts_string)
	tts_Obj.play_Speech(music_stream_uri)
	
	#requires a delay, if the py process closes before the mp3 has finished it will be cut off.
	time.sleep(10)
	file_content = tts_Obj.file_Read(file_desc)
	



