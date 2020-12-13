from pygame import *

class Music():
   def play_music():
    mixer.init()
    mixer.music.load('CLUE-LessTest1.ogg')
    mixer.music.play()
    while mixer.music.get_busy():
      time.Clock().tick(10)
