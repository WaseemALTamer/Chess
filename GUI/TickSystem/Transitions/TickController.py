# this file is desinged to be reusable in all sort of projects



import time


class TickController:
    def __init__(self, target_tps: int = 60):
        """
            target_tps - tps stands for tick per second and tick
        """
        self.target_tps = target_tps
        self.tick_interval  = 1.0 / self.target_tps # calculate 
        
        self.last_time = time.perf_counter() # this is more accurate than time.time()

        self._elapsed_last_time = self.last_time # used to calcuate eplised time for the get_elapsed function


        # this is used to calulate tps 
        self._tps = 0.0
        self._smoothing = 0.1  # lower = smoother


    def wait_for_tick(self) -> float:
        """
            this will simply wait until the next tick if you are
            ahead of  schedule then  this will  sleep if you are
            behind then this is not going to sleep 
        """


        target_dt = 1.0 / self.target_tps

        now = time.perf_counter()
        dt = now - self.last_time

        # Wait until we hit the target interval
        while dt < target_dt:
            remaining = target_dt - dt

            # Coarse sleep if we have enough time
            if remaining > 0.002:   # 2 ms safety margin
                time.sleep(remaining * 0.8) # sleep for the remaining 80% 
            else:
                pass

            now = time.perf_counter()
            dt = now - self.last_time

        self.last_time = now

        # Smoothed TPS
        instant_tps = 1.0 / dt if dt > 0 else 0.0
        self._tps += (instant_tps - self._tps) * self._smoothing

        return dt
    
    def get_elapsed(self) -> float:
        """
            Non-blocking elapsed time since last call.
            This RESETS the elapsed timer each time you call it.

            this function  is independent from the wait_for_tick
            so both can  run seperatly if you want to use either
            this doesnt block anything 
        """
        now = time.perf_counter()
        elapsed = now - self._elapsed_last_time
        self._elapsed_last_time = now
        return elapsed
    

    @property
    def tps(self) -> float:
        """
            this function require the wait_for_tick to be running
            so you can just measure the tps

            this returns the tick per second
        """


        return self._tps
