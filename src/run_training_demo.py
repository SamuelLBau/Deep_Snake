import argparse
import gym
from snake_game import snake_game
import numpy as np

import matplotlib
matplotlib.use('Agg')#Fixes error on DSMP server
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from deepQ import deepQ


#These are used for image pre-processing
frame_list = []
num_frames = 0

def run_training(args):
    network= deepQ(**args)

    network.train()

    del network


def empty_preprocess_func(frame):
    return np.expand_dims(frame,2)

def mspacman_preprocess_func(frame):
    mspacman_c = 448 #210 + 164 + 74
    img = frame[1:176:2, ::2] # crop and downsize
    img = img.sum(axis=2) # to greyscale
    img[img==mspacman_c] = 0 # Improve contrast
    img = (img // 3 - 128).astype(np.int8) # normalize from -128 to 127
    return empty_preprocess_func(img)

def carracing_preprocess_func(frame):
    global frame_list
    global frame_num
    img =  frame[:,:,0] * 0.2125
    img += frame[:,:,1] * 0.7154
    img += frame[:,:,2] * 0.0721
    img -= 1
    if len(frame_list)==0:
        frame_list = np.array([img,img,img,img])
    else:
        frame_list = np.array([frame_list[1],frame_list[2],frame_list[3],img])
    img = frame_list[1] + frame_list[2]*2 + frame_list[3] * 3 + img * 4
    img = img/10
    img = (img // 3 - 128).astype(np.int8) # normalize from -128 to 127
    
    return empty_preprocess_func(img)
def snake_preprocess_func(frame):
    return empty_preprocess_func(frame)
def asteroids_preprocess_func(frame):
        img = frame[34:210:2, ::2] # crop and downsize
        img = img.sum(axis=2) # to greyscale
        return empty_preprocess_func(img)



def configure_mspacman_training():
    args = {}


    args["game_type"] = "MsPacman-v0"
    args["env"] = gym.make(args["game_type"])
    args["proto"] = "cfn/MsPacman-v0.prototxt"
    args["action_space"] = list(range(9))
    args["preprocess_func"] = mspacman_preprocess_func
    args["n_steps"]=4000000
    args["momentum"]=.95
    args["learning_rate"] = .001
    args["discount"] = .99
    args["epsilon_min"]=.100000
    args["epsilon_max"]=1.000000
    
    
    args["game_skip"] = 80
    args["minibatch_size"] = 32
    args["fresh"] = False
    args["learning_interval"] = 4

    args["save_rewards"] = True

    return args
    
def configure_carracing_training():
    args = {} 
    args["game_type"] = "CarRacing-v0"
    args["env"] = gym.make(args["game_type"])
    args["proto"] = "cfn/CarRacing-v0.prototxt"
    args["preprocess_func"] = carracing_preprocess_func
    
    #Discretize the action space
    render = True
    range0 = [-1,0,1]
    range1 = [1,0]
    range2 = [.2,0]
    action_space = []
    for i in range0:
        for j in range1:
            for k in range2:
                action_space.append([i,j,k])
    args["action_space"] = action_space
    
    args["n_steps"]=4000000
    args["game_skip"] = 50
    args["minibatch_size"] = 50
    args["discount"] = .95
    args["fresh"] = False
    args["save_rewards"] = True
    args["learning_interval"] = 1
    args["max_neg_reward_steps"] = 150
    
    return args

def configure_snake_training():
    args = {} 
    args["game_type"] = "snake"
    args["env"] = snake_game(board_size=[25,25])
    args["proto"] = "cfn/snakenet.prototxt"
    args["preprocess_func"] = snake_preprocess_func
    args["action_space"] = list(range(4))

    args["save_rewards"] = True
    args["game_skip"] = 0
    args["minibatch_size"] = 30
    args["learning_interval"] = 1
    
    return args

def configure_asteroids_training():
    args = {}


    args["game_type"] = "Asteroids-v0"
    args["env"] = gym.make(args["game_type"])
    args["proto"] = "cfn/Asteroids.prototxt"
    args["action_space"] = list(range(14))
    args["preprocess_func"] = asteroids_preprocess_func
    args["n_steps"]=4000000
    args["momentum"]=.95
    args["learning_rate"] = .001
    args["discount"] = .99
    args["epsilon_min"]=.100000
    args["epsilon_max"]=1.000000
    
    
    args["game_skip"] = 0
    args["minibatch_size"] = 32
    args["fresh"] = False
    args["learning_interval"] = 1

    args["save_rewards"] = True
    
    return args   
    
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Run a convolutional neural net on an openAI gym environment.')
    parser.add_argument("--env",type=str,help="Select a prototxt file to load up",required=False,default="MsPacman-v0")
    args = parser.parse_args()
    env = args.env

    if env == "MsPacman-v0":
        print("Running MsPacman training")
        args = configure_mspacman_training()
        run_training(args)
    elif env == "CarRacing-v0":
        print("Running CarRacing training")
        try:
            args = configure_carracing_training()
            run_training(args)
        except Exception as e:
            print("Failed to run CarRacing example,",str(e))
            print("CarRacing requires the Box2D Library, which can by tricky to install")
    elif env.lower() == "snake":
        print("Running Snake training")
        #try:
        args = configure_snake_training()
        run_training(args)
        #except Exception as e:
        #print("Failed to run Snake example,",str(e))
    elif env == "Asteroids-v0":
        print("Running Asteroids training")
        args = configure_asteroids_training()
        run_training(args)
    else:
        print("Unsupported training environment %s"%(env))





