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

def getStateKey(board):
        key = ''
        
        for row in board:
            for item in row:
                key += str(item)

        return key

class Game:
    def __init__(self, teacher=None):

        print("inti")
        self.board = [['-','-','-'], ['-','-','-'], ['-','-','-']]
        self.agent = Learner(alpha=0.5, gamma=0.9, eps=0.1)
        self.teacher = teacher
        self.game_finished = False


    def render_board(self, ximg, oimg):
        global graphical_board
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'X':
                    # Create an X image and rect
                    graphical_board[i][j][0] = ximg
                    graphical_board[i][j][1] = ximg.get_rect(center=(j*300+150, i*300+150))
                elif self.board[i][j] == 'O':
                    graphical_board[i][j][0] = oimg
                    graphical_board[i][j][1] = oimg.get_rect(center=(j*300+150, i*300+150))

    def add_XO(self, row, column, xo):
        global graphical_board
        # if to_move == 'O':

        #     prev_board = getStateKey(self.board)
        #     print(prev_board)
            
        #     y, x = self.agent.act(prev_board)
        #     print(y ,x)
        #     self.board[y][x]
        #     to_move = 'X'

        # else :
        
        #     if self.board[round(converted_y)][round(converted_x)] != 'O' and self.board[round(converted_y)][round(converted_x)] != 'X':
        #         self.board[round(converted_y)][round(converted_x)] = to_move
            
        #     to_move = 'O'

        self.board[row][column] = xo


        self.render_board(X_IMG, O_IMG)

        for i in range(3):
            for j in range(3):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])


    def check_win(self):
        winner = None
        for row in range(0, 3):
            if((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board [row][0]  != '-')):
                winner = self.board[row][0]
                for i in range(0, 3):
                    graphical_board[row][i][0] = pygame.image.load(f"assets/Winning {winner}.png")
                    SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
                pygame.display.update()
                return winner

        for col in range(0, 3):
            if((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] != '-')):
                winner =  self.board[0][col]
                for i in range(0, 3):
                    graphical_board[i][col][0] = pygame.image.load(f"assets/Winning {winner}.png")
                    SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
                pygame.display.update()
                return winner
    
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] != '-'):
            winner =  self.board[0][0]
            graphical_board[0][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[0][0][0], graphical_board[0][0][1])
            graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
            graphical_board[2][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
            SCREEN.blit(graphical_board[2][2][0], graphical_board[2][2][1])
            pygame.display.update()
            return winner
            
        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] != '-'):
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
                    if self.board[i][j] != 'X' and self.board[i][j] != 'O':
                        return None
            return "DRAW"
        

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_pos = pygame.mouse.get_pos()
                    print(current_pos[0], current_pos[1])
                    x = round((current_pos[0]-65)/835*2)
                    y = round(current_pos[1]/835*2)

                    if self.board[y][x] == '-':
                        self.add_XO( y, x, 'X')

                        state = getStateKey(self.board)
                        y, x = self.agent.act(state)

                        if y == -1:
                            self.check_win()
                        else:
                            self.add_XO( y, x, 'O')


                if self.game_finished:
                    global graphical_board
                    self.board = [['-','-','-'], ['-','-','-'], ['-','-','-']]
                    graphical_board = [[[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]]]

                    self.to_move = 'X'

                    SCREEN.fill(BG_COLOR)
                    SCREEN.blit(BOARD, (64, 64))

                    self.game_finished = False

                    pygame.display.update()
                
                if self.check_win() is not None:
                    self.game_finished = True
                
                pygame.display.update()

game = Game()
game.play()

