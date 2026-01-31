import Constants
import Setting 
import pygame
import Assets


class Piece:
    def __init__(self):

        self.piece_type:str = None


        self.image_surface = None
        self.possible_moves:list[tuple] = [(1, 2),(3, 4)]

        self.is_draging:list = False # this will indecate if the piece is being dragged 

        self.board_pos: tuple[float, float] = None   # (file, rank) grid coordinates
        self.pixel_pos: tuple[float, float] = None   # (x, y) relative to board origin
        self.pixle_size: tuple[float, float] = None


    def in_bounds(self, pos):
        """
            Check if the given pos (x, y) is over the piece.
            pos: tuple (x, y) relative to the window
            Returns True if the point is inside the piece's rect.
        """
        if not self.pixel_pos or not self.pixle_size:
            return False

        x, y = pos
        px, py = self.pixel_pos
        w, h = self.pixle_size

        if px <= x <= px + w and py <= y <= py + h:
            return True
        return False
        





class Square:
    def __init__(self):
        self.base_color:tuple = (0, 0, 0, 0) # used as the base squre color
        self.displayed_color:tuple|None = None # will be used to make the squre a different color temperarly

        self.size:float = 0 


        self.board_pos: tuple[float, float]  = (0, 0) # (file, rank) grid coordinates

        self.pixel_pos: tuple[float, float] = (0, 0)    # (x, y) relative to  board origin, this is what 
                                                        # is used to display the piece on the board

        self.algebraic_notation:str = ""

        self.piece:Piece|None = None  # piece that it holds they are not drawn in the squre boundries but board

        self.render_surface:pygame.Surface = None

    



    def in_bounds(self, pos):
        """
            Check if the given pos (x, y) is over the piece.
            pos: tuple (x, y) relative to the window
            Returns True if the point is inside the piece's rect.
        """
        if not self.pixel_pos or not self.size:
            return False

        x, y = pos
        px, py = self.pixel_pos
        w, h = self.size, self.size

        if px <= x <= px + w and py <= y <= py + h:
            return True
        return False




