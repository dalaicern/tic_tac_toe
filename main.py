import pygame, sys
from agent import *

 
pygame.init()
 
WIDTH, HEIGHT = 900, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

BG_COLOR = (214, 201, 227)

graphical_board = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]]


SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (64, 64))

pygame.display.update()


class Game:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.game_finished = False
        self.player = 1
        self.p1 = p1
        self.p2 = p2

    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def render_board(self, ximg, oimg):
        global graphical_board
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    graphical_board[i][j][0] = ximg
                    graphical_board[i][j][1] = ximg.get_rect(center=(j*300+150, i*300+150))
                elif self.board[i][j] == -1:
                    graphical_board[i][j][0] = oimg
                    graphical_board[i][j][1] = oimg.get_rect(center=(j*300+150, i*300+150))


    def add_XO(self, action, xo):
        global graphical_board

        self.board[action[0]][action[1]] = xo


        self.render_board(X_IMG, O_IMG)

        for i in range(3):
            for j in range(3):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])


    def check_win(self):
        winner = None
        for row in range(0, 3):
            if abs(sum(self.board[row, :])) == 3:
                winner = self.board[row][0]
                for i in range(0, 3):
                    graphical_board[row][i][0] = pygame.image.load(f"assets/Winning {winner}.png")
                    SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
                pygame.display.update()
                return winner

        for col in range(0, 3):
            if abs(sum(self.board[:, col])) == 3:
                winner =  self.board[0][col]
                for i in range(0, 3):
                    graphical_board[i][col][0] = pygame.image.load(f"assets/Winning {winner}.png")
                    SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
                pygame.display.update()
                return winner
    
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] != 0):
            winner =  self.board[0][0]
            graphical_board[0][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[0][0][0], graphical_board[0][0][1])
            graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
            graphical_board[2][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[2][2][0], graphical_board[2][2][1])
            pygame.display.update()
            return winner
            
        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] != 0):
            winner =  self.board[0][2]
            graphical_board[0][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[0][2][0], graphical_board[0][2][1])
            graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
            graphical_board[2][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[2][0][0], graphical_board[2][0][1])
            pygame.display.update()
            return winner
        
        if winner is None:
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] != 1 and self.board[i][j] != -1:
                        return None
            return "DRAW"
        
    def play(self):
        while True:
            if self.player == 1:
                action = self.p1.act(self.availablePositions() , self.board, self.player)
            else:
                action = self.p2.act(self.availablePositions() ,  self.board, self.player)
            
            self.add_XO(action, self.player)
            self.player = 1 if self.player == -1 else -1
            winner = self.check_win()
            pygame.display.update()
            if winner is not None:
                pygame.time.wait(1000)
                global graphical_board
                graphical_board = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]]
                self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
                self.player = 1
                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (64, 64))
                pygame.display.update()



p1 = Learner("p1")
p2 = Learner("p2")

# st = State(p1, p2)
# print("training...")
# st.play(50001)    

p1.loadPolicy("policy_p1")
p2.loadPolicy("policy_p2")
game = Game(Human, p2)
game.play()
    
