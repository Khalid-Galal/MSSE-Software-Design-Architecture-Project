class Vehicle:
    """A base class representing a generic vehicle."""
    def __init__(self, regnum, make, model, color, is_electric=False):
        self.regnum = regnum
        self.make = make
        self.model = model
        self.color = color
        self.is_electric = is_electric
        self.charge = 100 if is_electric else None

    def get_type(self):
        """Returns the type of the vehicle."""
        return "Vehicle"

class Car(Vehicle):
    """Represents a Car, inheriting from Vehicle."""
    def get_type(self):
        return "Car"

class Truck(Vehicle):
    """Represents a Truck, inheriting from Vehicle."""
    def get_type(self):
        return "Truck"

class Motorcycle(Vehicle):
    """Represents a Motorcycle, inheriting from Vehicle."""
    def get_type(self):
        return "Motorcycle"

class Bus(Vehicle):
    """Represents a Bus, inheriting from Vehicle."""
    def get_type(self):
        return "Bus"