class Board:
    def __init__(self):
        self.grid:list[list[Square]] = []
        self.render_surface:pygame.Surface = None
        self.render_rect:pygame.Rect = None
        self.board_pos = (0, 0)

        self.selected_piece:Piece = None


        # this is call back section attach functions and this will run them for you
        self.on_piece_move_callbacks:list[callable] = []



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
        squre = self.grid[3][3]

        p = Piece()
        p.image_surface = Assets.Images.ghost_pawn_surface
        p.pixle_size = (squre.size, squre.size)
        p.board_pos = squre.board_pos
        squre.piece = p



    
    def on_start(self):
        self.setup_board() # setup the grid
        self.build_all_surfaces() # setup the surfaces for the grid


    def on_update(self, dt):
        """
            this function will be rendering everything
        """

        if not self.render_surface:
            return
        
        # render the squares
        for row in self.grid:
            for square in row:
                if square.displayed_color:
                    square.render_surface.fill(square.displayed_color)
                else:
                    square.render_surface.fill(square.base_color)

                self.render_surface.blit(square.render_surface, square.pixel_pos) # build the squre surface

        # render the pieces in the squres we use another for loop
        # so the pieces are on top of all the squres
        for row in self.grid:
            for square in row:
                if not square.piece:
                    continue
                
                square.piece.pixle_size = (square.size, square.size)
                if not square.piece.pixel_pos: 
                    # if the piece doesnt have pixle pos then just make it the same
                    # as the squre this is the case when the piece  is first loaded
                    # or after releasing the piece from the cursor
                    square.piece.pixel_pos = square.pixel_pos

                
                self.render_surface.blit(pygame.transform.smoothscale(square.piece.image_surface, (square.size, square.size)), square.piece.pixel_pos)


        # render the board 
        window_surface = pygame.display.get_surface()
        self.surface_rect = self.render_surface.get_rect(topleft=self.board_pos)
        window_surface.blit(self.render_surface, self.surface_rect)


    def build_all_surfaces(self):
        """
            this will build all the sufraces read for rendering
            it will build the main  grid surface  and build the
            squres on top of it 
        """

        
        board_size = min(Setting.WINDOW_WIDTH, Setting.WINDOW_HEIGHT)

        


        self.render_surface = pygame.Surface((board_size, board_size))
        self.render_surface.fill(Setting.WHITE_SQUARE_COLOR)

        
        square_size = board_size / Setting.BOARD_SQURE_WIDTH

        for row in self.grid:
            for square in row:
                square.size = square_size

                file, rank = square.board_pos  # (file, rank)
                square.pixel_pos = (
                    file * square_size,
                    rank * square_size,
                )
                square.render_surface = pygame.Surface((square_size, square_size))
                if square.displayed_color:
                    square.render_surface.fill(square.displayed_color)
                else:
                    square.render_surface.fill(square.base_color)




    def on_window_resize(self, event):
        self.build_all_surfaces()

    

    def on_mouse_press(self, event):
        if event.button == 1:

            # check if we clicked on a possible_move squre for the selected piece
            if self.surface_rect.collidepoint(event.pos):
                local_x = event.pos[0] - self.surface_rect.x
                local_y = event.pos[1] - self.surface_rect.y
                mouse_local = (local_x, local_y)

                self.on_highlighted_square_interacted(mouse_local)
                self.on_click_piece(mouse_local)
            

                        


    def on_mouse_release(self, event):
        if event.button == 1:

            if self.surface_rect.collidepoint(event.pos):
                local_x = event.pos[0] - self.surface_rect.x
                local_y = event.pos[1] - self.surface_rect.y
                mouse_local = (local_x, local_y)

                # check if we rleased on a possible_move squre for the selected piece
                self.on_highlighted_square_interacted(mouse_local)

                # loop through pieces and stop draging the piece
                for row in self.grid:
                    for square in row:
                        if not square.piece:
                            continue

                        square.piece.is_draging = False
                        square.piece.pixel_pos = None # reset the piece pos later on this will be a transition



    def on_mouse_motion(self, event):
        if self.surface_rect.collidepoint(event.pos):
            local_x = event.pos[0] - self.surface_rect.x
            local_y = event.pos[1] - self.surface_rect.y
            mouse_local = (local_x, local_y)

            for row in self.grid:
                for square in row:
                    if not square.piece:
                        continue
                    
                    if square.piece.is_draging:
                        x, y = mouse_local
                        new_top_left = (x - square.piece.pixle_size[0]/2, y - square.piece.pixle_size[1]/2)
                        square.piece.pixel_pos = new_top_left



    def update_squares_colors(self):
        """
            this function is responsible for changing the colors
        """



        # this highlightes the squres for the possible moves, of the selected piece
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                pos = (x, y)

                if self.selected_piece and pos in self.selected_piece.possible_moves:
                    square.displayed_color = Setting.HIGHLIGHTED_SQUARE_COLOR
                else:
                    square.displayed_color = None


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
                    square.piece.pixel_pos = new_top_left

                    self.selected_piece = square.piece
                    _piece_got_pressed = True
                    
        
        if not _piece_got_pressed:
            self.selected_piece = False

        self.update_squares_colors()


        
    def on_highlighted_square_interacted(self, pos):
        """
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
                    if square.in_bounds(pos):
                        if square.board_pos in self.selected_piece.possible_moves:
                            x, y = self.selected_piece.board_pos

                            # transfere the selected piece
                            self.grid[y][x].piece = None
                            square.piece = self.selected_piece
                            square.piece.pixel_pos = None # this needs to be changed a transition

                            self.selected_piece.board_pos = square.board_pos
                            self.selected_piece.pixle_size = square.pixel_pos
                            self.selected_piece = None


        self.update_squares_colors()

    

        

    
        
    




    