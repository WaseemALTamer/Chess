from .Constants import *






class Piece: # all the pieces are going to inheritance this class

    value:int = 0
    blocks_movement:bool = True # this indecate if other piece can jump over the piece
    base_move_rays: list[list[tuple[int, int]]] = []

    def __init__(self, color:str):


        self.color:str|None = color
        self.has_moved:int = 0 # 0 means it didnt move and it is increamented as we move the piece
        self.life_span = -1
        self.state = ALIVE

        self.possible_moves: list[tuple[int, int]] = []
        self.capture_directions = [] # this will be used for the pawns to specify capture directions for the special move
                                     # as pawns capture is considered to be a special move in this arcticutre

        self.move_direction_y = 0 # represent going forwrad this will be used for the pawns
        self.move_direction_x = 0 # this is an extra varable to code with it to make the code more editable

        self.on_kill:list[callable] = []    # this will be triggered after the piece is killed

        self.on_move:list[callable] = []    # this will be triggered after the piece moves
                                            # this function will get feed its pervious pos
                                            # it will also be feed its current pos make


    def kill_trigger(self):
        self.state = DEAD
        for function in self.on_kill:
            function()
    
    def move_trigger(self):
        self.has_moved += 1
        for function in self.on_move:
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
        self.base_move_rays = [
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
        self.base_move_rays = [
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

        self.move_direction_y = 1 # indecate we need to move Forward
        if color == WHITE:
            self.move_direction_y = -1 # indecate we need to move backward

        self.capture_directions = [
            (1, 1), # top right 
            (-1, 1) # top left
        ]

        self._base_move_rays = [
            [(0, self.move_direction_y), # once forward 
             (0, self.move_direction_y * 2)], # twice forward
        ]

    def create_ghost_pawn():
        """
           this function will be attached to the on_move for the
           piece it is in
        """

        pass


    
    @property
    def base_move_rays(self):
        """
            this methode lets us  over ride the base_move_rays 
            and now we can compute it on the go this is highly
            encouraged to do if you are  making dynamic pieces
        """

        rays = self._base_move_rays
        
        if self.has_moved:
            rays = [
                [self._base_move_rays[0][0]]
            ]

        return rays


    
    




class GhostPawn(Piece):
    def __init__(self, pawn_to_link:Pawn):
        super().__init__(pawn_to_link.color)
        self.value = 0

        self.life_span = 1 # this will make it live for one round and then disapper not kill
        self.blocks_movement = False # doesnt come in pieces way
        self.linked_pawn = pawn_to_link
        self.base_move_rays = [] # no moves

        self.on_kill.append(lambda: self.linked_pawn.kill_trigger()) # subscribe to the pawn kill event to kill the pawn







