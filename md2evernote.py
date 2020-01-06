# Script         : Markdown to Evernote Uploader
#                  Recursively reads a directory containing markdown files, and uploads them to Evernote
#                  Designed to work with the output of wp2md (see https://github.com/jonbeckett/wp2md)
#                  Also requires the Windows Evernote client installed
# Author         : Jonathan Beckett (jonathan.beckett@gmail.com)
# Compatibility  : Python 3.x
# Pre-Requisites : Windows Evernote Client

# path where markdown files reside
root_path = "c:\\temp\\blog"


# Import modules
import os
import os.path
import json
import time
import subprocess


for subdir, dirs, files in os.walk(root_path):
	for file in files:
		if '.txt' in file and 'README.md' not in file:

			print("Processing " + file)
			
			# Read the file contents
			markdown_file_full_path = os.path.join(subdir, file)
			markdown_file = open(markdown_file_full_path,'r',encoding="latin-1")
			markdown_text = markdown_file.read()
			
			# split the line into files, and chop the top 4 off
			# (to get rid of the title and date, as output by wp2md)
			markdown_text_lines = markdown_text.splitlines()
			hybrid_text_lines = []
			hybrid_text_lines += markdown_text_lines[4:]
			
			# build the post title and body
			post_title = markdown_text_lines[0].replace('# ','')
			post_body = '\n'.join(hybrid_text_lines)
			
			post_body = post_body.replace( u'\U0001f499', '')
			post_body = post_body.replace( u'\U0001f49a', '')
			post_body = post_body.replace( u'\U0001f49b', '')
			post_body = post_body.replace( u'\U0001f49c', '')
			post_body = post_body.replace( u'\U0001f633', '')
			post_body = post_body.replace( u'\u2018', u'\'')
			post_body = post_body.replace( u'\u2019', u'\'')
			post_body = post_body.replace( u'\u201c', u'\'')
			post_body = post_body.replace( u'\u201d', u'\'')
			post_body = post_body.replace( u'\u2013', '-')
			post_body = post_body.replace( u'\u2026', '...')
			post_body = post_body.replace( u'\u2033', '\'')
			post_body = post_body.replace( u'\u2032', '\'')
			post_body = post_body.replace( u'\xd7', 'x')
			post_body = post_body.replace( u'\xc2', ' ')
			
			# Extract the date from the filename
			year = file[0:4]
			month = file[5:7]
			day = file[8:10]
			post_date = year + '-' + month + '-' + day
			
			# close the open markdown file
			markdown_file.close()
			
			# create a temporary file
			post_file = open("C:\\Program Files (x86)\\Evernote\\Evernote\\post.txt", "w",encoding="latin-1")
			post_file.write(post_body)
			post_file.close()
			
			# run the evernote command line tool with parameters
			
			os.chdir("C:\\Program Files (x86)\\Evernote\\Evernote\\")
			
			cmd = "enscript.exe createNote /s \"post.txt\" /n \"Blog\" /i \"" + post_title.replace("\"","") + "\" /c \"" + post_date + "\" /t \"Blog\" /t \"" + year + "-" + month + "\""
			
			os.system(cmd)
			
			# rename the file
			os.rename(markdown_file_full_path,markdown_file_full_path.replace(".txt",".bak"))
			
			# wait 1 second (to avoid stressing the API too much)
			# time.sleep(1)
			
