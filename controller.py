import model
import view
import time

class Controller:
    def __init__(self):
        self.model = model.Model(self)
        self.view = view.View(self)
        self.framerate = 30
        self.last_update = time.time()

        # update loop
        while True:

            # checking framerate
            curr_time = time.time()
            dt = curr_time - self.last_update
            if dt > 1 / self.framerate:

                # updating
                self.last_update = curr_time
                self.update(dt)

    def update(self, dt):
        self.view.update()

# starting
Controller()