RUNEZERONAME    = "Pawn"
RUNEONENAME     = "Rook"
RUNETWONAME     = "Bishop"
RUNETRHEENAME   = "Knight"
RUNEFOURNAME    = "Queen"
RUNEOBLNAME     = "Oblivion"
EMPTYTILE       = "_"


class Rune:
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        self.column = column
        self.row    = row
        self.owner  = owner
        self.flip   = flipped

        self.dead   = False
    
    def flip_over(self) -> None:
        self.flip = not self.flip
    
    def kill(self) -> None:
        self.dead   = True
        self.column = -1
        self.row    = -1
    
    def move(self, column: int, row: int) -> None:
        self.column = column
        self.row = row
    
    def movelist(self) -> list:
        return self.__class__.MOVES[self.flip][self.owner]


class RuneZero(Rune):

    MOVES = { True  : { 1 : [("NW",     ), ("N",     ), ("NE",     ), ("E",     ),               ("S",     ),               ("W",     ), ], 
                        2 : [              ("N",     ),               ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], },
              False : { 1 : [              ("N",     ),               ("E",     ),                                          ("W",     ), ], 
                        2 : [                                         ("E",     ),               ("S",     ),               ("W",     ), ], }, }
    
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)
        
        self.image_id = 0
        
    def __str__(self) -> str:
        return RUNEZERONAME
    
    def get_moves(self, player: int) -> list:
        if player == 1:
            if self.flip:
                return ["N", "E", "W"]
            
            else:
                return 

class RuneOne(Rune):

    MOVES = { True  : { 1 : [("NW", "NE"), ("N", "E" ), ("NE", "SE"), ("E", "S" ), ("SE", "SW"), ("S", "W" ), ("SW", "NW"), ("W", "N" ),
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ],
                        2 : [("NW", "NE"), ("N", "E" ), ("NE", "SE"), ("E", "S" ), ("SE", "SW"), ("S", "W" ), ("SW", "NW"), ("W", "N" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], }, 
              False : { 1 : [("NW", "SW"), ("N", "W" ), ("NE", "NW"), ("E", "N" ), ("SE", "NE"), ("S", "E" ), ("SW", "SE"), ("W", "S" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], 
                        2 : [("NW", "SW"), ("N", "W" ), ("NE", "NW"), ("E", "N" ), ("SE", "NE"), ("S", "E" ), ("SW", "SE"), ("W", "S" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], }, }
    
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)

        self.image_id = 2
        
    def __str__(self) -> str:
        return RUNEONENAME


class RuneTwo(Rune):

    MOVES = { True  : { 1 : [("NW", "SE"), ("N", "S" ), ("NE", "SW"), ("E", "W" ), ("SE", "NW"), ("S", "N" ), ("SW", "NE"), ("W", "E" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], 
                        2 : [("NW", "SE"), ("N", "S" ), ("NE", "SW"), ("E", "W" ), ("SE", "NW"), ("S", "N" ), ("SW", "NE"), ("W", "E" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], }, 
              False : { 1 : [("NW", "NW"), ("N", "N" ), ("NE", "NE"), ("E", "E" ), ("SE", "SE"), ("S", "S" ), ("SW", "SW"), ("W", "E" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], 
                        2 : [("NW", "NW"), ("N", "N" ), ("NE", "NE"), ("E", "E" ), ("SE", "SE"), ("S", "S" ), ("SW", "SW"), ("W", "E" ), 
                             ("NW",     ), ("N",     ), ("NE",     ), ("E",     ), ("SE",     ), ("S",     ), ("SW",     ), ("W",     ), ], }, }
    
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)

        self.image_id = 4
    
    def __str__(self) -> str:
        return RUNETWONAME


class RuneThree(Rune):

    MOVES = { True  : { 1 : [("NW", "N" ),              ("NE", "E" ),              ("SE", "S" ),              ("SW", "W" ),
                             ("NW", "W" ),              ("NE", "N" ),              ("SE", "E" ),              ("SW", "E" ),              
                             ("NW",     ),              ("NE",     ),              ("SE",     ),              ("SW",     ),              ],
                        2 : [("NW", "N" ),              ("NE", "E" ),              ("SE", "S" ),              ("SW", "W" ),
                             ("NW", "W" ),              ("NE", "N" ),              ("SE", "E" ),              ("SW", "E" ),              
                             ("NW",     ),              ("NE",     ),              ("SE",     ),              ("SW",     ),              ], },
              False : { 1 : [              ("N", "NE"),               ("E", "SE"),               ("S", "SW"),               ("W", "NW"), 
                                           ("N", "NW"),               ("E", "NE"),               ("S", "SE"),               ("W", "SW"), 
                                           ("N",     ),               ("E",     ),               ("S",     ),               ("W",     ), ], 
                        2 : [              ("N", "NE"),               ("E", "SE"),               ("S", "SW"),               ("W", "NW"), 
                                           ("N", "NW"),               ("E", "NE"),               ("S", "SE"),               ("W", "SW"),
                                           ("N",     ),               ("E",     ),               ("S",     ),               ("W",     ), ], }, }

    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)

        self.image_id = 6
    
    def __str__(self) -> str:
        return RUNETRHEENAME


class RuneFour(Rune):

    MOVES = { True  : { 1 : [], 2 : [], },
              False : { 1 : [], 2 : [], }, }
    
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)

        self.image_id = 8
        
    def __str__(self) -> str:
        return RUNEFOURNAME


class RuneOblivion(Rune):

    MOVES = { True  : { 1 : [], 2 : [], },
              False : { 1 : [], 2 : [], }, }
    
    def __init__(self, column: int, row: int, owner: int, flipped: bool) -> None:
        super().__init__(column, row, owner, flipped)

        self.image_id = 10
    
    def __str__(self) -> str:
        return RUNEOBLNAME
