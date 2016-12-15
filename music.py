#!/usr/bin/python

import time
import threading
import vlc
import random
from os import listdir
from os.path import isfile, join
option1path = r"C:\Users\Evan\Desktop\votebot\music\option1"
option2path = r"C:\Users\Evan\Desktop\votebot\music\option2"

option1files = [f for f in listdir(option1path) if isfile(join(option1path, f))]
option2files = [f for f in listdir(option1path) if isfile(join(option2path, f))]


	
while(1):
	file = random.choice(option1files)
	p = vlc.MediaPlayer(join(option1path, file))
	
	p.play()
	while(p.get_state() != vlc.State.Ended):
		time.sleep(1)
		print p.get_state()

