from models import Vehicle

class VehicleFactory:
    """
    A factory class for creating vehicle objects.
    This encapsulates the logic for vehicle instantiation.
    """
    @staticmethod
    def create_vehicle(vehicle_type, regnum, make, model, color, is_electric):
        """
        Creates a vehicle object of a specific type.
        
        Args:
            vehicle_type (str): The type of vehicle to create (e.g., 'car', 'motorcycle').
            ... other vehicle attributes ...
        
        Returns:
            An instance of a Vehicle subclass.
        """
        if vehicle_type.lower() == 'motorcycle':
            return Vehicle.Motorcycle(regnum, make, model, color, is_electric)
        elif vehicle_type.lower() == 'car':
            return Vehicle.Car(regnum, make, model, color, is_electric)
        else:
            return Vehicle.Car(regnum, make, model, color, is_electric)