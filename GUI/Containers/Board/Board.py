from .Square import Square
from .Piece import Piece
import Setting 
import pygame




        





class Board:
    def __init__(self):
        self.grid:list[list[Square]] = []
        self.render_surface:pygame.Surface = None
        self.render_rect:pygame.Rect = None
        self.board_pos = (0, 0)

        self.selected_piece:Piece = None

        self.dead_piece:list[Piece] = [] # this is going to contain all the dead pieces that are out of the game


        # this is call back section attach functions and this will run them for you
        self.on_piece_move_callbacks:list[callable] = []

        # those are public var so  you can keep track of where you 
        # pressed for the functions to  use on  the  run they will
        # contain only mouse local pos not public window mouse pos
        self.right_press_pos = (0, 0)
        self.left_press_pos = (0, 0) 


    def setup_board(self):
        self.grid = [
            [Square() for _ in range(Setting.BOARD_SQURE_WIDTH)]
            for _ in range(Setting.BOARD_SQURE_HEIGHT)
        ]


        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                if (x + y) % 2 == 0:
                    square.base_color = Setting.WHITE_SQUARE_COLOR
                else:
                    square.base_color = Setting.BLACK_SQUARE_COLOR

                square.board_pos = (x, y)
                square.notation = f"{chr(ord('a') + x)}{y + 1}"

        # this is for testing
        #squre = self.grid[3][3] 
        #p = Piece()
        #p.image_surface = Assets.Images.ghost_pawn_surface
        #p.pixle_size = (squre.size, squre.size)
        #p.board_pos = squre.board_pos
        #squre.piece = p



    
    def on_start(self):
        #self.setup_board() # setup the grid let the user setup he board
        self.build_all_surfaces() # setup the surfaces for the grid


    def on_update(self, dt):
        """
            this function will be rendering everything
        """

        if not self.render_surface:
            return
        
        self.render_surface.fill(Setting.BACKGROUND_COLOR) # clear the board

        # loop through the squres
        for row in self.grid:
            for square in row:
                square.update() # update the displayed color through the transition

                if square.displayed_color:
                    square.render_surface.fill(square.displayed_color)
                else:
                    square.render_surface.fill(square.base_color)

                self.render_surface.blit(square.render_surface, square.pixel_pos) # build the squre surface and render them



        # render the pieces that are dead first so they are at the bottom
        for piece in self.dead_piece: # loop through the dead pieces and display them
            if not piece: # for redundency
                continue

            piece.update() # update the pos transition

            if piece.image_surface:
                self.render_surface.blit(pygame.transform.smoothscale(piece.image_surface.convert_alpha(), 
                                                                      (piece.pixle_size[0], piece.pixle_size[1])
                                                                      ), 
                                                                      piece.pixel_pos)


        # render the pieces in the squres 
        for row in self.grid: # loop through the pieces
            for square in row:
                if not square.piece:
                    continue

                if square.piece is self.selected_piece:
                    continue  # skip, we draw it later on top even if you remove this code 
                              # nothing will happen it it  will still look the same as the
                              # piece it drawn twice on the same pos but if you have alpha
                              # value this will lead to a problem

                square.piece.update() # update the pos transition

                square.piece.pixle_size = (square.size, square.size)
                if not square.piece.pixel_pos:
                    # if the piece doesnt have pixle pos then just make it the same
                    # as the squre this is the case when the piece  is first loaded
                    # or after releasing the piece from the cursor
                    square.piece.pixel_pos = square.pixel_pos

                if square.piece.image_surface:
                    self.render_surface.blit(pygame.transform.smoothscale(square.piece.image_surface.convert_alpha(), 
                                                                          (square.size, square.size)
                                                                          ), 
                                                                          square.piece.pixel_pos)
            
        # render the selected piece at the end so it is right at the top
        if self.selected_piece:
            piece = self.selected_piece
            piece.update() # update the pos transition

            if piece.image_surface:
                self.render_surface.blit(pygame.transform.smoothscale(piece.image_surface.convert_alpha(), 
                                                                      (piece.pixle_size[0], piece.pixle_size[1])
                                                                      ), 
                                                                      piece.pixel_pos)

        




        # render the board 
        window_surface = pygame.display.get_surface()
        self.render_rect = self.render_surface.get_rect(topleft=self.board_pos)
        window_surface.blit(self.render_surface, self.render_rect)


    def on_resize(self, event):
        for row in self.grid:
            for square in row:
                if not square.piece:
                    continue

                square.piece.pixel_pos = square.pixel_pos
                


    def build_all_surfaces(self):
        """
            this will build all the sufraces read for rendering
            it will build the main  grid surface  and build the
            squres on top of it 
        """

        
        board_size = min(Setting.WINDOW_WIDTH, Setting.WINDOW_HEIGHT)

        


        self.render_surface = pygame.Surface((board_size, board_size), pygame.SRCALPHA).convert_alpha()
        self.render_surface.fill(Setting.BACKGROUND_COLOR)

        
        square_size = board_size // Setting.BOARD_SQURE_WIDTH

        for row in self.grid:
            for square in row:
                square.size = square_size

                file, rank = square.board_pos  # (file, rank)
                square.pixel_pos = (
                    file * square_size,
                    rank * square_size,
                )
                square.render_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA).convert_alpha()
                if square.displayed_color:
                    square.render_surface.fill(square.displayed_color)
                else:
                    square.render_surface.fill(square.base_color)




    def on_window_resize(self, event):
        self.build_all_surfaces()

    

    def on_mouse_press(self, event):
        if not self.render_rect:
            return
        
        local_x, local_y = event.pos
        mouse_local = event.pos
        if self.render_rect.collidepoint(event.pos):
            local_x = event.pos[0] - self.render_rect.x
            local_y = event.pos[1] - self.render_rect.y
            mouse_local = (local_x, local_y)
        else:
            return

        if event.button == 1:
            self.left_press_pos = mouse_local
            # check if we clicked on a possible_move squre for the selected piece
            self.on_highlighted_square_interacted(mouse_local)
            self.on_click_piece(mouse_local)

        if event.button == 3:
            self.right_press_pos = mouse_local
            

                        


    def on_mouse_release(self, event):
        if not self.render_rect:
            return
        
        local_x, local_y = event.pos
        mouse_local = event.pos
        if self.render_rect.collidepoint(event.pos):
            local_x = event.pos[0] - self.render_rect.x
            local_y = event.pos[1] - self.render_rect.y
            mouse_local = (local_x, local_y)
        else:
            return
        

        if event.button == 1: # left click button
                # check if we rleased on a possible_move squre for the selected piece
                self.on_highlighted_square_interacted(mouse_local)

                # loop through pieces and stop draging the piece
                for row in self.grid:
                    for square in row:
                        if not square.piece:
                            continue
                        
                        if square.piece.is_draging: # ensure that we transition the piece only if it getting dragged
                            square.piece.transition_to_pos(square.pixel_pos) 
                            square.piece.is_draging = False
                            #square.piece.pixel_pos = None # reset the piece pos later on this will be a transition
        
        if event.button == 3:
            for row in self.grid: # loop through the squres and check if we right clicked on them
                for square in row:
                    if square.in_bounds(mouse_local) and square.in_bounds(self.right_press_pos):

                        self.hide_selected_piece_possible_moves()

                        if not square.is_highlighted:
                            square.transition_to_color(Setting.HIGHLIGHTED_SQUARE_COLOR)
                            square.is_highlighted = True
                        else:
                            square.transition_to_color(square.base_color)
                            square.is_highlighted = False


    def on_mouse_motion(self, event):
        if not self.render_rect:
            return
        
        local_x, local_y = event.pos
        mouse_local = event.pos
        if self.render_rect.collidepoint(event.pos):
            local_x = event.pos[0] - self.render_rect.x
            local_y = event.pos[1] - self.render_rect.y
            mouse_local = (local_x, local_y)
        else:
            return


        for row in self.grid:
            for square in row:
                if not square.piece:
                    continue
                
                if square.piece.is_draging:
                    x, y = mouse_local
                    new_top_left = (x - square.piece.pixle_size[0]/2, y - square.piece.pixle_size[1]/2)
                    
                    
                    #square.piece.transition_to_pos(new_top_left) # this will transition the piece to where the cursor is
                                                                    # this approch wont work when the  user wants to move a
                                                                    # piece this will be  triggered multiple times while he
                                                                    # is moving the piece it because it pauses the previous
                                                                    # tranistion it makes the pieces stay in one place dont
                                                                    # try to reimplement it it is a wast of time for now
                    
                    square.piece.pixel_pos = new_top_left
                    square.piece.pos_transition_animation.stop_transition()



    def on_click_piece(self, pos):
        """
            this function will detect when you click on a piece


            this function is triggered locally
        """


        _piece_got_pressed = False # will be used to check if we clicked on nother piece 

        # check if we clicked on a piece
        for row in self.grid:
            for square in row:
                if not square.piece:
                    continue

                if square.piece.in_bounds(pos):
                    square.piece.is_draging = True
                    x, y = pos
                    new_top_left = (x - square.piece.pixle_size[0]/2, y - square.piece.pixle_size[1]/2)
                    #square.piece.pixel_pos = new_top_left
                    square.piece.transition_to_pos(new_top_left)

                    self.selected_piece = square.piece
                    _piece_got_pressed = True

                    # we over ride the animation just in case
                    #square.piece.pos_transition_animation.stop_transition()
                    
        
        if not _piece_got_pressed:
            self.selected_piece = False

        self.reset_squares_colors()
        self.show_selected_piece_possible_moves()



    def reset_squares_colors(self):
        """
            this function is responsible for reset the colors of
            the squres to there base color
        """

        # this highlightes the squres for the possible moves, of the selected piece
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                square.transition_to_color(square.base_color)
                square.is_highlighted = False

    
    def show_selected_piece_possible_moves(self):
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                pos = (x, y)
                if self.selected_piece and pos in self.selected_piece.possible_moves:
                    square.transition_to_color(Setting.POSSIBLEMOVE_SQUARE_COLOR)
    
    def hide_selected_piece_possible_moves(self):
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                pos = (x, y)
                if self.selected_piece and pos in self.selected_piece.possible_moves:
                    square.transition_to_color(square.base_color)

        
    def on_highlighted_square_interacted(self, pos):
        """
            pose - is your cursor postion relative to the board

            this function will be excuated when you interact with the highlighted
            squre, either by pressing it or  draging a  piece on it this function
            doest check if the squre is highlighted but does check

            this function is triggered locally
        """

        if self.selected_piece:
            # we simply loop through the squres and check if the squre is a possible move 
            # for the selected piece that we interacted with 
            for row in self.grid:
                for square in row:
                    if square.in_bounds(pos): # we check if thats the squre we are on
                        if self.selected_piece and square.board_pos in self.selected_piece.possible_moves:
                            self.move_piece(self.selected_piece.board_pos, square.board_pos)
                            self.selected_piece = None

                            self.reset_squares_colors() # this updates the color incase of no interaction
        


    def move_piece(self, from_pos, to_pos): 
        """
            this takes a board pos that contain a piece and moves the
            piece from one first pos to the second pos
        """


        if not from_pos or not to_pos:
            return

        from_square = self.grid[from_pos[1]][from_pos[0]]

        if not from_square:
            return

        piece_to_move = from_square.piece
        if not piece_to_move:
            return

        self.grid[from_pos[1]][from_pos[0]].piece = None # remove the pieces refrence from the squre

        to_square = self.grid[to_pos[1]][to_pos[0]]

        if to_square.piece:
            self.dead_piece.append(to_square.piece)
            to_square.piece.hide() 
            pass

        to_square.piece = piece_to_move # append the piece to move

        piece_to_move.board_pos = to_square.board_pos
        
        
        # this next two lines need to be replaced by a transition effect
        #piece_to_move.pixle_size = to_square.pixel_pos
        #piece_to_move = None # this forces it to appear on the squre

        piece_to_move.transition_to_pos(to_square.pixel_pos)
