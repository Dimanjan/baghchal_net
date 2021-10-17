

from definitions import *
from board import *

def evaluation(board):
    INFINITY=30000
    goat_value=[100,250,700,2000,INFINITY]
    bagh_value=[100,250,700,INFINITY]

    return goat_value[board.captured_goats] - bagh_value[len(board.trapped_baghs)]

     
def max(depth,board):
    best=-INFINITY
    if depth==0:
        return evaluation(board)
    #print(board.bagh_moves)
    
    for mv in board.bagh_moves:
        #print(mv)

        if board.game_end == False:
            board.make_move(mv)
            val=min(depth-1,board) 
            board.move_back()
            if val>best:
                best=val
    return best

def min(depth,board):
    best=INFINITY
    if depth==0:
        return evaluation(board)
    #print(board.goat_moves)
    for mv in board.goat_moves:
        #print(mv)
        if board.game_end == False:
            board.make_move(mv)
            val=max(depth-1,board) 
            board.move_back()
            if val<best:
                best=val
    return best

     
         
def minimax(depth,board):
    count=0
    if board.turn==GOAT_NUMBER:
        return min(depth,board)
    else:
        return max(depth,board)

def mxv(d):
    print(d)
    k=list(d.keys())
    print(k)
    kx=k[0]
    mx=d[k[0]]
    for i in range(len(k)):
        if d[k[i]]>mx:
            kx=k[i]
            mx=d[k[i]]
            
    return [kx,mx]

def mnv(d):
    print(d)
    k=list(d.keys())
    print(k)
    kx=k[0]
    mn=d[k[0]]
    for i in range(len(k)):
        if d[k[i]]<mn:
            kx=k[i]
            mn=d[k[i]]
            
    return [kx,mn]


def best_mm(depth,board):
    d={}
    if board.turn==GOAT_NUMBER:
        for mv in board.goat_moves:
            board.make_move(mv)
            d[mv]=minimax(depth,board)
            board.move_back()

        return mnv(d)
    else:
        for mv in board.bagh_moves:
            board.make_move(mv)
            d[mv]=minimax(depth,board)
            board.move_back()
        return mxv(d)
        


brd=Board()


print(best_mm(2 ,brd))

# print(brd.goat_moves)
# brd.make_move('G01')
# print(brd.bagh_moves)
# brd.make_move('B020001')
# print(brd.captured_goats)
# print(evaluation(brd))
