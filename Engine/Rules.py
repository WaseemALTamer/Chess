# this rule book only works for 2 player chess game if you want more player chess game then 
# consider editing the functions to fit your 4 player chess game




from .Board import Board
from . import Constants
from .Pieces import *
import copy




class Rules:
    @staticmethod
    def calculate_all_moves(board: Board):
        """
            Recalculate possible_moves for all pieces

            this function will not elemnate the moves that puts
            your king in danger

        """
        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                pos = (x, y)
                if piece:
                    Rules.calculate_piece_moves(board, pos) # calculate surface level moves for the piece



    @staticmethod
    def calculate_piece_moves(board: Board, pos:tuple[int, int]):
        """
            Populate possible_moves for a single piece

            this function will not elemnate the moves that puts
            your king in danger
        """

        piece = board.get_piece(pos)
        if not piece:
            return

        piece.possible_moves = [] # remove all the possible moves from before if there is any


        pos_x, pos_y = pos

        for move_ray in piece.base_move_rays:
            for transition in move_ray:
                dx, dy = transition
                end_pos = (pos_x + dx, pos_y + dy)

                if not board.in_bounds(end_pos):
                    break  # rays stop at board edge

                target_piece  = board.get_piece(end_pos)
                if isinstance(target_piece, Piece):
                    if isinstance(piece, Pawn):
                        break # pawn doesnt capture forward at this point the pawn only moves forward and no capture moves

                    if target_piece.blocks_movement:
                        if target_piece.color == piece.color:
                            break # exit that ray and move to check another direction
                        else:
                            piece.possible_moves.append(end_pos) # adds it if the piece is an enmy
                            break # exit that ray and move to check another direction
                    else:
                        piece.possible_moves.append(end_pos) # adds it if the piece doesnt block
                else:
                    piece.possible_moves.append(end_pos) # adds it if there is no piece in the way



    @staticmethod
    def filter_king_safety(board: Board):
        """
            Remove moves that leave king in check

            this will play the move on a virtual board check if the king
            is exposed and will remove the move if the king is exposed
        """

        #current_turn_color = Rules.players_turn(board)
        

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                
                if not piece:
                    continue

                #if piece.color != current_turn_color:
                #    continue

                piece_pos = (x, y)
                legal_moves = []

                for move in piece.possible_moves:
                    board_copy = Rules.copy_board(board)
                    Rules.apply_move(board_copy, piece_pos, move)
                    Rules.calculate_all_moves(board_copy) # recalculate the possible moves that can be made at a surface level
                    Rules.calculate_pawns_capture_moves(board_copy) # this calculate the pawns capture moves if they are possible
                    king_pos = Rules.find_king(board_copy, piece.color)
                    is_attacked = Rules.is_square_attacked(board_copy, king_pos, piece.color)
                    if not is_attacked:
                        legal_moves.append(move)
                    
                
                piece.possible_moves = legal_moves


    def filter_moves_by_turn(board:Board):
        """
            this removes all the possible moves for a set of pieces
            where the turn is not theres
        """

        current_turn_color = Rules.players_turn(board)

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                
                if not piece:
                    continue

                if piece.color != current_turn_color:
                    piece.possible_moves = []




    @staticmethod
    def calculate_all_special_moves(board:Board):
        """
            this function  will handel exception  rules that go
            against the arcticutre it is not  the best sloution
            but it is better to keep all the parts that cant be
            made with the arcticutre as a special move

            
            this function is  going to  handel casling and pawn
            capture 
        """

        Rules.calculate_pawns_capture_moves(board)


    @staticmethod
    def calculate_pawns_capture_moves(board:Board):
        """
            this function will  handel the capturing  for pawns
            this  will be mostly  a hard coded  check it doesnt
            come from the piece it self since it is 

            this function should be calculated before you start
            chcking for king safty

            this function can be refactored into a function that
            calculates one pawn captures and  then this function
            which loops over the pawns and run  them through the
            function this will result in extra checks 
        """


        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                if not isinstance(piece, Pawn):
                    continue

                for dx, dy in piece.capture_directions:
                    target_square = (
                        x + dx, 
                        y + (dy * piece.move_direction_y) # compute the direction on the board
                    )
                    if not board.in_bounds(target_square):
                        continue

                    target_piece = board.get_piece(target_square)
                    if isinstance(target_piece, Piece) and target_piece.color != piece.color:
                        piece.possible_moves.append(target_square)
                     
                        


    def calculate_casling_moves(board:Board):
        """
            this function  will check if casling is possible if
            it is then it will  make a simple  function that we
            can excuate on the go and add it to special move on
            the board
        """



    @staticmethod
    def players_turn(board:Board):
        """
            this function will return whos trun it is
        """

        if board.move_index % 2:
            return Constants.BLACK
        else:
            return Constants.WHITE

    
    @staticmethod
    def apply_move(board: Board, from_pos:tuple[int, int], to_pos:tuple[int, int]) -> bool:
        """
            this function will double check that the move is possible then
            it will apply the move, and handel the capture logic 
        """

        piece = board.get_piece(from_pos)


        if not piece:
            return False # nothing to move 

        if to_pos not in piece.possible_moves:
            return False # move is not possible
        
        target_piece = board.get_piece(to_pos)

        if  isinstance(target_piece, GhostPawn) and not isinstance(piece, Pawn):
            board.forget_piece(to_pos)  # this will forget the piece we dont kill 
                                        # the gohstpawn unless its kiled by pawn
        elif isinstance(target_piece, Piece):
            board.killed_pieces.append(target_piece)
            target_piece.kill_trigger() # the piece is killed
            board.forget_piece(to_pos)  # this will forget the piece
        
        board.move(from_pos, to_pos) # now we are free to move the piece to that square
        piece.move_trigger()


        Rules.age_and_cleanup_pieces(board) # this reduces the pieces life and removes the dead pieces if there is any
        

        # now we check if we need to create a ghost pawn
        if isinstance(piece, Pawn):
            pos_dif = board.coord_diff(from_pos, to_pos) # calculate the difference in the two coords
            dx, dy = pos_dif
            if abs(dy) == 2: # this check if we moved up or down twice on the board
                pos_mid = board.coord_mid(from_pos, to_pos)
                ghost_pawn = GhostPawn(piece)
                board.set_piece(pos_mid, ghost_pawn)

                
        board.move_index += 1 # increament the baord counter
        board.trigger_state_change() # excuate the subscriped function to the state
        


    @staticmethod
    def is_square_attacked(board: Board, pos:tuple[int, int], except_color:str) -> bool:
        """
            this function checks is attacked by a certain color
            you can keep the except_color  to check  if the pos
            is attacked by either color
        """

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                if isinstance(piece, Piece) and piece.color != except_color:
                    if pos in piece.possible_moves:
                        return True
        
        return False
    
    @staticmethod
    def age_and_cleanup_pieces(board: Board):
        """
            this will  reduce pieces lifespan until it is zero
            if it is zero it will foget  them   from the board
            it will not kill them, this is made purely for the
            ghostpawn which will make en- passant possible and
            to track the  other pieces  states and  remove the
            dead ones
        """

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                if piece:
                    piece_pos = (x, y)
                    piece.life_span -= 1
                    if piece.life_span == 0 or piece.state == DEAD:
                        board.forget_piece(piece_pos)
    

    @staticmethod
    def copy_board(board:Board) -> Board:
        """
            this function will make a copy  of the board  and will only
            copy the relevent matter  for validifying  moves and seeing
            if squres are in danger
        """

        
        board_copy = Board() # this doesnt make the grid it self
        board_copy.grid = copy.deepcopy(board.grid)

        board_copy.width = board.width
        board_copy.height = board.height


        board_copy.move_index = board.move_index


        return board_copy
    

    @staticmethod
    def find_king(board:Board, color:str) -> tuple[int, int]|None:
        """
            this will find the king for a specific color
        """

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == color:
                    pos = (x, y)
                    return pos
        
        return None
    
                    



    @staticmethod
    def calculate_all_legal_moves(board:Board):
        """
            this function will take a  Board which represent the game
            it will calcualte  all the  possible  moves calculate the
            special moves, and it will provide them inside the pieces
            inside  the board  grid, the speical moves will be inside 
            a the board.special_moves as a function that you can this  
            call update function  should be excuate once per postion  
        """

        Rules.calculate_all_moves(board) # calculates surface moves no king safty concern
        Rules.calculate_all_special_moves(board) # this will get all the special moves
        Rules.filter_king_safety(board) # removes that moves that puts the king under attack
        #Rules.filter_moves_by_turn(board) # this filters the pieces that dont have turn


