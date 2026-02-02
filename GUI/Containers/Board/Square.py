# this is independent file




from TickSystem.Transitions.EaseInOut import EaseInOut
import Setting






class Square:
    def __init__(self):
        self.base_color:tuple = (0, 0, 0, 0) # used as the base squre color
        self.displayed_color:tuple|None = None # will be used to make the squre a different color temperarly

        self.size:float = 0 


        self.board_pos:tuple[float, float]  = (0, 0) # (file, rank) grid coordinates

        self.pixel_pos:tuple[float, float] = (0, 0)    # (x, y) relative to  board origin, this is what 
                                                        # is used to display the piece on the board


        self.is_highlighted = False # this well tell us if the user highlighted the square

        self.algebraic_notation:str = ""

        self.piece = None  # piece that it holds they are not drawn in the squre boundries but board
                           # the date type is up to  you to  decide, but  check the  Piece class for
                           # what will be inside this var

        self.render_surface = None # this will contain a pygame surface


        self.color_transition_animation = EaseInOut()
        self.color_transition_animation.duration = Setting.TRANSITION_TIME
        self.color_transition_animation.on_update_callbacks.append(self.animation_trigger)


        self._transition_color_from = None
        self._transition_color_to = None



    def transition_to_color(self, color:tuple[float, float, float, float]):
        
        if color == self.displayed_color:
            return

        self._transition_color_to = color

        self._transition_color_from = self.base_color
        if self.displayed_color:
            self._transition_color_from = self.displayed_color
            

        self.color_transition_animation.reset_transition()
        self.color_transition_animation.start_tranition()



    def animation_trigger(self, value:float):
        if not self._transition_color_to:
            return
        
        # Clamp value just to be safe
        if value < 0:
            value = 0
        elif value > 1:
            value = 1

        r1, g1, b1, a1 = self._transition_color_from
        r2, g2, b2, a2 = self._transition_color_to

        r = int(r1 + (r2 - r1) * value)
        g = int(g1 + (g2 - g1) * value)
        b = int(b1 + (b2 - b1) * value)
        a = int(a1 + (a2 - a1) * value) # this is not used for now

        self.displayed_color = (r, g, b, a1) # we keep the alpha the same


    
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

        if px < x < px + w and py < y < py + h:
            return True
        return False
    

    def update(self):
        """
            this function needs to be ran every frames
        """

        if self.color_transition_animation:
            self.color_transition_animation.update()