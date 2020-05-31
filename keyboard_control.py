import pygame
import time

class Dkey:
    def __init__(self, key_id):
        self.key_id = key_id
        self.latched = time.time()
        self.pressed = False;
        self.latch_period_s  = 0.5

    def update(self, key_states):
        if (time.time() - self.latched) > self.latch_period_s:
            import pdb
            pdb.set_trace()
            new_state = key_states[self.key_id] != 0
            if new_state != self.pressed:
                self.latched = time.time()
                self.pressed = new_state

    def is_pressed(self):
        return self.pressed


pygame.init()

while True:
    events = pygame.event.get()
    for e in events:
        print(e)
        if e.type == pygame.KEYDOWN:
            print(e.key)
    time.sleep(0.5)
    pygame.event.pump()




