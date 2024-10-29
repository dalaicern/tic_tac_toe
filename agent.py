from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random

class Agent(ABC):
    def __init__ (self, alpha , gamma, eps, eps_decay):

        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay

        self.actions = []

        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
       
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)

        self.rewards = []


    def act(self, s):
        possible_actions = [a for a in self.actions if s[a[0]*3 + a[1]] == '-']

        if len(possible_actions) == 0:
                return -1 , -1
        

        if random.random() < self.eps:

            action = possible_actions[random.randint(0,len(possible_actions)-1)]
        else:

            values = np.array([self.Q[a][s] for a in possible_actions])

            

            ix_max = np.where(values == np.max(values))[0]
            if len(ix_max) > 1:

                ix_select = np.random.choice(ix_max, 1)[0]
            else:

                ix_select = ix_max[0]
            action = possible_actions[ix_select]


        self.eps *= (1.-self.eps_decay)

        return action
    

    @abstractmethod
    def update(self, s, prev_s, a, prev_a, r):
        pass


class Learner(Agent):

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, prev_s, a, prev_a, r):
        """
        Perform the Q-Learning update of Q values.

        Parameters
        ----------
        s : string
            previous state
        prev_s : string
            new state
        a : (i,j) tuple
            previous action
        prev_a : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """

        if prev_s is not None:

            possible_actions = [action for action in self.actions if prev_s[action[0]*3 + action[1]] == '-']
            Q_options = [self.Q[action][prev_s] for action in possible_actions]

            self.Q[a][s] += self.alpha*(r + self.gamma*max(Q_options) - self.Q[a][s])
        else:

            self.Q[a][s] += self.alpha*(r - self.Q[a][s])


        self.rewards.append(r)



    