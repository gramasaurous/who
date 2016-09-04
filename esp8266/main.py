# connect a switch to an available GPIO pin
# connect an interrupt to that switch
# if we catch falling, and time until rising, then we can allocate different
# functions for different length presses
# but for the simple case we can just catch falling/rising and attach a simple
# toggle function to the interrupt