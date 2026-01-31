from .TickController import TickController



# this is a transition class its main perpose it to take a value 
# and move it from staring value to another end value this class
# is desinged to work with the TickController and how many times
# you want to update during transition is up to you to decide 


class Uniform:

    def __init__(self):
        self.tick_controller = TickController()

        self.starting_value = 0 # this is in millisecond
        self.ending_value = 1 # this is in millisecond
        self.duration = 1000 # this is in millisecond

        self.is_reversed = False

        # the function you provide will be feed the value that is in between
        # the starting value and the ending value depending on the proggress
        self.trigger_function:list[callable[float]] = []

    
    def update():
        """
            this function will be requreded to be running in your
            main  loop,  you  provide  the  loop  and the trigger
            functions will be excuated as a result
        """

        pass


    def start_tranition():
        pass

    def reverse_transition():
        pass













