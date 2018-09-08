import random
import copy
import time
import sys
import os

import Pieces


class Board:

    BOARDWIDTH  = 9
    BOARDHEIGHT = 9

    STARTINGRUNES = [ Pieces.RuneOblivion(1, 2, 1, False) , Pieces.RuneOblivion(5, 3, 1, False) , Pieces.RuneOblivion(9, 2, 1, False) ,
                      Pieces.RuneZero(1, 9, 1, False)     , Pieces.RuneZero(2, 8, 1, True)      , Pieces.RuneZero(3, 8, 1, False)     ,
                      Pieces.RuneZero(4, 8, 1, False)     , Pieces.RuneZero(5, 8, 1, True)      , Pieces.RuneZero(6, 8, 1, False)     ,
                      Pieces.RuneZero(7, 8, 1, False)     , Pieces.RuneZero(8, 8, 1, True)      , Pieces.RuneZero(9, 9, 1, False)     ,
                      Pieces.RuneOne(2, 9, 1, False)      , Pieces.RuneOne(8, 9, 1, True)       , Pieces.RuneFour(5, 9, 1, False)     ,
                      Pieces.RuneTwo(3, 9, 1, False)      , Pieces.RuneTwo(7, 9, 1, False)      ,
                      Pieces.RuneThree(4, 9, 1, False)    , Pieces.RuneThree(6, 9, 1, False)    ,
                      Pieces.RuneOblivion(1, 8, 2, False) , Pieces.RuneOblivion(5, 7, 2, False) , Pieces.RuneOblivion(9, 8, 2, False) ,
                      Pieces.RuneZero(1, 1, 2, False)     , Pieces.RuneZero(2, 2, 2, True)      , Pieces.RuneZero(3, 2, 2, False)     ,
                      Pieces.RuneZero(4, 2, 2, False)     , Pieces.RuneZero(5, 2, 2, True)      , Pieces.RuneZero(6, 2, 2, False)     ,
                      Pieces.RuneZero(7, 2, 2, False)     , Pieces.RuneZero(8, 2, 2, True)      , Pieces.RuneZero(9, 1, 2, False)     ,
                      Pieces.RuneOne(2, 1, 2, True)       , Pieces.RuneOne(8, 1, 2, False)      , Pieces.RuneFour(5, 1, 2, False)     ,
                      Pieces.RuneTwo(3, 1, 2, False)      , Pieces.RuneTwo(7, 1, 2, False)      ,
                      Pieces.RuneThree(4, 1, 2, False)    , Pieces.RuneThree(6, 1, 2, False)    , ]
    
    TEAM = {1 : slice(0 , 19),
            2 : slice(19, 38), }

    def __init__(self, runes: list, side=1, turn=1) -> None:

        self.side = side
        self.turn = turn

        self.runes = copy.deepcopy(runes)
        
        
    
    def display(self, external=True) -> None:

        if external == False:
            board = [["_"] * Board.BOARDWIDTH for i in range(Board.BOARDHEIGHT)]
            
            for rune in self.runes:
                board[rune.row - 1][rune.column - 1] = str(rune)[0].lower() if rune.owner == 2 else str(rune)[0]
            
            print("\n".join(map(lambda x: "".join(x), board)))
        
        else:
            file = open(os.path.join(os.path.dirname(__file__), "../Compiled/BoardData.txt"), "w")
            file.write("%s\n" %sum(1 for rune in self.runes if not rune.dead))

            for rune in self.runes:
                if not rune.dead:
                    file.write("%s %s %s\n" %(rune.column - 1, rune.row - 1, rune.image_id + rune.flip + 11 * (rune.owner == 2)))
            
            file.close()
            
    
    def get_moves(self) -> list:
        teammates = [(t.column, t.row)   for t in self.runes[Board.TEAM[self.side]][3:] if not t.dead]
        toblivion = [(t.column, t.row)   for t in self.runes[Board.TEAM[self.side]][:3] if not t.dead]
        deadteam  = [self.runes.index(t) for t in self.runes[Board.TEAM[self.side]][3:] if t.dead]
        enemyrune = [(e.column, e.row)   for e in self.runes[Board.TEAM[abs(self.side - 2) + 1]][3:] if not e.dead]
        eoblivion = [(e.column, e.row)   for e in self.runes[Board.TEAM[abs(self.side - 2) + 1]][:3] if not e.dead]

        moves = []

        for rune in self.runes[Board.TEAM[self.side]]:
            for move in rune.movelist():
                pos         = (rune.column, rune.row)
                movement    = [(rune.column, rune.row)]
                kills       = []

                flips = False

                try:
                    for step in move:
                        pos = neighbour(pos, step)

                        assert pos != None
                        assert pos not in eoblivion
                        
                        if pos in enemyrune:
                            kills.append(pos)
                        
                        elif pos in teammates:
                            flips = True

                except AssertionError:
                    continue
                
                if pos not in teammates:
                    movement.append(pos)
                    movement.append(flips)
                    moves.append((movement, kills, []))
                    
        return moves
    
    def apply_move(self, move: tuple) -> 'Board':
        output = Board(self.runes, side=(abs(self.side - 2) + 1), turn=(self.turn + abs(self.side % 2 - 1)))

        for kill in move[1]:
            for piece in output.runes:
                if (piece.column, piece.row) == kill:
                    piece.kill()
                    break
        
        for piece in output.runes[Board.TEAM[self.side]]:
            if (piece.column, piece.row) == move[0][0]:
                piece.move(*move[0][1])
                break
        
        if move[0][2]:
            piece.flip_over()
        
        
        
        return output


