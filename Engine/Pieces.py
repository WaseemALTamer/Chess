from Constants import *






class Piece: # all the pieces are going to inheritance this class

    # Per-type constants
    value:int = 0
    blocks_movement:bool = True # this indecate if other piece can jump over the piece
    base_move_rays: list[list[tuple[int, int]]] = []
    default_life_span = -1 # -1 < 0 indecate it lives forever, as 0 will delet it and we sub -1 each time

    def __init__(self, color:str):
        self.color:str|None = color
        self.has_moved: bool = False
        self.life_span = self.default_life_span
        self.on_kill:list[callable] = []
        self.possible_moves: list[tuple[int, int]] = []


    def kill(self):
        for function in self.on_kill:
            function()




class King(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 0

        self.blocks_movement = True
        self.base_move_rays =   [
            [(1,-1)], [(0,1)], [(1,1)],
            [(-1,0)],          [(1,0)],
            [(-1,-1)],[(0,-1)],[(1,-1)]
        ]


class Queen(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 9

        self.blocks_movement = True
        self.base_move_rays =[
            [(i, i) for i in range(1, MAX_RANGE)] , [(i, -i) for i in range(1, MAX_RANGE)],     # UP-RIGHT, DOWN-RIGHT 
            [(-i, i) for i in range(1, MAX_RANGE)] , [(-i, -i) for i in range(1, MAX_RANGE)],   # UP-LEFT, DOWN-LEFT
            [(i, 0) for i in range(1, BOARD_WIDTH)] , [(0, i) for i in range(1, BOARD_HEIGHT)] ,     # RIGHT, LEFT
            [(-i, 0) for i in range(1, BOARD_WIDTH)] , [(0, -i) for i in range(1, BOARD_HEIGHT)]     # DOWN, UP 
        ]    


class Rock(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 5

        self.blocks_movement = True
        self.base_move_rays = [ 
            [(i, 0) for i in range(1, BOARD_WIDTH)] , [(0, i) for i in range(1, BOARD_HEIGHT)],  # RIGHT, LEFT               
            [(-i, 0) for i in range(1, BOARD_WIDTH)] , [(0, -i) for i in range(1, BOARD_HEIGHT)] # DOWN, UP 
        ]    



class Bishop(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 3

        self.blocks_movement = True
        self.base_move_rays =[
            [(i, i) for i in range(1, MAX_RANGE)] , [(i, -i) for i in range(1, MAX_RANGE)],     # UP-RIGHT, DOWN-RIGHT
            [(-i, i) for i in range(1, MAX_RANGE)] , [(-i, -i) for i in range(1, MAX_RANGE)],   # UP-LEFT, DOWN-LEFT
        ]

class Knight(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 3

        self.blocks_movement = True
        self.base_move_rays = [
            [(2,1)],[(2,-1)],
            [(-2,1)],[(-2,-1)],
            [(1,2)],[(-1,2)],
            [(1,-2)],[(-1,-2)]
        ]


class Pawn(Piece):
    def __init__(self, color:str):
        super().__init__(color)
        self.value = 1

        self.blocks_movement = True
        self.base_move_rays =[
            [(0, 1)]
        ] # other moves for the pawn is handled by the rules




class GhostPawn(Piece):
    def __init__(self, pawn_to_link:Pawn):
        super().__init__(pawn_to_link.color)
        self.value = 0

        self.life_span = 1 # this will make it live for one round and then disapper not kill
        self.blocks_movement = False
        self.linked_pawn = pawn_to_link

        self.on_kill.append(lambda: self.linked_pawn.kill()) # subscribe to the pawn kill event to kill the pawn







