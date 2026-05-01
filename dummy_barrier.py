from time import time

# Acest cod este folosit pentru a testa programul cand nu exista o bariera. Nu este folosit de program.
class Barrier(object):

    def __init__(self):
        # False - Closed
        # True - Open
        self.barrier_status = False
        self.timer_open = None
        self.time_to_wait = 7
    
    def command(self, command, time=None):
        match command:
            case 1:
                return self.get_barrier_status()
            case 2:
                return self.open_barrier()
            case 3:
                return self.close_barrier()
            case 4:
                return self.set_time(time)

    def get_barrier_status(self):
        return f"1 {int(self.barrier_status)}"
    
    def open_barrier(self):
        if self.barrier_status == True:
            return "2 0"
        else:
            self.barrier_status = True
            self.timer_open = time()
            print("BARRIER OPEN!!!")
            return "2 1"
    
    def close_barrier(self):
        time_close = time()
        if self.barrier_status and time_close - self.timer_open > self.time_to_wait:
            self.barrier_status = False
            self.timer_open = None
            print("BARRIER CLOSED!!!")
            return "3 1"
        else:
            return "3 0"
    
    def set_time(self, time):
        self.time_to_wait = time
        print(f"Time set to {time} seconds")

barrier = Barrier()

def get_barrier_status():
    result = barrier.command(1)
    if result == "1 1":
        return True
    elif result == "1 0":
        return False

def open_barrier():
    result = barrier.command(2)
    if result == "2 1":
        return True
    elif result == "2 0":
        return False

def close_barrier():
    result = barrier.command(3)
    if result == "3 1":
        return True
    elif result == "3 0":
        return False

def set_time(time):
    barrier.command(4, time)