class State:
    
    def __init__(self, board_state: Board, depth=0) -> None:
        self.root       = board_state
        self.children   = []
        self.depth      = depth

    def bruteforce(self) -> None:
        for move in self.root.get_moves():
            self.children.append(State(self.root.apply_move(move), depth=self.depth+1))

    def evaluate(self, weights: dict) -> tuple:
        m_score1 = 0
        e_score1 = 0
        m_score2 = 0
        e_score2 = 0
        
        for rune in [r for r in self.root.runes if not r.dead]:
            if rune.owner == self.root.side:
                m_score1 += weights[type(rune)]
                m_score2 -= abs(rune.column - 5) + abs(rune.row - 5)
                
            else:
                e_score1 += weights[type(rune)]
                e_score2 -= abs(rune.column - 5) + abs(rune.row - 5)
            
        return (m_score1, sys.maxsize - e_score1, m_score2, sys.maxsize - e_score2)

class AI:

    def __init__(self, state: State) -> None:
        self.state  = state
    
    def BFS(self, depth: int) -> None:
        queue = [self.state]

        while queue:
            s = queue.pop(0)
            
            if s.depth < depth:
                s.bruteforce()
                for new_state in s.children:
                    queue.append(new_state)

    def minmax(self) -> State:
        w={Pieces.RuneZero : 1, Pieces.RuneOne : 2, Pieces.RuneTwo : 3, Pieces.RuneThree : 4, Pieces.RuneFour : 5, Pieces.RuneOblivion : 0}
        
        return max(self.state.children, key=lambda Q: min(Q.children, key=lambda y: y.evaluate(w)).evaluate(w))


def neighbour(position: tuple, direction: str) -> tuple:
    column, row = position
    column  = column + ("E" in direction) - ("W" in direction)
    row     = row    + ("S" in direction) - ("N" in direction)

    if 0 < column < 10 and 0 < row < 10:
        return (column, row)
    
    else:
        return None


game = [State(Board(Board.STARTINGRUNES))]
game[-1].root.display()

while True:
    user_input = ""

    if user_input == "":
        A = AI(State(game[-1].root))
        A.BFS(2)
        game.append(A.minmax())
        
    else:
        game.pop()
    game[-1].root.display()





















    
