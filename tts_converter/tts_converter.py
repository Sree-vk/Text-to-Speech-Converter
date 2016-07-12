#!/usr/bin/python

import sys  #for cmd line argv
import time #for delay
import pygst    #for playing mp3 stream
import gst      #" "
import os   #for finding file size

#take command line args as the input string
input_string = sys.argv

#remove the program name from the argv list
input_string.pop(0)

input_file = input_string.pop()
print 'Input File name is :' + input_file

file_desc = open(input_file,'r')

'''file_size = os.path.getsize(input_file)
print 'file size is : ' + str(file_size)

loop_count = file_size / 100
rem_bytes = file_size % 100
int(rem_bytes)
print 'rem_bytes is : ' + str(rem_bytes)
i=0
'''

#for i in range(loop_count + 1) :
#	file_content = file_desc.read()
while True :
	file_content = file_desc.read(100)
#	if i == loop_count :
#		if rem_bytes != 0 :
#			file_content = file_desc.read(6)
	if file_content == '' :
		break

	if not file_content.endswith(' ') :
		file_list = file_content.rsplit(' ',1)
		if len(file_list) == 2 :
			offset = len(file_list[1])
			file_desc.seek(-offset,1)
		file_content = file_list[0]
#		file_desc.seek(-offset,1)
	print 'file content is  :' +  file_content

#convert to google friendly url (with + replacing spaces)
	tts_string = '+'.join(file_content.split())

	print tts_string

#use string in combination with the translate url as the stream to be played
	music_stream_uri = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&q='
	music_stream_uri += tts_string + "&client=tw-ob"
	print  music_stream_uri
	player = gst.element_factory_make("playbin","player")
	player.set_property('uri',music_stream_uri)
	player.set_state(gst.STATE_PLAYING)
	
#print  sys.exc_info()[0]
#requires a delay, if the py process closes before the mp3 has finished it will be cut off.
time.sleep(70)
	
#	raw_input('Press Enter to Exit')


