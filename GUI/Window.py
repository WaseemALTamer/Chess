# this class is simply responsible to make a window on screen and is responsible to kick start
# the update loop and map the events to pass them to other parts of the code that might attach
# to this file for the window everything will run on one thread


from Constants import *
from TickSystem import * 
from Setting import *
import pygame





class Window():
    # this class is made to be a single instance way 

    def __init__(self):
        # Initialize Pygame
        
        self.main_loop_state = False # true indecate it is running false indecate 
                                     # that it is not running
        
        pygame.init()
        pygame.display.set_caption(WINDOW_NAME)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        

        self.tick_controller = TickController(
                target_tps=WINDOW_FPS # you can change the target_tps on the run
            )
        


        # this is subscribe functions
        self.on_start:list[callable] = [] # excuate subscribed function on start

        self.on_update:list[callable[float]] = [] # excuate subscribed functions on each update per fps and
                                                  # they will be feed the delta time
        

        # subscripe function will need to have <function(Event)>
        # pramaters wise
        self.on_event_map:dict = {
            # this indecate of order of events
            


            WINDOW_RESIZE : [], 

            KEY_DOWN : [],
            KEY_UP : [],
            
            MOUSE_DOWN : [],
            MOUSE_UP : [],
            MOUSE_MOTION : [],
            MOUSE_WHEEL : [],
            
        }











    def update(self):

        """
            this  function is made to run once you should not rerun it
            this function  will run when  you  ready  but  it  is  not
            it is adviced if you terminate this function you reintiate
            the Window class so you can remove the event 
        """
        
        for function in self.on_start:
            function()
        
        self.main_loop_state = True
        while self.main_loop_state:

            
            delta_time = self.tick_controller.wait_for_tick()

            

            # excuate the
            for event in pygame.event.get():


                # Window
                if event.type == pygame.QUIT: # we dont expose the quite event
                    self.main_loop_state = False # we dont quite let the code flush until we hit quit natrually

                elif event.type == pygame.WINDOWSIZECHANGED:
                    for function in self.on_event_map[WINDOW_RESIZE]:
                        function(event)

                # Keyboard
                elif event.type == pygame.KEYDOWN:
                    for function in self.on_event_map[KEY_DOWN]:
                        function(event)

                elif event.type == pygame.KEYUP:
                    for function in self.on_event_map[KEY_UP]:
                        function(event)

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for function in self.on_event_map[MOUSE_DOWN]:
                        function(event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    for function in self.on_event_map[MOUSE_UP]:
                        function(event)

                elif event.type == pygame.MOUSEMOTION:
                    for function in self.on_event_map[MOUSE_MOTION]:
                        function(event)

                elif event.type == pygame.MOUSEWHEEL:
                    for function in self.on_event_map[MOUSE_WHEEL]:
                        function(event)




            # excuate all the on update functions
            for function in self.on_update:
                function(delta_time)

            pygame.display.update()


        self.main_loop_state = False
        pygame.quit()



        