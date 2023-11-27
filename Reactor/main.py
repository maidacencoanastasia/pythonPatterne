from queue import Queue
import time
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify


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


    class GraphHandler(EventHandler):
        def handle_event(self, event):
            equation = input("Enter an equation in terms of x: ")
            try:
                x = symbols('x')
                expression = sympify(equation)
                func = lambdify(x, expression, 'numpy')
                x_vals = np.linspace(-10, 10, 400)
                y_vals = func(x_vals)
                plt.plot(x_vals, y_vals, label=f"y = {equation}")
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title(f"Graph of y = {equation}")
                plt.legend()
                plt.show()
            except Exception as e:
                print("Invalid equation. Please enter a valid equation.")


    reactor.register_handler('Graph', GraphHandler())

    event = Event('Graph', '')

    reactor.dispatch_event(event)
