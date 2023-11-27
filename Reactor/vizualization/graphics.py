import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

# Define the Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, x, y):
        pass

# Create a class representing the Reactor (Subject)
class Reactor:
    def __init__(self):
        self.observers = []
        self.x = []
        self.y = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, x, y):
        for observer in self.observers:
            observer.update(x, y)

    def add_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.notify_observers(x, y)

    def generate_plot(self):
        plt.plot(self.x, self.y, label='Default Color')  # Default color
        plt.xlabel('X-координата')
        plt.ylabel('Y-координата')
        plt.title('График данных из файла')
        plt.legend()  # Add a legend
        plt.show()

# Create an Observer class representing a data source
class DataSource(Observer):
    def __init__(self, reactor, filename, color):  # Specify a default color
        self.reactor = reactor
        self.filename = filename
        self.color = color  # Color for this data source

    def read_data_from_file(self):
        with open(self.filename, 'r') as file:
            for line in file:
                x, y = map(float, line.strip().split())
                self.reactor.add_data(x, y)

    def update(self, x, y):
        # This method is called when the reactor receives data from this source.
        pass  # You can implement specific behavior here if needed.

# Create an instance of the Reactor
reactor = Reactor()

# Create data sources and add them to the Reactor
data_source1 = DataSource(reactor, 'data1.txt', color='r')  # Specify a different color (red)
data_source2 = DataSource(reactor, 'data2.txt', color='b')  # Specify a different color (green)

reactor.add_observer(data_source1)
reactor.add_observer(data_source2)

# Read data from files and generate the plot
data_source1.read_data_from_file()
data_source2.read_data_from_file()
reactor.generate_plot()
