from vehicle_factory import VehicleFactory

class ParkingLot:
    """
    Manages the state and operations of a single parking lot level.
    This class is decoupled from any UI framework and vehicle creation logic.
    """
    def __init__(self):
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.slots = []
        self.evSlots = []
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self.factory = VehicleFactory()

    def create_parking_lot(self, capacity, ev_capacity, level):
        """Initializes or resets the parking lot with a given capacity."""
        self.capacity = capacity
        self.evCapacity = ev_capacity
        self.level = level
        self.slots = [None] * capacity
        self.evSlots = [None] * ev_capacity
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        return f'Created a parking lot with {capacity} regular slots and {ev_capacity} ev slots on level: {level}\n'

    def _get_empty_slot(self):
        """Finds the first available regular parking slot."""
        for i, slot in enumerate(self.slots):
            if slot is None:
                return i
        return -1

    def _get_empty_ev_slot(self):
        """Finds the first available EV parking slot."""
        for i, slot in enumerate(self.evSlots):
            if slot is None:
                return i
        return -1

    def park(self, vehicle_type, regnum, make, model, color, is_electric):
        """Parks a vehicle created by the factory in an appropriate slot."""
        vehicle = self.factory.create_vehicle(vehicle_type, regnum, make, model, color, is_electric)
        if vehicle is None:
            return "ERROR: Vehicle creation failed. Check the vehicle type.\n"
        if vehicle.is_electric:
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slot_id = self._get_empty_ev_slot()
                self.evSlots[slot_id] = vehicle
                self.numOfOccupiedEvSlots += 1
                return f'Allocated EV slot number: {slot_id + 1}\n'
            else:
                return "Sorry, EV parking lot is full\n"
        else:
            if self.numOfOccupiedSlots < self.capacity:
                slot_id = self._get_empty_slot()
                self.slots[slot_id] = vehicle
                self.numOfOccupiedSlots += 1
                return f'Allocated slot number: {slot_id + 1}\n'
            else:
                return "Sorry, parking lot is full\n"

    def leave(self, slot_id, is_electric):
        """Removes a vehicle from the specified slot."""
        slot_index = slot_id - 1
        if is_electric:
            if 0 <= slot_index < self.evCapacity and self.evSlots[slot_index] is not None:
                self.evSlots[slot_index] = None
                self.numOfOccupiedEvSlots -= 1
                return f'Slot number {slot_id} is free\n'
            else:
                return f"Unable to remove car from EV slot: {slot_id}\n"
        else:
            if 0 <= slot_index < self.capacity and self.slots[slot_index] is not None:
                self.slots[slot_index] = None
                self.numOfOccupiedSlots -= 1
                return f'Slot number {slot_id} is free\n'
            else:
                return f"Unable to remove car from slot: {slot_id}\n"

    def get_status(self):
        """Returns a string detailing the status of all occupied slots."""
        status_report = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, vehicle in enumerate(self.slots):
            if vehicle is not None:
                status_report += f"{i+1}\t{self.level}\t{vehicle.regnum}\t\t{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}\n"
        
        status_report += "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, vehicle in enumerate(self.evSlots):
            if vehicle is not None:
                status_report += f"{i+1}\t{self.level}\t{vehicle.regnum}\t\t{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}\n"
        return status_report

    def get_charge_status(self):
        """Returns a string detailing the charge status of all EV vehicles."""
        charge_report = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        for i, vehicle in enumerate(self.evSlots):
            if vehicle is not None:
                charge_report += f"{i+1}\t{self.level}\t{vehicle.regnum}\t\t{vehicle.charge}\n"
        return charge_report

    def _find_vehicles(self, condition):
        """
        A generic search method that finds vehicles based on a condition.
        
        Args:
            condition (callable): A function that takes a vehicle and returns True for a match.
            
        Yields:
            A tuple of (vehicle, slot_id, is_electric).
        """
        for i, vehicle in enumerate(self.slots):
            if vehicle is not None and condition(vehicle):
                yield (vehicle, i + 1, False)
        for i, vehicle in enumerate(self.evSlots):
            if vehicle is not None and condition(vehicle):
                yield (vehicle, i + 1, True)

    def find_reg_nums_by_color(self, color):
        """Returns registration numbers for vehicles of a specific color."""
        condition = lambda v: v.color.lower() == color.lower()
        found_vehicles = list(self._find_vehicles(condition))
        
        reg_nums = [v.regnum for v, _, is_electric in found_vehicles if not is_electric]
        ev_reg_nums = [v.regnum for v, _, is_electric in found_vehicles if is_electric]

        result = ""
        if reg_nums:
            result += "Registration Numbers: " + ', '.join(reg_nums) + "\n"
        if ev_reg_nums:
            result += "Registration Numbers (EV): " + ', '.join(ev_reg_nums) + "\n"
        return result if result else f"No vehicles found with color: {color}\n"

    def find_slot_nums_by_color(self, color):
        """Returns slot numbers for vehicles of a specific color."""
        condition = lambda v: v.color.lower() == color.lower()
        found_vehicles = list(self._find_vehicles(condition))
        
        slot_nums = [str(slot_id) for _, slot_id, is_electric in found_vehicles if not is_electric]
        ev_slot_nums = [str(slot_id) for _, slot_id, is_electric in found_vehicles if is_electric]

        result = ""
        if slot_nums:
            result += "Identified slots: " + ', '.join(slot_nums) + "\n"
        if ev_slot_nums:
            result += "Identified slots (EV): " + ', '.join(ev_slot_nums) + "\n"
        return result if result else f"No slots found for color: {color}\n"

    def find_slot_num_by_reg(self, regnum):
        """Returns the slot number for a specific registration number."""
        condition = lambda v: v.regnum.lower() == regnum.lower()
        # Find the first match, if any
        try:
            _, slot_id, is_electric = next(self._find_vehicles(condition))
            slot_type = "(EV)" if is_electric else ""
            return f"Identified slot {slot_type}: {slot_id}\n"
        except StopIteration:
            return "Not found\n"