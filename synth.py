from math import *
from constants import SAMPLE_RATE

pi = 3.141592653

class SoundSource:
	def __init__():
 		pass 
 	def sample():
 		return 0

 	def maxAmp():
 		return 0

 	def __add__(self, other):
 		if isinstance(other, Finite) and isinstance(self, Finite):
 			return Finite(WaveAdd(self, other), max(self.getDuration(), other.getDuration()))
 		return WaveAdd(self, other)

 	def __mul__(self, other):
 		if isinstance(other, Finite) and isinstance(self, Finite):
 			return Finite(WaveMult(self._wave, other._wave), min(self.getDuration(), other.getDuration()))
 		elif isinstance(self, Finite):
 			return Finite(WaveMult(self._wave, other), self.getDuration())
 		return WaveMult(self, other)

class TimeMod(SoundSource):
	def __init__(self, wave, func):
		assert(isinstance(wave, SoundSource))

		self._wave = wave
		self._func = func

	def sample(self, time, duration):
		return self._wave.sample(self._func(time), self._func(duration))

	def maxAmp(self):
		return self._wave.maxAmp()

	def __str__(self):
		return "TimeMod(" + str(self._wave) + ")"

class FMSynth(SoundSource):
	def __init__(self, wave, mod):
		self._wave = wave
		self._mod = mod

	def sample(self, time, duration):
		return self._wave.sample(time + self._mod.sample(time, duration), duration)

	def maxAmp(self):
		return self._wave.maxAmp()
		
	def __str__(self):
		return "FM(" + str(self._wave) + ", " + str(self._mod) + ")"

class SinWave(SoundSource):
	def __init__(self, freq):
		self._freq = freq
		
	def sample(self, time, duration):
		return cos(2 * pi * time * self._freq)

	def maxAmp(self):
		return 1

	def __str__(self):
		return "SinWave(" + str(self._freq) + ")"

class Value(SoundSource):
	def __init__(self, value):
		assert(value != None)
		self._value = value
		
	def sample(self, time, duration):
		return self._value

	def maxAmp(self):
		return self._value

	def __str__(self):
		return "[" + str(self._value) + "]"

class WaveMult(SoundSource):
	def __init__(self, wave1, wave2):
		self._wave1 = wave1
		self._wave2 = wave2
		self._maxAmp = wave1.maxAmp() * wave2.maxAmp()
		
	def sample(self, time, duration):
		return self._wave1.sample(time, duration) * self._wave2.sample(time, duration)

	def maxAmp(self):
		assert(self._maxAmp != None)
		return self._maxAmp

	def __str__(self):
		return "(" + str(self._wave1) + " * " + str(self._wave2) + ")"

class WaveAdd(SoundSource):
	def __init__(self, wave1, wave2):
		self._wave1 = wave1
		self._wave2 = wave2
		self._maxAmp = wave1.maxAmp() + wave2.maxAmp()
		
	def sample(self, time, duration):
		return self._wave1.sample(time, duration) + self._wave2.sample(time, duration)

	def maxAmp(self):
		assert(self._maxAmp != None)
		return self._maxAmp

	def __str__(self):
		return "(" + str(self._wave1) + " + " + str(self._wave2) + ")"

class PhaseShift(SoundSource):
	def __init__(self, wave, offset):
		self._wave = wave
		self._offset = offset
		self._maxAmp = wave.maxAmp()
		
	def maxAmp(self):
		assert(self._maxAmp != None)
		return self._maxAmp

	def sample(self, time, duration):
		if time < self._offset:
			return 0
		return self._wave.sample(time - self._offset, duration - self._offset)

	def __str__(self):
		return "PhaseShift(" + str(self._wave) + ", " + str(self._offset) +")"

def phaseShift(wave, offset):
	if isinstance(wave, Finite):
		return Finite(PhaseShift(wave, offset), offset + wave.getDuration())
	return PhaseShift(wave, offset)


class Finite(SoundSource):
	def __init__(self, wave, duration):
		self._wave = wave
		self._duration = duration
		self._maxAmp = wave.maxAmp()

	def sample(self, time, duration):
		if time >= self._duration:
			return 0
		return self._wave.sample(time, self._duration)

	def maxAmp(self):
		return self._maxAmp

	def getDuration(self):
		return self._duration

	def __str__(self):
		return str(self._wave) + ":" + str(self._duration)

	def __lshift__(self, other):
		sum = self + phaseShift(other, self.getDuration())
		return Finite(sum, self.getDuration() + other.getDuration())

class Sequence:
	def __init__():
		self._waves = []
		self._maxAmp = 0
	def maxAmp():
		return 

	def __lshift__(self):
		return self._waves

class Envelope(SoundSource):
	def __init__(self, wave, time):
		self._wave = wave
		self._time = float(time)
		self._maxAmp = wave.maxAmp()
		
	def sample(self, time, duration):
		if time < self._time:
			return time / self._time * self._wave.sample(time, duration)
		elif time > duration - self._time:
			return (duration - time) / self._time * self._wave.sample(time, duration)
		return self._wave.sample(time, duration)

	def maxAmp(self):
		return self._maxAmp

	def getDuration(self):
		return self._durations

	def __str__(self):
		return "Envelope(" + str(self._wave) + ", " + str(self._time) + ")"


def normalize(wave):
	return wave * Value(1.0 / wave.maxAmp())