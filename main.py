from synth import *
from out import *
from instruments import * 
import math

def overtones(freq):
	s1 = SinWave(freq) * Value(6)
	s2 = SinWave(freq * 2) * Value(2)
	s3 = SinWave(freq * 4)
	return Envelope(normalize(s1 + s2 + s3), 0.1)

def alien(freq):
	return Envelope(
		FMSynth(
				SinWave(freq), 
				SinWave(10) * Value(0.04)
			)
		, 0.1)

def record(freq):
	return Envelope(
		FMSynth(
				SinWave(freq), 
				SinWave(freq * 4) * Value(0.01) + SinWave(freq * 2) * Value(0.02)
			)
		, 0.1)

def repeatOf(note, times):
	signal = note
	for x in range(1, times):
		signal = signal << note
	return signal

dS = Finite(Finite(overtones(311.13), 0.25), 0.5)
fS = Finite(Finite(overtones(369.99), 0.25), 0.5)
gS = Finite(Finite(overtones(415.30), 0.25), 0.5)
aS = Finite(Finite(overtones(466.16), 0.25), 0.5)
cS = Finite(Finite(overtones(554.37), 0.25), 0.5)

dSa = Finite(Finite(alien(311.13), 0.25), 0.5)
fSa = Finite(Finite(alien(369.99), 0.25), 0.5)
gSa = Finite(Finite(alien(415.30), 0.25), 0.5)
aSa = Finite(Finite(alien(466.16), 0.25), 0.5)
cSa = Finite(Finite(alien(554.37), 0.25), 0.5)

dSr = Finite(Finite(record(311.13), 0.25), 0.5)
fSr = Finite(Finite(record(369.99), 0.25), 0.5)
gSr = Finite(Finite(record(415.30), 0.25), 0.5)
aSr = Finite(Finite(record(466.16), 0.25), 0.5)
cSr = Finite(Finite(record(554.37), 0.25), 0.5)

dSrf = Finite(Finite(record(311.13), 0.25), 0.3)
fSrf = Finite(Finite(record(369.99), 0.25), 0.3)
gSrf = Finite(Finite(record(415.30), 0.25), 0.3)
aSrf = Finite(Finite(record(466.16), 0.25), 0.3)
cSrf = Finite(Finite(record(554.37), 0.25), 0.3)

dG = Guitar(311.13)
fG = Guitar(369.99)
gG = Guitar(415.30)
aG = Guitar(466.16)
cG = Guitar(554.37)

# aS is the frequency i keep returning to
# building up tempo
# sequence1 = (dG << dG << dG << dG) << (gG << gG << gG) << (fG << fG) << (aG << dG << fG << gG)
sequence1 = (dS << dS << dS << gS << gS << gS << fS << fS << aS << dS << fS << gS)
# repeating a pattern
sequence2 = aSa << ((cS << cS << aS << cS) << (cS << aS << fS << fSa)) << (aS << dS << dS << aS) << ((gS << gS << aS << dSa) << (fS << gSa << aS))
# and into madness we go
sequence3 = (cSr << cSa << aS << dSr) << (dSr << aS << cSr << cSr) << (dSr << dSr << aS)
# continuation there of!!!
sequence4 = dSa << repeatOf(dSrf, 4) << dSa << repeatOf(gSrf, 4) << dSa << repeatOf(cSrf, 4)
# a conclusion...
sequence5 = ((dSa << aSr << dSa << dS) << (aSa * Value(0.2) + aS * Value(0.8))) << (dS << dS << cS << cS) << ((aS << dS << dS << gS) << (gS << aS << aS << aS * Value(0.2)))

sequence = sequence1 << repeatOf((sequence2 << repeatOf((sequence3 << sequence4), 2)), 2) << sequence5





# sequence = sequence << (cS << cS << aS << aS << gS << aS << gS << aS)
#sound = normalize(offsetPlayback(sound, 1))
# print ("duration: " + str(sequence.getDuration()))
# play (normalize(sequence))

