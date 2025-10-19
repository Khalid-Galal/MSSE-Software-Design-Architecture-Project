class Vehicle:
    """A base class representing a generic vehicle."""
    def __init__(self, regnum, make, model, color):
        self.regnum = regnum
        self.make = make
        self.model = model
        self.color = color

    def getMake(self):
        return self.make

    def getModel(self):
        return self.model

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regnum

class Car(Vehicle):
    """Represents a Car, inheriting from Vehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Car"

class Truck(Vehicle):
    """Represents a Truck, inheriting from Vehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Truck"

class Motorcycle(Vehicle):
    """Represents a Motorcycle, inheriting from Vehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Motorcycle"

class Bus(Vehicle):
    """Represents a Bus, inheriting from Vehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Bus"