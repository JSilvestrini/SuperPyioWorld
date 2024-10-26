# TODO: When player dies or succeeds, reset Environment, put player in level

import dxcam
import time
import numpy as np
from PIL import Image
import memory_access
from helper import press_combos, find_activate_window, hold_key, get_region
import torch

action_space = {
    # arrow key movement
    # c = jump(b), v = spin(a), x = run(y)
    0: ['left'],
    1: ['down'],
    2: ['right'],
    3: ['right', 'c'],
    4: ['left', 'c'],
    5: ['right', 'v'],
    6: ['left', 'v'],
    7: ['c'],
    8: ['v'],
    9: ['d'],
    10: ['right', 'x'],
    11: ['left', 'x'],
    12: ['right', 'x', 'c'],
    13: ['left', 'x', 'c'],
    14: ['right', 'x', 'v'],
    15: ['left', 'x', 'v'],
}

class Environment:
    def __init__(self, device='cpu'):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.camera = dxcam.create()
        self.choose = False
        self.region = get_region()
        self.reset()

    def reset(self):
        self.x_velocity = 0
        self.x_velocity_prev = 0
        self.x_velocity_max = 1
        self.y_velocity = 0
        self.y_velocity_prev = 0
        self.x_coord = 0
        self.x_coord_max = 0
        self.power_up = 0
        self.power_up_prev = 0
        self.lives = 0
        self.lives_prev = 0
        self.frame_stack = []
        self.choose = not self.choose
        time.sleep(2.6)
        find_activate_window()
        press_combos(['v'])
        press_combos(['tab'])
        time.sleep(1.2)
        self.start_time = time.time()
        self.screenshot()

    def screenshot(self) -> None:
        try:
            m = np.array(self.camera.grab(region=self.region))
            im = Image.fromarray(m)
            #self.frame_stack.append(np.array(im.reduce(2)))
            self.frame_stack.append(np.array(im))
        except:
            #print("BROKEN")
            return
        if len(self.frame_stack) > 1:
            self.frame_stack.pop(0)

    def action(self, action : np.ndarray) -> None:
        press_combos(action_space[np.where(action == 1)[0][0]])

    def update(self) -> None:
        # Update Previous Values
        self.x_velocity_prev = self.x_velocity
        self.y_velocity_prev = self.y_velocity
        self.power_up_prev = self.power_up
        self.lives_prev = self.lives

        # Current Values
        self.x_velocity = memory_access.read_memory_bytes(0xA3238F, 1, _signed=True)
        self.y_velocity = memory_access.read_memory_bytes(0xA32391, 1, _signed=True)
        self.x_coord = memory_access.read_memory_bytes(0xA323E5, 2)
        self.power_up = memory_access.read_memory_bytes(0xA3232D, 1)
        self.lives = memory_access.read_memory_bytes(0xA330D2, 1)

        self.screenshot()

    def state(self) -> np.ndarray:
        return ((torch.tensor(self.frame_stack[0])).permute(2, 0, 1)).unsqueeze(0).numpy()

    def reward(self) -> float:
        reward = 0.0

        # If the player is maintaining max velocity
        if self.x_velocity >= 37:
            reward += 0.3
        if self.x_velocity >= 47:
            reward += 0.5
        if self.x_coord > self.x_coord_max:
            self.x_coord_max = self.x_coord
            reward += 1
        if self.x_velocity <= 0:
            reward -= 0.2
        if self.x_velocity == self.x_velocity_prev and self.x_velocity < 37:
            reward -= 0.3

        # If the player is gaining or losing velocity
        if self.x_velocity > self.x_velocity_prev:
            reward += 0.2
        else:
            reward -= 0.2

        return reward

    def step(self, action):
        self.action(action)
        self.update()
        reward = self.reward()

        done = False
        flags = memory_access.read_memory_bytes(0xA330E9, 1)
        other = memory_access.read_memory_bytes(0xA32385, 1)

        if flags in [0x1, 0x2, 0x3, 0x4]:
            hold_key(['tab'], 1.0)
            reward += 2
            done = True
        elif flags in [0x80] or other in [0x09]:
            hold_key(['tab'], 1.0)
            reward -= 4
            done = True

        if (time.time() - self.start_time >= 15) and done == False:
            memory_access.write_byte(0xA33245, b'\x00\x00\x03')
            hold_key(['tab'], 1.0)
            reward -= 2
            done = True
            

        print(f"REWARD: {reward}")

        return self.state(), reward, done

if __name__ == "__main__":
    en = Environment()