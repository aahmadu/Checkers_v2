from checkers.rl_env import *
from ai.replay_buffer import *
import numpy as np
# import torch

if __name__ == "__main__":

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('Using {} device'.format(device))

    env = RLEnv()

    """ Training Variables """
