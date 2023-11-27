from queue import Queue
import time
import matplotlib.pyplot as plt
import numpy as np


class Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class EventHandler:
    def handle_event(self, event):
        pass


class Reactor:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, event_name, handler):
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    def remove_handler(self, event_name, handler):
        if event_name in self.handlers and handler in self.handlers[event_name]:
            self.handlers[event_name].remove(handler)

    def dispatch_event(self, event):
        event_name = event.name
        if event_name in self.handlers:
            for handler in self.handlers[event_name]:
                start_time = time.time()
                handler.handle_event(event)
                end_time = time.time()
                print(f"Handler {handler.__class__.__name__} took {end_time - start_time:.6f} seconds to execute.")


if __name__ == '__main__':
    reactor = Reactor()


    class Degree2GraphHandler(EventHandler):
        def handle_event(self, event):
            x = np.linspace(-10, 10, 400)
            y = x ** 2
            plt.plot(x, y, label="y = x^2")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Graph of y = x^2")
            plt.legend()
            plt.show()


    class Degree3GraphHandler(EventHandler):
        def handle_event(self, event):
            x = np.linspace(-10, 10, 400)
            y = x ** 3
            plt.plot(x, y, label="y = x^3")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Graph of y = x^3")
            plt.legend()
            plt.show()


    reactor.register_handler('Degree2', Degree2GraphHandler())
    reactor.register_handler('Degree3', Degree3GraphHandler())

    event1 = Event('Degree2', '')
    event2 = Event('Degree3', '')

    reactor.dispatch_event(event1)
    reactor.dispatch_event(event2)
