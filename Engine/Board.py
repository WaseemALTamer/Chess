from .Constants import *
from .Pieces import *








class Board:
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        # board dimentions can be changed on the go
        self.width = width
        self.height = height
        self.grid: list[list[Piece|None]] = [[None]*width for _ in range(height)] # we need to set it up manually later

        self.move_index:int = 0 # this will increament by 1 each time
        self.special_moves:dict[callable] = {} # this will hold the special moves that you can excuate on the board
        
        self.killed_pieces:list[Piece] = [] # this will store the dead pieces that leave the board
        
        self.on_state_change: list[callable] = [] # this will be triggered when the state of the board changes
                                                  # this will excuate after a move happen  after the move_idex
                                                  # changes



    def setup_classic(self):
        """
            Populate the board in standard 8x8 chess arrangement. this will only
            work if the board has a width and height of 8x8
        """
        self.width = 8
        self.height = 8

        # to make things simpler and more readable we recreate the array and put everything in order
        self.grid = [
            [Rock(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rock(BLACK)],
            [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
            [Rock(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rock(WHITE)],
        ]
    

    def move(self, from_pos: tuple[int,int], to_pos: tuple[int,int]) -> bool:
        """
            from_pos - squre containing a piece
            to_pos - squre to move the piece on from pos

            if from_pos squre doesnt have a piece we return with false other
            wise move move and return True
        """

        piece = self.get_piece(from_pos)
        if not piece:
            return  False # indecate it didnt work
        
        result = self.set_piece(to_pos, piece) # move the piece to that squre
        if not result:
            return False
        

        self.forget_piece(from_pos) # remove  the piece from  the squre that we are on 
                                    # this we dont need to verfy it is already verfied 
                                    # from the get_piece
    
        #piece.has_moved = True # this will be handled by the Rules

        #self.trigger_state_change() # this function will be handled by the Rules

        return True # indecate it worked
    

    def get_piece(self, pos:tuple[int,int]) -> Piece|None:
        x, y = pos
        if self.in_bounds(pos):
            return self.grid[y][x]
        
        return None


    def set_piece(self, pos:tuple[int,int], piece: Piece|None) -> bool:
        x, y = pos
        if self.in_bounds(pos):
            self.grid[y][x] = piece
            return True
        return False
    

    def forget_piece(self, pos:tuple[int,int]) -> bool:
        x, y = pos
        if self.in_bounds(pos):
            self.grid[y][x] = None
            return True
        return False


    def in_bounds(self, pos:tuple[int,int])-> bool:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        else:
            return False


    def trigger_state_change(self):
        for func in self.on_state_change:
            func()

    



    def print_grid(self, cell_width=12):
        """
            this will print out the board game with all the pieces
            in the terminal
        """

        for row in self.grid:
            for piece in row:
                if isinstance(piece, Piece):
                    name = piece.__class__.__name__
                else:
                    name = "."

                print(name.ljust(cell_width), end="")
            print()  # newline ONLY at end of row


    def coord_diff(self, pos_1: tuple[int, int], pos_2: tuple[int, int]) -> tuple[int, int]:
        """
            Returns the difference vector from a to b.
        """
        return (pos_2[0] - pos_1[0], pos_2[1] - pos_1[1])
    

    def coord_mid(self, pos_1: tuple[int, int], pos_2: tuple[int, int]) -> tuple[int, int]:
        """
            Returns the midpoint between two coordinates.
            Assumes the midpoint lies on integer coordinates.
        """
        return ((pos_1[0] + pos_2[0]) // 2, (pos_1[1] + pos_2[1]) // 2)
                










