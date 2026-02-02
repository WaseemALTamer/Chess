from Containers.Board.Board import Board, Piece
from Window import Window
from Constants import *
import Setting 
import pygame

import Assets as Assets



# handles window resizing
def on_resize(event:pygame.event.Event):
    Setting.WINDOW_WIDTH = event.x
    Setting.WINDOW_HEIGHT = event.y



window = Window() 
window.on_event_map[WINDOW_RESIZE].append(on_resize)


board = Board()
board.setup_board() # set up the board

# window event
window.on_event_map[WINDOW_RESIZE].append(board.on_window_resize)
window.on_start.append(board.on_start)
window.on_update.append(board.on_update)
window.on_event_map[WINDOW_RESIZE].append(board.on_resize)

# mouse events
window.on_event_map[MOUSE_MOTION].append(board.on_mouse_motion)
window.on_event_map[MOUSE_DOWN].append(board.on_mouse_press)
window.on_event_map[MOUSE_UP].append(board.on_mouse_release)



squre = board.grid[3][3] # pick a squre 
p = Piece() # make a piece
p.image_surface = Assets.Images.ghost_pawn_surface.convert_alpha() # attach the surface image and make it an alpah surface
p.board_pos = squre.board_pos
p.possible_moves = [(1, 2), (3, 4), (3, 5), (2, 2), (0, 0)] # give the piece possible moves
squre.piece = p


squre = board.grid[2][2] # pick a squre 
p = Piece() # make a piece
p.image_surface = Assets.Images.ghost_pawn_surface.convert_alpha() # attach the surface image and make it an alpah surface
p.board_pos = squre.board_pos
p.possible_moves = [(1, 2), (3, 4), (3, 5), (2, 2), (0, 0)] # give the piece possible moves
squre.piece = p




window.update() # start updating





