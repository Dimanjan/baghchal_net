from .definitions import *
from .lookup_values import *

class Board:
    def __init__(self):
        self.board_array=[EMPTY_NUMBER]*TOTAL_INTERSECTIONS

        # place baghs
        for square in INITIAL_BAGH_SQ:
            self.put_bagh(square)

        self.bagh_occupancy=INITIAL_BAGH_SQ
        self.goat_occupancy=[]

        self.bagh_moves=self.legal_bagh_moves()
        self.goat_moves=self.legal_goat_moves()

        self.captured_goats=0
        self.turn=GOAT_NUMBER

        self.phase=PHASES['PLACEMENT']

        self.history={
            'positions':{},
            'index':{},
            'total_moves':0,
            'pgn_dict':[]
        }
        self.position_string = self.stringify_position()

        self.repetitions={}
        self.thrice_repetition=False

        self.draw = False
        self.victor=None
        self.game_end=False

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
        string=''
        for piece in self.board_array:
            string+=str(piece)
        return string
        
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
        if self.phase == PHASES['PLACEMENT']:
            return_dict={
                'moves':[],
                'total_moves':0
            }
            for square in self.board_array:
                if self.board_array[square] == EMPTY_NUMBER:
                    return_dict['moves'].append(square)
                    return_dict['total_moves']+=1
            return return_dict
            
        else:
            return_dict={
                'moves':{},
                'total_moves':0
            }
            for square in self.goat_occupancy:
                return_dict['moves'][square]=[]
                for connection in CONNECTIONS[square]:
                    if self.board_array[connection] == EMPTY_NUMBER:
                        return_dict['moves'][square].append(connection)
                        return_dict['total_moves']+=1            
            return return_dict

    def legal_bagh_moves(self):
        return_dict={
            'simple_moves':{},
            'jump_moves':{},
            'total_moves':0,
            'total_jump_moves':0
        }
        for square in self.bagh_occupancy:
            return_dict['simple_moves'][square]=[]
            return_dict['jump_moves'][square]=[]
            for connection in CONNECTIONS[square]:
                if self.board_array[connection] == EMPTY_NUMBER:
                    return_dict['simple_moves'][square].append(connection)
                    return_dict['total_moves']+=1
            for jump_connection in JUMP_CONNECTIONS[square]:
                if self.board_array[jump_connection['jump_destination']] == EMPTY_NUMBER and self.board_array[jump_connection['jump_over']] == GOAT_NUMBER:
                    return_dict['jump_moves'][square].append(jump_connection)
                    return_dict['total_moves']+=1
                    return_dict['total_jump_moves']+=1
        return return_dict

    def bagh_victory(self):
        if self.captured_goats >= 5:
            self.victor = BAGH_NUMBER
            self.game_end=True

    def goat_victory(self):
        if  self.bagh_moves['total_moves'] == 0:
            self.victor = GOAT_NUMBER
            self.game_end=True

    def is_draw(self):
        if self.goat_moves['total_moves'] == 0 or self.thrice_repetition == True:
            self.draw = True
            self.game_end=True

    def make_move(self,move_dict):
        #add history
        self.position_string = self.stringify_position()
        self.check_repetitions() #before updating history 

        self.history['pgn_dict'].append(move_dict)
        self.history['total_moves'] += 1
        self.history['positions'][self.position_string] = self.history['total_moves']
        self.history['index'][self.history['total_moves']] = self.position_string

        if move_dict['piece']==BAGH_NUMBER:
            self.remove_bagh(move_dict['from'])
            self.put_bagh(move_dict['to'])
            if 'captured' in move_dict:
                self.remove_goat(move_dict['captured'])
                self.captured_goats += 1
            
            self.goat_moves = self.legal_goat_moves()
            self.bagh_victory()

        else:
            self.put_goat(move_dict['to'])
            if 'from' in move_dict:
                self.remove_goat(move_dict['from']) 

            self.bagh_moves = self.legal_bagh_moves()
            self.goat_victory()  

        self.is_draw()
        if self.history['total_moves'] >= PLACEMENT:
            self.phase = PHASES['MOVEMENT']
        
        self.switch_turn()

    def move_back(self):
        
        self.uncheck_repetition() #this happens before history is reverted
        #remove history
        del self.history['index'][self.history['total_moves']]              
        del self.history['positions'][self.position_string] 
        self.history['total_moves'] -= 1
        self.position_string = self.history['index'][self.history['total_moves']] #revert to previous string

        move_dict = self.history['pgn_dict'].pop()  
        
        if move_dict['piece'] == BAGH_NUMBER:
            self.remove_bagh(move_dict['to'])
            self.put_bagh(move_dict['from'])
            if 'captured' in move_dict:
                self.put_goat(move_dict['captured'])
                self.captured_goats -= 1

        else:
            self.remove_goat(move_dict['to'])
            if 'from' in move_dict:
                self.put_goat(move_dict['from'])        

        if self.history['total_moves'] < PLACEMENT:
            self.phase = PHASES['PLACEMENT']

        self.draw=False
        self.victor=None
        self.game_end=False
        self.switch_turn()