#!/usr/bin/python

import sys  #for cmd line argv
import time #for delay
import pygst    #for playing mp3 stream
import gst      #" "
#import os   #for finding file size


class Tts_converter :

	def __init__(self,input_string) :
		self.input_string = input_string
		#remove the program name from the argv list
		self.input_string.pop(0)
		#Extract the file name from the arg list
		self.input_file = input_string.pop(0)

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
#input_string = sys.argv

#remove the program name from the argv list
#input_string.pop(0)
#print 'File name removed : ' + str(tts_Obj.input_string)

#input_file = input_string.pop()
print 'Input File name is :' + tts_Obj.input_file

file_desc = open(tts_Obj.input_file,'r')
#print 'File Descriptor is : ' + str(file_desc)

file_content = tts_Obj.file_Read(file_desc)
#if file_content == '' :
#	break

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
#convert to google friendly url (with + replacing spaces)
#tts_string = '+'.join(file_content.split())
#		print tts_string

		#use string in combination with the translate url as the stream to be played
#		music_stream_uri = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&q='
#		music_stream_uri += tts_string + "&client=tw-ob"
#		print  music_stream_uri

#		player = gst.element_factory_make("playbin","player")
#		player.set_property('uri',music_stream_uri)
#		player.set_state(gst.STATE_PLAYING)
	

		#requires a delay, if the py process closes before the mp3 has finished it will be cut off.
	time.sleep(7)
	file_content = tts_Obj.file_Read(file_desc)
	



