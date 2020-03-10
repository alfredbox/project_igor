'''
A simple program to read in the state of a motor encoder
pin and compute and print the speed in RPM.
'''
from gpiozero import DigitalInputDevice
#from signal import pause

def on_change():
   print('Change detected')

def setup():
    encoder_a = DigitalInputDevice(12)
    while True:
        encoder_a.wait_for_active()
        print('ON!')
        encoder_a.wait_for_inactive()
        print('OFF!')
    #encoder_a.when_activated = on_change
    #encoder_a.when_deactivated = on_change

if __name__ == "__main__":
    print('Testing motor speed')
    setup()
    #pause()
