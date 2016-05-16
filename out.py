from math import *
from constants import SAMPLE_RATE
import synth
import struct
import pyaudio

def play(source):
	if not isinstance(source, synth.Finite):
		raise ValueError("expected instance of synth.Finite got " + str(source))

	print ("playing... " + str(source))

	p = pyaudio.PyAudio()  
	#open stream
	stream = p.open(format = p.get_format_from_width(2),  
	                channels = 1,  
	                rate = int(SAMPLE_RATE),
	                output = True)  
	
	#paly stream
	duration = source.getDuration()
	exponent = float((2 ** 15) - 1)
	for index in range(0, int(source.getDuration() * SAMPLE_RATE)):
		sample = (source.sample(index / SAMPLE_RATE, source.getDuration())) * exponent
		if sample >= exponent:
			sample = exponent
		elif sample <= -exponent:
			sample = -exponent

		packed_value = struct.pack('h', int(sample))
		stream.write(packed_value)
		index = index + 1

	#stop stream  
	stream.stop_stream()  
	stream.close()

	#close PyAudio  
	p.terminate()  
