from Window import Window
from Constants import *
from Board import Board
import Setting 
import pygame
import Assets



# handles window resizing
def on_resize(event:pygame.event.Event):
    Setting.WINDOW_WIDTH = event.x
    Setting.WINDOW_HEIGHT = event.y



window = Window() 
window.on_event_map[WINDOW_RESIZE].append(on_resize)


board = Board()
window.on_event_map[WINDOW_RESIZE].append(board.on_window_resize)
window.on_start.append(board.on_start)
window.on_update.append(board.on_update)

window.on_event_map[MOUSE_MOTION].append(board.on_mouse_motion)
window.on_event_map[MOUSE_DOWN].append(board.on_mouse_press)
window.on_event_map[MOUSE_UP].append(board.on_mouse_release)





window.update() # start updating





