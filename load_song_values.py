"""Runs pyalsa on a given song and pickles the values"""
import alsaaudio
import audioop

inp = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,0)
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)
       
while True:
        l,data = inp.read()
        if l:
                print audioop.rms(data,2)