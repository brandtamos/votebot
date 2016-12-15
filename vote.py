
#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir
import serial
import time
import threading
import vlc
import random
from os import listdir
from os.path import isfile, join

PORT_NUMBER = 8080

option1_count = 0
option2_count = 0
total_count = 0
current_option = 1
usbSerial = serial.Serial("COM5", 9600)

option1path = r"C:\Users\Evan\Desktop\votebot\music\option1"
option2path = r"C:\Users\Evan\Desktop\votebot\music\option2"

option1files = [f for f in listdir(option1path) if isfile(join(option1path, f))]
option2files = [f for f in listdir(option2path) if isfile(join(option2path, f))]

def send_signal():
	while(1):
		if(total_count == 0):
			value = "0.5"
		else:
			value = str(option1_count / float(total_count))
		print value
		usbSerial.write(value)
		usbSerial.flush()
		time.sleep(2)

def play_music():
	global current_option, option1_count, total_count
	last_option = current_option
	while(1):
		if(current_option == 1):
			file = random.choice(option1files)
			p = vlc.MediaPlayer(join(option1path, file))
		else:
			file = random.choice(option2files)
			p = vlc.MediaPlayer(join(option2path, file))
		
		
		p.play()
		while((p.get_state() != vlc.State.Stopped) and (p.get_state() != vlc.State.Ended)):
			if option1_count > total_count - option1_count:
				current_option = 1
			else:
				current_option = 2
			
			if(current_option == last_option):
				time.sleep(1)
			else:
				print 'Stopping'
				p.stop();
			last_option = current_option
			
def increment_option1():
	global option1_count, total_count
	option1_count += 1
	total_count += 1
	
def increment_option2():
	global total_count
	total_count += 1
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		print self.path
		if(self.path == '/vote'):
			f = open('vote.html', 'rb')
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.send_header('Access-Control-Allow-Origin','*') 
			self.end_headers()
			# Send the html message
			self.wfile.write(f.read())
		elif(self.path == '/option1'):
			increment_option1()
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("option 1 count: " + str(option1_count))
		elif(self.path == '/option2'):
			increment_option2()
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("Vote received.")
		elif(self.path =='/gettally'):
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write('{"option1": ' + str(option1_count) + ', "option2": ' + str((total_count - option1_count)) + '}')
		else:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("Wrong URL, dingus!")
		return
	
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	t1 = threading.Thread(target=send_signal, args=[])
	t2 = threading.Thread(target=play_music, args=[])
	
	t1.start()
	t2.start()
	
	
	#Wait forever for incoming http requests
	server.serve_forever()
	

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
