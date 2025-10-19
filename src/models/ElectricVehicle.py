class ElectricVehicle:
    """A base class representing a generic electric vehicle."""
    def __init__(self, regnum, make, model, color):
        self.regnum = regnum
        self.make = make
        self.model = model
        self.color = color
        self.charge = 0

    def getMake(self):
        return self.make

    def getModel(self):
        return self.model

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regnum

    def setCharge(self, charge):
        self.charge = charge

    def getCharge(self):
        return self.charge

class ElectricCar(ElectricVehicle):
    """Represents an Electric Car, inheriting from ElectricVehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Car"

class ElectricBike(ElectricVehicle):
    """Represents an Electric Bike, inheriting from ElectricVehicle."""
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Motorcycle"