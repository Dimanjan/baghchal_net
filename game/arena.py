import random
from definitions import *
from lookup_values import *
from board import Board

mode='random' # or 'nnet'
f = open("data.txt", "a")

def create_games(n):

    for i in range(n):
        brd=Board()
        if mode=='nnet':
            pass 
        else:
            while brd.game_end==False:
                if brd.turn==BAGH_NUMBER:

                    mv=random.choice(brd.bagh_moves)
                    brd.make_move(mv)
                else:
                    mv=random.choice(brd.goat_moves)
                    brd.make_move(mv)
        for s in brd.history['pgn']:
            f.write(str(s))
            f.write(',')

        f.write(str(brd.victor))

        f.write('\n')
        
    f.close()
  

create_games(3)





