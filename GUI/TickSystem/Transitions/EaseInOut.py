# this is a simple Trnsition script that lets you transition that lets
# you transition  with a  smooth speed  gain at  the start  and smooth
# loss of speed at the end


# this class is based on the Uniform Transition class 
from .Uniform import Uniform







class EaseInOut:
    def __init__(self):

        # set up the Uniform Trnsition 0-1
        self.uniform_transition = Uniform()
        self.uniform_transition.starting_value = 0
        self.uniform_transition.ending_value = 1
        self.uniform_transition.on_update_callbacks.append(self.on_uniform_update_callback) # we push the function to be excuated
                                                                                            # by the uniform tranition


        self.starting_value:float = 0
        self.ending_value:float = 1
        self.current_value:float = 0

        self.damping:float = 2

        self.on_update_callbacks:list[callable[float]] = [] # this we are going to control we dont wrap


    # we simply  just wrap  some of  the uniform transition
    # vairables that to do with the duriation and direction
    # we dont wrap the starint time or ending values
    @property
    def duration(self):
        return self.uniform_transition.duration
    
    @duration.setter
    def duration(self, value):
        self.uniform_transition.duration = value
    

    @property
    def duration_time_stamp(self):
        return self.uniform_transition.duration_time_stamp
    
    @duration_time_stamp.setter
    def duration_time_stamp(self, value):
        self.uniform_transition.duration_time_stamp = value


    @property
    def is_reversed(self):
        return self.uniform_transition.is_reversed
    
    @is_reversed.setter
    def is_reversed(self, value):
        self.uniform_transition.is_reversed = value


    @property
    def is_running(self):
        return self.uniform_transition.is_running
    
    @is_running.setter
    def is_running(self, value):
        self.uniform_transition.is_running = value



    # we also wrap the functions
    def start_tranition(self):
        self.uniform_transition.start_tranition() 

    def reverse_transition(self):
        self.uniform_transition.reverse_transition() 

    def stop_transition(self):
        self.uniform_transition.stop_transition()

    def reset_transition(self):
        self.uniform_transition.reset_transition()

    def update(self):
        self.uniform_transition.update()


    def on_uniform_update_callback(self, value:float):
        """
            this function will be ran through the uniform transition
            class, this will be called  back it will ease in_out the
            value and return it to you

            this uses two mathmatical function:
                y = 0.5 * ((2*value)**damping) { 0 <= x <= 0.5 }
                y = 1 - 0.5((2(1-value))**damping) { 0.5 <= x <= 1 }
        """
        eased_value = 0 # this value will still be between 0-1

        if value <= 0.5:
            eased_value = 0.5 * ((2*value)**(self.damping))
        else:
            eased_value = 1 - (0.5*((2*(1-value))**self.damping))
        
        self.current_value = ((self.ending_value - self.starting_value) * eased_value) + self.starting_value

        for function in self.on_update_callbacks:
            return function(self.current_value)

