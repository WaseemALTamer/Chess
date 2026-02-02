from .TickController import TickController



# this is a transition class its main perpose it to take a value 
# and move it from staring value to another end value this class
# is desinged to work with the TickController and how many times
# you want to update during transition is up to you to decide 


# this class is the base of any transition animation 


# the progress for the Uniform is liner
class Uniform:
    def __init__(self):
        self.tick_controller = TickController()

        self.starting_value:float = 0 # scaler
        self.ending_value:float = 1 # scaler
        self.duration:float = 1 # this is in seconds

        self.duration_time_stamp:float = 0 # this will track the progress of the time stamp
        self.current_value:float = 0

        self.is_reversed:bool = False
        self.is_running:bool = False

        # the function you provide will be feed the value that is in between
        # the starting value and the ending value depending on the proggress
        self.on_update_callbacks:list[callable[float]] = []

    
    def update(self):
        """
            this function will be requreded to be running in your
            main  loop,  you  provide  the  loop  and the trigger
            functions will be excuated as a  result this function
            will have its own dt time you dont need to provide it
        """

        if not self.is_running:
            return

        elapsed_time_seconds = self.tick_controller.get_elapsed() # this is in second
        

        if self.is_reversed:
            self.duration_time_stamp -= elapsed_time_seconds
        else:
            self.duration_time_stamp += elapsed_time_seconds

        if self.duration_time_stamp > self.duration:
            self.duration_time_stamp = self.duration
            self.current_value = self.ending_value
            self.is_running = False


        if self.duration_time_stamp < 0:
            self.duration_time_stamp = 0
            self.current_value = self.starting_value
            self.is_running = False

        
        self.current_value = ((self.duration_time_stamp / self.duration) * (self.ending_value - self.starting_value)) + self.starting_value

        for function in self.on_update_callbacks:
            return function(self.current_value)
    


    def start_tranition(self):
        """
            start tranistion from start_value to end_value 
        """


        self.is_reversed = False
        self.is_running = True

        # flaush the elips time
        self.tick_controller.get_elapsed()


    def reverse_transition(self):
        """
            start tranistion from end_value to start_value

            this made to start from the current value
        """


        self.is_reversed = True
        self.is_running = True

        # flaush the elips time
        self.tick_controller.get_elapsed()


    def stop_transition(self):
        self.is_running = False


    def reset_transition(self):
        self.duration_time_stamp = 0











