from definitions import *
from lookup_values import *

class Board:
    def __init__(self):
        self.board_array=[EMPTY_NUMBER]*TOTAL_INTERSECTIONS
        self.bagh_occupancy=[0,4,20,24]
        self.goat_occupancy=[]

        # initialize baghs
        for square in [0,4,20,24]:
            self.board_array[square]=BAGH_NUMBER

        self.phase=PHASES['PLACEMENT']
        self.position_string = self.stringify_position()

        self.trapped_baghs=[]
        self.captured_goats=0
        self.turn=GOAT_NUMBER


        self.history={
            'positions':[],
            'pgn':[]
        }
        

        self.repetitions={}
        self.thrice_repetition=False

        self.draw = False
        self.victor=None
        self.game_end=False

        self.bagh_moves=self.legal_bagh_moves()
        self.goat_moves=self.legal_goat_moves()

             
        

    def switch_turn(self):
        if self.turn == BAGH_NUMBER:
            self.turn = GOAT_NUMBER
        else:
            self.turn = BAGH_NUMBER

    def check_repetitions(self):
        if self.position_string in self.history['positions']:
            if self.position_string not in self.repetitions:
                self.repetitions[self.position_string] = 1
            else:
                self.repetitions[self.position_string] += 1
                # is this third time?
                if self.repetitions[self.position_string] >= 3:
                    self.thrice_repetition = True

    def uncheck_repetition(self):
        if self.position_string in self.repetitions:
            if self.repetitions[self.position_string] == 1:
                del self.repetitions[self.position_string]
            else:
                self.repetitions[self.position_string] -= 1                
                self.thrice_repetition = False #for both 3 and 2

    def stringify_position(self):
        return ''.join(str(i) for i in self.board_array)
        
    def put_bagh(self,square):
        self.board_array[square]=BAGH_NUMBER
        self.bagh_occupancy.append(square)

    def put_goat(self,square):
        self.board_array[square]=GOAT_NUMBER
        self.goat_occupancy.append(square)

    def remove_bagh(self,square):
        self.board_array[square]=EMPTY_NUMBER
        self.bagh_occupancy.remove(square)

    def remove_goat(self,square):
        self.board_array[square]=EMPTY_NUMBER
        self.goat_occupancy.remove(square)

    def legal_goat_moves(self):
        self.legal_bagh_moves() #for updating number of trapped baghs since a move by bagh itself may trap or release another bagh
        return_l =[]              
        if self.phase == PHASES['PLACEMENT']:            
            for square in range(len(self.board_array)):
                if self.board_array[square] == EMPTY_NUMBER:
                    return_l.append(GOAT_LETTER+f"{square:02d}")            
        else:
            for square in self.goat_occupancy:
                for connection in CONNECTIONS[square]:
                    if self.board_array[connection] == EMPTY_NUMBER:
                        return_l.append(GOAT_LETTER+f"{connection:02d}"+f"{square:02d}")
        return return_l

    def legal_bagh_moves(self):
        self.trapped_baghs=[]
        return_l=[]
        for square in self.bagh_occupancy:
            nomove=True
            for connection in CONNECTIONS[square]:
                if self.board_array[connection] == EMPTY_NUMBER:
                    nomove=False
                    return_l.append(BAGH_LETTER+f"{connection:02d}"+f"{square:02d}")                    
            for jump_connection in JUMP_CONNECTIONS[square]:
                if self.board_array[jump_connection['jump_destination']] == EMPTY_NUMBER and self.board_array[jump_connection['jump_over']] == GOAT_NUMBER:
                    nomove=False
                    return_l.append(BAGH_LETTER+f"{jump_connection['jump_destination']:02d}"+f"{square:02d}"+f"{jump_connection['jump_over']:02d}")                    
            if nomove:
                self.trapped_baghs.append(square)


        return return_l

    def bagh_victory(self):
        if self.captured_goats >= 5:
            self.victor = BAGH_NUMBER
            self.game_end=True

    def goat_victory(self):
        if  len(self.bagh_moves)==0:
            self.victor = GOAT_NUMBER
            self.game_end=True

    def is_draw(self):
        if len(self.goat_moves) == 0 or self.thrice_repetition == True:
            self.draw = True
            self.game_end=True

    def make_move(self,move):

        if move[0]==BAGH_LETTER:
            self.remove_bagh(int(move[3:5]))
            self.put_bagh(int(move[1:3]))
            if move[5:7]:
                self.remove_goat(int(move[5:7]))
                self.captured_goats += 1            
            self.goat_moves = self.legal_goat_moves()
            self.bagh_victory()
            self.bagh_moves=['noturn']

        else:
            self.put_goat(int(move[1:3]))
            if move[3:5]:
                self.remove_goat(int(move[3:5])) 

            self.bagh_moves = self.legal_bagh_moves()
            self.goat_victory()  
            self.goat_moves = ['noturn']

        self.is_draw()
        if len(self.history['pgn']) == PLACEMENT:
            self.phase = PHASES['MOVEMENT']
        
        self.switch_turn()

        #add history
        self.position_string = self.stringify_position()
        self.check_repetitions() #before updating history 

        self.history['pgn'].append(move)
        self.history['positions'].append(self.position_string)

    def move_back(self):
        
        self.uncheck_repetition() #this happens before history is reverted

        move = self.history['pgn'].pop()  
        
        if move[0] == BAGH_LETTER:
            self.remove_bagh(int(move[1:3]))
            self.put_bagh(int(move[3:5]))
            if move[5:7]:
                self.put_goat(int(move[5:7]))
                self.captured_goats -= 1

        else:
            self.remove_goat(int(move[1:3]))
            if move[3:5]:
                self.put_goat(int(move[3:5]))        

        if len(self.history['pgn']) < PLACEMENT:
            self.phase = PHASES['PLACEMENT']

        self.draw=False
        self.victor=None
        self.game_end=False
        self.switch_turn()
        self.history['positions'].remove(self.position_string)
        self.position_string = self.stringify_position() #revert to previous string


brd=Board()
brd.make_move('G01')
brd.move_back()
print(brd.bagh_moves)
print(brd.goat_moves)

brd.make_move('B0500')
print(brd.bagh_moves)
print(brd.goat_moves)

