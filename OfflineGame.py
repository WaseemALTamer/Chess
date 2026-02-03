from GUI.Containers.Board.Board import Board as DisplayBoard, Piece
from Engine import Rules, Board, Pieces, Constants as EngineConstant
from GUI.Window import Window
import GUI.Assets as Assets
from GUI.Constants import *
import GUI.Setting 
import pygame



# handles window resizing
def on_resize(event:pygame.event.Event):
    GUI.Setting.WINDOW_WIDTH = event.x
    GUI.Setting.WINDOW_HEIGHT = event.y



window = Window() 
window.on_event_map[WINDOW_RESIZE].append(on_resize)


display_board = DisplayBoard()
display_board.setup_board() # set up the board

# window event
window.on_event_map[WINDOW_RESIZE].append(display_board.on_window_resize)
window.on_start.append(display_board.on_start)
window.on_update.append(display_board.on_update)
window.on_event_map[WINDOW_RESIZE].append(display_board.on_resize)

# mouse events
window.on_event_map[MOUSE_MOTION].append(display_board.on_mouse_motion)
window.on_event_map[MOUSE_DOWN].append(display_board.on_mouse_press)
window.on_event_map[MOUSE_UP].append(display_board.on_mouse_release)


# we make a simple game here just for show case on how to use


def on_display_board_move(from_pos, to_pos):

    Rules.apply_move(game_board, from_pos, to_pos)
    Rules.calculate_all_legal_moves(game_board)

    for y, row in enumerate(game_board.grid):
        for x, piece in enumerate(row):
            square = display_board.grid[y][x]
            piece_pos = (x, y)

            if square.piece and piece:
                square.piece.possible_moves = piece.possible_moves

            if square.piece and not piece:
                square.piece.hide()
            
            if piece and not square.piece and piece.piece_to_track: # this needs to be tested
                piece.piece_to_track.show() # this ensure that the piece is visable
                display_board.move_piece(piece.piece_to_track, to_pos)
                


display_board.on_piece_move_callbacks.append(on_display_board_move) # append the on move trigger

game_board = Board() 
game_board.setup_classic() # set up the clasic chess postion
Rules.calculate_all_legal_moves(game_board) # caluclate the starting possible moves


for y, row in enumerate(game_board.grid):
    for x, piece in enumerate(row):
        square = display_board.grid[y][x]

        if piece:
            display_piece = Piece() # make a psquare.is_highlighted = Trueiece
            display_piece.board_pos = square.board_pos
            display_piece.possible_moves = piece.possible_moves
            display_piece.piece_engine = piece # we link the piece into the file it self
            square.piece = display_piece

            piece.piece_to_track = display_piece # this allow us to track the piece cor and transition
                                                 # if we need to do so 
            
        else:
            continue


        if isinstance(piece, Pieces.Pawn):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.pawn_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.pawn_black_surface.convert_alpha()

        if isinstance(piece, Pieces.King):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.king_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.king_black_surface.convert_alpha()

        if isinstance(piece, Pieces.Queen):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.queen_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.queen_black_surface.convert_alpha()

        if isinstance(piece, Pieces.Bishop):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.bishop_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.bishop_black_surface.convert_alpha()

        if isinstance(piece, Pieces.Knight):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.knight_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.knight_black_surface.convert_alpha()

        if isinstance(piece, Pieces.Rock):
            if piece.color == EngineConstant.WHITE:
                display_piece.image_surface = Assets.Images.rock_white_surface.convert_alpha() # attach the surface image and make it an alpah surface
            if piece.color == EngineConstant.BLACK:
                display_piece.image_surface = Assets.Images.rock_black_surface.convert_alpha()




window.update() # start updating





