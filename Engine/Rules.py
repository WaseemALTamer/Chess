# this rule book only works for 2 player chess game if you want more player chess game then 
# consider editing the functions to fit your 4 player chess game




from Board import Board
from Pieces import *
import Constants





class Rules:
    @staticmethod
    def calculate_all_moves(board: Board):
        """
            Recalculate possible_moves for all pieces

        """
        for x, row in enumerate(board.grid):
            for y, piece in enumerate(row):
                pos = (x, y)
                Rules.calculate_piece_moves(board, pos) # calculate
                


    @staticmethod
    def calculate_piece_moves(board: Board, pos:tuple[int, int]):
        """
            Populate possible_moves for a single piece

            this function will not elemnate the moves that puts
            your king in danger
        """

        piece = board.get_piece(pos)
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
                    if target_piece.blocks_movement:
                        if target_piece.color == piece.color:
                            break # exit that ray and move to check another direction
                        else:
                            piece.possible_moves.append(end_pos)
                            break # exit that ray and move to check another direction
                else:
                    piece.possible_moves.append(end_pos)



    @staticmethod
    def filter_king_safety(board: Board):
        """
            Remove moves that leave king in check

            this will play the move on a virtual board check if the king
            is exposed and will remove the move if the king is exposed
        """



    @staticmethod
    def get_special_moves(board:Board):
        """
            Returns special moves (castling, en passant, promotion)
            without executing them
        """

    @staticmethod
    def is_players_turn(board:Board):
        """
            this function will return whos trun it is
        """

        if board.move_index % 2:
            return Constants.WHITE
        else:
            return Constants.BLACK

    
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

        if target_piece:
            target_piece.kill() # the piece is killed
            board.forget_piece(to_pos) # this will forget the piece
        
        board.move(from_pos, to_pos) # now we are free to move the piece to that square
        piece.has_moved = True
        




    @staticmethod
    def is_square_attacked(board: Board, pos:tuple[int, int], except_color:str) -> bool:
        """
            this function checks is attacked by a certain color
            you can keep the except_color  to check  if the pos
            is attacked by either color
        """

        pos = (x, y)
        for x, row in enumerate(board.grid):
            for y, piece in enumerate(row):
                if isinstance(piece, Piece) and piece.color != except_color:
                    if pos in piece.possible_moves:
                        return True
        
        return False
                    



    @staticmethod
    def update(board:Board):
        """
            this function will take a  Board which represent the game
            it will calcualte  all the  possible  moves calculate the
            special moves, and it will provide them inside the pieces
            inside  the board  grid, this  update function  should be
            excuate once per postion  
        """

        pass

