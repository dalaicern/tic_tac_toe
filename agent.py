from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random


def getStateKey(board):
        key = ''
        
        for row in board:
            for item in row:
                key += str(item)

        return key


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
        
        self.rewards = []


    @abstractmethod
    def act(self, s):
        pass
    

    @abstractmethod
    def update(self, s, prev_s, a, prev_a, r):
        pass


class Learner(Agent):

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def act(self, s):
        possible_actions = [a for a in self.actions if s[a[0]*3 + a[1]] == '-']

        if len(possible_actions) == 0:
                return -1 , -1
        

        if random.random() < self.eps or s not in self.Q:

            action = possible_actions[random.randint(0,len(possible_actions)-1)]
        else:

            values = self.Q[s]


            empty_q_values = [values[cell[0], cell[1]] for cell in possible_actions]     
            max_q_value = max(empty_q_values)                                         
            max_q_indices = [i for i in range(len(possible_actions)) if empty_q_values[i] == max_q_value] 
            max_q_index = random.choice(max_q_indices)                             
            action = tuple(possible_actions[max_q_index]) 


        self.eps *= (1.-self.eps_decay)

        return action



    def update(self, state, next_state, action, reward):

        q_values = self.Q.get(state, np.zeros((3, 3)))

        next_q_values = self.Q.get(next_state, np.zeros((3, 3)))
        max_next_q_value = np.max(next_q_values)

        q_values[action[0], action[1]] += self.alpha * (reward + self.gamma * max_next_q_value - q_values[action[0], action[1]])

        self.Q[state] = q_values

    
    def is_game_over(self, board):

        for row in board:
            if len(set(row)) == 1 and row[0] != '-':      
                return True, row[0]


        for col in board.T:                               
            if len(set(col)) == 1 and col[0] != '-':
                return True, col[0]


        
        if len(set(board.diagonal())) == 1 and board[0, 0] != '-':           
            return True, board[0, 0]
        if len(set(np.fliplr(board).diagonal())) == 1 and board[0, 2] != '-': 
            return True, board[0, 2]



        if '-' not in board:
            return True, 'draw'

        return False, None
    def learn(self):
        num_draws = 0  # Counter for the number of draws
        agent_wins = 0  # Counter for the number of wins by the agent
        players = ['X', 'O']
        num_episodes = 10000

        for episode in range(num_episodes):
            board = np.array([['-', '-', '-'],
                            ['-', '-', '-'],
                            ['-', '-', '-']])

            current_player = random.choice(players)  # Randomly choose the current player
            game_over = False

            while not game_over:
                action = self.act(getStateKey(board))  # Choose an action using the exploration rate

                row, col = action
                board[row, col] = current_player  # Update the board with the current player's move

                game_over, winner = self.is_game_over(board)  # Check if the game is over and determine the winner

                if game_over:
                    if winner == current_player:  # Agent wins
                        reward = 1
                        agent_wins += 1
                    elif winner == 'draw':  # Game ends in a draw
                        reward = 0
                        num_draws += 1
                    else:  # Agent loses
                        reward = -1
                    self.update(getStateKey(board), getStateKey(board), action,  reward)  # Update the Q-table
                else:
                    current_player = players[(players.index(current_player) + 1) % 2]  # Switch to the next player

                if not game_over:
                    state = getStateKey(board)
                    board[row, col] = current_player
                    next_state = getStateKey(board)
                    self.update(state, next_state, action, 0)  # Update the Q-table with the next state


        # Play multiple games between the trained agent and itself
        agent_win_percentage = (agent_wins / num_episodes) * 100
        draw_percentage = (num_draws / num_episodes) * 100

        print("Agent win percentage: {:.2f}%".format(agent_win_percentage))
        print("Draw percentage: {:.2f}%".format(draw_percentage))