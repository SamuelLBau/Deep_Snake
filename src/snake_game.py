import random as rand
from copy import copy

#These are only used in visualization (See render_snake)
import numpy as np
import matplotlib.pyplot as plt

#This is just for debugging
import time
import cProfile
from math import sqrt

class snake_game():
    DEFAULT_BOARD_SIZE = [80,80]
    VALID_DIRS = [[0,0],[0,-1],[0,1],[-1,0],[1,0]]
    ACTION_dict = {}

    def __init__(self,board_size=DEFAULT_BOARD_SIZE,render=False,save=False):
        self.board_size = board_size
        self.snake = self.get_rand_pos(board_size) #index0 is the head, index-1 is the tail

        #self.ACTION_dict[0] = self.ACTION_dict["stay"] = self.VALID_DIRS[0]
        self.ACTION_dict[0] = self.ACTION_dict["up"] = self.VALID_DIRS[3]
        self.ACTION_dict[1] = self.ACTION_dict["down"] = self.VALID_DIRS[4]
        self.ACTION_dict[2] = self.ACTION_dict["left"] = self.VALID_DIRS[1]
        self.ACTION_dict[3] = self.ACTION_dict["right"] = self.VALID_DIRS[2]

        self.render=render
        self.save=save

        self.fig = plt.figure()

#----------------------------------BEGIN 'PUBLIC' FUNCTIONS------------------------------
    def get_rand_pos(self,board_size):
        return [rand.randrange(0,board_size[0]),
                    rand.randrange(0,board_size[1])]
    def reset(self,render=False,save=False):
        self.food_pos   = self.get_rand_pos(self.board_size)
        init_pos        =  self.get_rand_pos(self.board_size)
        self.snake      = [init_pos]

        self.render=render
        self.save=save

    def get_image(self):
        board = np.zeros(self.board_size)
        board[self.food_pos[0],self.food_pos[1]] = 128
        for pos in self.snake:
            board[pos[0],pos[1]] = 255
        return board

    def get_image_dims(self):
        return self.board_size

    def get_num_controls(self):
        return len( self.VALID_DIRS)

    def step(self,direction):
        '''
            direction: Input format to be determined, but will be the up/down/left/right directions
            Can also be input as[0:3]
            returns: [score,is_done] if the snake doesn't crash
                    final score if the snake crashes
        '''
        prev_snake_head= self.snake[0]
        if not isinstance(direction,list):
            direction = self.ACTION_dict[direction]
        if not self.is_pos_in_list(direction,self.VALID_DIRS):
            error_str = "Snake game INVALID ACTION %s"%(str(direction))
            raise RuntimeError(error_str)
        if direction[0] == direction[1] and direction[1] == 0:
            return [len(self.snake)-1,False]
        next_pos0 = (self.snake[0][0] + direction[0])%self.board_size[0]
        next_pos1 = (self.snake[0][1] + direction[1])%self.board_size[1]
        next_pos = [next_pos0,next_pos1]

        #Ignore step if the snake goes "backwards"
        if len(self.snake) == 1 or not self.is_pos_in_list(next_pos,[self.snake[1]]):
            if self.is_pos_in_list(next_pos,self.snake[:-1]):
                return [len(self.snake)-1,True]
            
            self.snake.insert(0,copy(next_pos)) #Add new head position to list
            if not self.is_pos_in_list(next_pos,[self.food_pos]): #Food wasn't eaten, remove last tail position from snake
                del self.snake[-1]
            else:
                #Food was eaten, find a new food spot
                #TODO: Will have issues when snake gets large, consider keeping list of free values?
                while self.is_pos_in_list(self.food_pos,self.snake):
                    self.food_pos =  self.get_rand_pos(self.board_size)

            if self.render:
                self.render_snake()
            #TODO:Implement some sort of save functionality
            dist_diff = sqrt(prev_snake_head[0]**2 + prev_snake_head[1]**2) - \
                sqrt(self.snake[0][0]**2 + self.snake[0][1]**2)
            if abs(dist_diff) > 1:
                dist_diff = 0
            score = len(self.snake)-1 + dist_diff
            return [score,False]
        else:
            return [len(self.snake)-1,False]

#------------------------------------END 'PUBLIC' FUNCTIONS-------------------------------
#----------------------------------BEGIN 'PRIVATE' FUNCTIONS------------------------------

    def is_pos_in_list(self,sublist,cont_list):
        for cont in cont_list:
            if not cmp(sublist,cont):
                return True
        return False
    def print_snake(self):
        snake_str = "{"
        for pos in self.snake:
            snake_str += str("%s,"%(str(pos)))
        snake_str = snake_str[:-1] + "}"
        print("PRINTING NEW SNAKE")
        print(snake_str)
    def render_snake(self):
        board = self.get_image()
        plt.figure(self.fig.number)
        plt.ion()
        plt.clf()
        plt.imshow(board)
        plt.show()
        plt.pause(1e-10)
        #plt.imsave("garbage.png",board)
def main_test():
    game = snake_game()

    for i in xrange(1000):
        score,is_done = game.step("right")
        if(is_done):
            print("Snake died at %d"%(score))
            break
        game.render_snake()
if __name__ == "__main__":
    main_test()

            
