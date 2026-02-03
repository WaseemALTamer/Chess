# this file is independent



from GUI.TickSystem.Transitions.EaseInOut import EaseInOut
import GUI.Setting as Setting



class Piece:
    def __init__(self):
        self.piece_type:str = None


        self.image_surface = None # this will contain a pygame surface the user decide
                                  # the surface make sure that <set_alpha(value)> is a 
                                  # function

        self.possible_moves:list[tuple] = []

        self.is_draging:list = False # this will indecate if the piece is being dragged 

        self.board_pos:tuple[float, float] = None   # (file, rank) grid coordinates
        self.pixel_pos:tuple[float, float] = None   # (x, y) relative to board origin
        self.pixle_size:tuple[float, float] = None

        self.pos_transition_animation = EaseInOut()
        self.pos_transition_animation.duration = Setting.TRANSITION_TIME
        self.pos_transition_animation.on_update_callbacks.append(self.pos_animation_trigger)


        self.alpha_transition_animation = EaseInOut() # this is used to hide or show the piece it self
        self.alpha_transition_animation.duration = Setting.TRANSITION_TIME
        self.alpha_transition_animation.starting_value = 255 # full transirancy thats where the piece is going to start at
        self.alpha_transition_animation.ending_value = 0 # we are going to end at 0 for hiding the piece
        self.alpha_transition_animation.on_update_callbacks.append(self.set_opacity)


        # these are for transition animation
        self._transition_point_from = None
        self._transition_pos_to = None



    def transition_to_pos(self, pos:tuple[float, float]):
        if not pos:
            return
        
        self._transition_point_from = self.pixel_pos
        self._transition_pos_to = pos

        self.pos_transition_animation.reset_transition()
        self.pos_transition_animation.start_tranition()




    def pos_animation_trigger(self, value:float):

        start_x, start_y = self._transition_point_from
        end_x, end_y = self._transition_pos_to

        x = int(start_x + (end_x - start_x) * value)
        y = int(start_y + (end_y - start_y) * value)

        self.pixel_pos = (x, y)


    def show(self): # this will show the piece
        if self.alpha_transition_animation:
            self.alpha_transition_animation.reverse_transition() # transition back to 255


    def hide(self): # this will hide the piece
        if self.alpha_transition_animation:
            self.alpha_transition_animation.start_tranition() # transition to 0


    def set_opacity(self, value:float):
        """
            this will set the apha value of the piece it self
            the value should range from 0-255
        """

        if self.image_surface:
            self.image_surface.set_alpha(value)



    def in_bounds(self, pos:float):
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

        if px < x < px + w and py < y < py + h:
            return True
        return False
    

    def update(self):
        """
            this function needs to be ran every frames
        """

        if self.pos_transition_animation:
            self.pos_transition_animation.update()
        
        if self.alpha_transition_animation:
            self.alpha_transition_animation.update()

    
    

