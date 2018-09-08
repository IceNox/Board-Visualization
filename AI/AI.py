import collections
import random
import copy
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
                    print(piece.column, piece.row)
                    piece.kill()
                    break
        
        for piece in output.runes[Board.TEAM[self.side]]:
            if (piece.column, piece.row) == move[0][0]:
                piece.move(*move[0][1])
                break
        
        if move[0][2]:
            piece.flip_over()
        
        
        
        return output


class AI:
    
    state = collections.namedtuple("state", "root children depth")

    def __init__(self, board_state: Board) -> None:
        self.state  = AI.state(board_state, [], 0)
    
    @staticmethod
    def bruteforce(s: 'state') -> None:
        for move in s.root.get_moves():
            s.children.append(AI.state(s.root.apply_move(move), [], s.depth + 1))
    
    def BFS(self, depth: int) -> None:
        queue = [self.state]

        while queue:
            s = queue.pop(0)
            
            if s.depth < depth:
                self.bruteforce(s)
                for new_state in s.children:
                    queue.append(new_state)

def neighbour(position: tuple, direction: str) -> tuple:
    column, row = position
    column  = column + ("E" in direction) - ("W" in direction)
    row     = row    + ("S" in direction) - ("N" in direction)

    if 0 < column < 10 and 0 < row < 10:
        return (column, row)
    
    else:
        return None


game = [Board(Board.STARTINGRUNES)]
game[-1].display()

while True:
    user_input = input()

    if user_input == "":
        a = random.choice(game[-1].get_moves())
        game.append(game[-1].apply_move(a))
        print(a)
    else:
        game.pop()
    game[-1].display()

    print(game[-1].runes[0].dead, game[-1].runes[1].dead, game[-1].runes[2].dead)





















    
