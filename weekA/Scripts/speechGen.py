#!/usr/bin/env python3
import rospy
from vosk import Model, KaldiRecognizer
import pyaudio
import simpleaudio as sa
import numpy as np

def playback(recognizer, stream, playback_obj):
	soundhandle.say("Speak now")

	audioData = stream.read(1024)
	#checks if nothing is said
	if len(audioData) == 0:
		return
		recognizer.AcceptWaveform(audioData)
		result = recognizer.Result()
		text = result["text"].strip()

		if text:
			print("You said: ", text)
			playback_obj.play(audioData)



def listenerRun():
	rospy.init_node('speech_listener')

	modelPath = "/hri2023/src/ros-vosk/models/vosk-model-small-en-us-0.15/am/final.mdl"
	sampleRate = 16000
	model = Model(modelPath)
	recognizer = KaldiRecognizer(model, sampleRate)

	audio = pyaudio.Pyaudio()
	stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sampleRate, input=True, frames_per_buffer=1024)

	playback_obj = sa.playback.PlaybackObject(sampleRate = sampleRate, channels = 1, dtype = np.int16)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		playback()
		rate.sleep()
	cleanup(stream, audio)

def cleanup(stream, audio):
	stream.stop_stream()
	stream.close()
	audio.terminate()

if __name__ == '__main__':
	try:
		#Testing our function
		listenerRun()
	except rospy.ROSInterruptException: pass
		