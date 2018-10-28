#!/usr/bin/env python3.6
import speech_recognition as sr
import pyaudio, sys
from ctypes import *
from contextlib import contextmanager
from subprocess import call

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def speech_recog():
  r = sr.Recognizer()
  with noalsaerr() as n, sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)  # here
    #print("Say something!")
    audio = r.listen(source)
  try:
      #print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
      return r.recognize_google(audio).lower().replace(" ", "")
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
      return None
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
      return None
  # recognize speech using Sphinx
  #try:
  #  print("Sphinx thinks you said " + r.recognize_sphinx(audio))
  #except sr.UnknownValueError:
  #  print("Sphinx could not understand audio")
  #except sr.RequestError as e:
  #  print("Sphinx error; {0}".format(e))

print("Please say the command. Don't be too close to the microphone nor too far for a better quality.")
command=speech_recog()
while command != "exit" or command != "quit" or command != "terminate":

  if command:
    command=command.replace("space", " ").replace("dash", "-")
    print("The command is: "+command)
    print("Please confirm whether this is what you meant, by saying yes/enter or no.")
    resp=speech_recog()

    while resp != "yes" and resp !="no" and resp!="enter" and resp=="abort" or resp is None:
      print("Please repeat")
      resp=speech_recog()

    if resp == "yes" or resp == "enter":
      print("Executing...")
      if command == "date":
        call(["date"])
      if command == "show machine messages":
        call(["dmesg", "-T"])
      if "weather" in command:
        command=command.replace("weather ", "") 
        call("/usr/bin/curl http://wttr.in/"+command, shell=True)
      elif command == "exit" or command == "quit" or command == "terminate":
        print("Terminating...")
        sys.exit(0)
      else:
        call(command.lower(), shell=True)
  else:
    print("Whoops, couldn't understand")
  
  print("Please say the command")
  command=speech_recog()

