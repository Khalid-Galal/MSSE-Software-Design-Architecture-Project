import tkinter as tk
from models import Vehicle, ElectricVehicle

# --- Global Tkinter Variables ---
# Note: Using global variables like this is an anti-pattern we will address later.
root = tk.Tk()
root.geometry("650x850")
root.resizable(0,0)
root.title("Parking Lot Manager")

# Input values from the UI, now with more descriptive names
reg_slots_var = tk.StringVar()
ev_slots_var = tk.StringVar()
level_var = tk.StringVar()

make_var = tk.StringVar()
model_var = tk.StringVar()
color_var = tk.StringVar()
reg_var = tk.StringVar()
is_electric_var = tk.IntVar()
is_motorcycle_var = tk.IntVar()

remove_slot_var = tk.StringVar()
remove_is_electric_var = tk.IntVar()

find_slot_by_reg_var = tk.StringVar()
find_slot_by_color_var = tk.StringVar()
find_reg_by_color_var = tk.StringVar()
    
tfield = tk.Text(root, width=70, height=15)
    
class ParkingLot:
    """
    Manages the state and operations of a single parking lot level,
    including parking, leaving, and querying vehicle information.
    """
    def __init__(self):
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.slotid= 0
        self.slotEvId = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0

    def createParkingLot(self,capacity,evcapacity,level):
        """Initializes or resets the parking lot with a given capacity."""
        self.slots = [-1] * capacity
        self.evSlots = [-1] * evcapacity
        self.level = level
        self.capacity = capacity
        self.evCapacity = evcapacity
        return self.level

    def getEmptySlot(self):
        """Finds the first available regular parking slot."""
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i
        return -1 # Should not happen if capacity is checked first

    def getEmptyEvSlot(self):
        """Finds the first available EV parking slot."""
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                return i
        return -1 # Should not happen if capacity is checked first

    def park(self,regnum,make,model,color,ev,motor):
        """Parks a vehicle in an appropriate slot."""
        if (self.numOfOccupiedEvSlots < self.evCapacity or self.numOfOccupiedSlots < self.capacity):
            slotid = -1
            if (ev == 1):
                if self.numOfOccupiedEvSlots < self.evCapacity:
                    slotid = self.getEmptyEvSlot()
                    if (motor == 1):
                        self.evSlots[slotid] = ElectricVehicle.ElectricBike(regnum,make,model,color)
                    else:
                        self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum,make,model,color)
                    self.slotEvId = self.slotEvId+1
                    self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots + 1
                    slotid = self.slotEvId
            else:
                if self.numOfOccupiedSlots < self.capacity:
                    slotid = self.getEmptySlot()
                    if (motor == 1):
                        self.slots[slotid] = Vehicle.Motorcycle(regnum,make,model,color)
                    else:
                        self.slots[slotid] = Vehicle.Car(regnum,make,model,color)
                    self.slotid = self.slotid+1
                    self.numOfOccupiedSlots = self.numOfOccupiedSlots + 1
                    slotid = self.slotid    
            return slotid
        else:
            return -1

    def leave(self,slotid,ev):
        """Removes a vehicle from the specified slot."""
        if (ev == 1):
            if self.numOfOccupiedEvSlots > 0 and self.evSlots[slotid-1] != -1:
                self.evSlots[slotid-1] = -1
                self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots - 1
                return True
            else:
                return False
        else:
            if self.numOfOccupiedSlots > 0 and self.slots[slotid-1] != -1:
                self.slots[slotid-1] = -1
                self.numOfOccupiedSlots = self.numOfOccupiedSlots - 1
                return True
            else:
                return False

    def edit(self,slotid,regnum,make,model,color,ev):
        """Edits the details of a vehicle in a given slot."""
        if (ev == 1):
            self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum,make,model,color)
            return True
        else:
            self.slots[slotid] = Vehicle.Car(regnum,make,model,color)
            return True
            
        return False     

    def status(self):
        """Displays the status of all occupied slots in the text field."""
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.slots)):
            if self.slots[i] != -1:
                output = str(i+1) + "\t" +str(self.level) + "\t" + str(self.slots[i].regnum) + "\t\t" + str(self.slots[i].color) + "\t\t" +str(self.slots[i].make) +"\t\t" +str(self.slots[i].model) +"\n"                    
                tfield.insert(tk.INSERT, output)
            else:
                continue
            
        output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                output = str(i+1) + "\t" +str(self.level) + "\t" + str(self.evSlots[i].regnum) + "\t\t" + str(self.evSlots[i].color) + "\t\t" +str(self.evSlots[i].make) +"\t\t" +str(self.evSlots[i].model) +"\n"                    
                tfield.insert(tk.INSERT, output)
            else:
                continue

    def chargeStatus(self):
        """Displays the charge status of all EV vehicles."""
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        tfield.insert(tk.INSERT, output)
        
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                output = str(i+1) + "\t" +str(self.level) + "\t" + str(self.evSlots[i].regnum) + "\t\t" + str(self.evSlots[i].charge) +"\n"                    
                tfield.insert(tk.INSERT, output)
            else:
                continue

    def getRegNumFromColor(self,color):
        """Returns a list of registration numbers for a given color (non-EV)."""
        regnums = []
        for i in self.slots:
            if i == -1:
                continue
            if i.color == color:
                regnums.append(i.regnum)
        return regnums
            
    def getSlotNumFromRegNum(self,regnum):
        """Returns the slot number for a given registration number (non-EV)."""
        for i in range(len(self.slots)):
            if (self.slots[i] != -1):
                if self.slots[i].regnum == regnum:
                    return i+1
                else:
                    continue
        return -1
            
    def getSlotNumFromColor(self,color):
        """Returns a list of slot numbers for a given color (non-EV).""" 
        slotnums = []
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].color == color:
                slotnums.append(str(i+1))
        return slotnums

    def getRegNumFromColorEv(self,color):
        """Returns a list of registration numbers for a given color (EV)."""
        regnums = []
        for i in self.evSlots:
            if i == -1:
                continue
            if i.color == color:
                regnums.append(i.regnum)
        return regnums
            
    def getSlotNumFromRegNumEv(self,regnum):
        """Returns the slot number for a given registration number (EV)."""
        for i in range(len(self.evSlots)):
            if (self.evSlots[i] != -1):
                if str(self.evSlots[i].regnum) == str(regnum):
                    return i+1
                else:
                    continue
        return -1
            
    def getSlotNumFromColorEv(self,color):
        """Returns a list of slot numbers for a given color (EV).""" 
        slotnums = []
        for i in range(len(self.evSlots)):          
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].color == color:
                slotnums.append(str(i+1))
        return slotnums

    # --- UI-bound Methods ---
    # These methods are directly called by the Tkinter buttons.
    # This tight coupling is an anti-pattern we will refactor later.
    def slotNumByReg(self):
        """Handler for 'Get Slot ID by Registration #' button."""
        slot_val = find_slot_by_reg_var.get()
        slotnum = self.getSlotNumFromRegNum(slot_val)
        slotnum2 = self.getSlotNumFromRegNumEv(slot_val)
        output = ""
        if slotnum >= 0:
            output = "Identified slot: " + str(slotnum) + "\n"
        elif slotnum2 >= 0:
            output = "Identified slot (EV): " + str(slotnum2) + "\n"
        else:
            output = "Not found\n"
        tfield.insert(tk.INSERT, output)

    def slotNumByColor(self):
        """Handler for 'Get Slot ID by Color' button."""
        slotnums = self.getSlotNumFromColor(find_slot_by_color_var.get())
        slotnums2 = self.getSlotNumFromColorEv(find_slot_by_color_var.get())
        output = "Identified slots: " + ', '.join(slotnums) + "\n"
        tfield.insert(tk.INSERT, output)
        output = "Identified slots (EV): " + ', '.join(slotnums2) + "\n"
        tfield.insert(tk.INSERT, output)

    def regNumByColor(self):
        """Handler for 'Get Registration # by Color' button."""
        regnums = self.getRegNumFromColor(find_reg_by_color_var.get())
        regnums2 = self.getRegNumFromColorEv(find_reg_by_color_var.get())
        output = "Registation Numbers: "+', '.join(regnums) + "\n"        
        tfield.insert(tk.INSERT, output)
        output = "Registation Numbers (EV): "+', '.join(regnums2) + "\n"        
        tfield.insert(tk.INSERT, output)

    def makeLot(self):
        """Handler for 'Create Parking Lot' button."""
        self.createParkingLot(int(reg_slots_var.get()),int(ev_slots_var.get()),int(level_var.get()),)
        output = 'Created a parking lot with '+reg_slots_var.get()+' regular slots and '+ev_slots_var.get()+' ev slots on level: '+level_var.get()+ "\n"
        tfield.insert(tk.INSERT, output)

    def parkCar(self):
        """Handler for 'Park Car' button."""
        res = self.park(reg_var.get(),make_var.get(),model_var.get(),color_var.get(),is_electric_var.get(),is_motorcycle_var.get())
        if res == -1:
            tfield.insert(tk.INSERT, "Sorry, parking lot is full\n")
        else:
            output = 'Allocated slot number: '+str(res)+ "\n"
            tfield.insert(tk.INSERT, output)

    def removeCar(self):
        """Handler for 'Remove Car' button."""
        status = self.leave(int(remove_slot_var.get()),int(remove_is_electric_var.get()))
        if status:
            output = 'Slot number '+str(remove_slot_var.get())+' is free\n'
            tfield.insert(tk.INSERT, output)
        else:
            tfield.insert(tk.INSERT, "Unable to remove a car from slot: " + remove_slot_var.get() + "\n")
             
def main():
    """Main function to setup and run the Tkinter application."""
    parkinglot = ParkingLot()
    
    # --- GUI Layout ---
    label_head= tk.Label(root, text = 'Parking Lot Manager', font = 'Arial 14 bold')
    label_head.grid(row=0, column=0, padx = 10, columnspan = 4)

    label_head= tk.Label(root, text = 'Lot Creation', font = 'Arial 12 bold')
    label_head.grid(row=1, column=0, padx = 10, columnspan = 4)

    lbl_num = tk.Label(root, text = 'Number of Regular Spaces', font = 'Arial 12')
    lbl_num.grid(row=2, column=0, padx = 5)

    num_entry = tk.Entry(root, textvariable = reg_slots_var,  width = 6, font='Arial 12')
    num_entry.grid(row = 2, column=1,  padx = 4, pady = 2)

    lbl_ev = tk.Label(root, text = 'Number of EV Spaces', font = 'Arial 12')
    lbl_ev.grid(row=2, column=2, padx = 5)

    num_entry = tk.Entry(root, textvariable = ev_slots_var,  width = 6, font='Arial 12')
    num_entry.grid(row = 2, column=3,  padx = 4, pady = 4)

    lbl_level = tk.Label(root, text = 'Floor Level', font = 'Arial 12')
    lbl_level.grid(row=3, column=0, padx = 5)
    
    level_entry = tk.Entry(root, textvariable = level_var,  width = 6, font='Arial 12')
    level_entry.grid(row = 3, column=1,  padx = 4, pady = 4)
    level_entry.insert(tk.INSERT, "1")

    parkMakeBtn = tk.Button(root, command = parkinglot.makeLot, text = "Create Parking Lot", font="Arial 12", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    parkMakeBtn.grid(row=4, column=0,  padx = 4, pady = 4)

    label_car= tk.Label(root, text = 'Car Management', font = 'Arial 12 bold')
    label_car.grid(row=5, column=0, padx = 10, columnspan = 4)

    lbl_make = tk.Label(root, text = 'Make', font = 'Arial 12')
    lbl_make.grid(row=6, column=0, padx = 5)

    make_entry = tk.Entry(root, textvariable = make_var,  width = 12, font='Arial 12')
    make_entry.grid(row=6, column=1,  padx = 4, pady = 4)

    lbl_model = tk.Label(root, text = 'Model', font = 'Arial 12')
    lbl_model.grid(row=6, column=2, padx = 5)

    model_entry = tk.Entry(root, textvariable = model_var,  width = 12, font='Arial 12')
    model_entry.grid(row=6, column=3,  padx = 4, pady = 4)
    
    lbl_color = tk.Label(root, text = 'Color', font = 'Arial 12')
    lbl_color.grid(row=7, column=0, padx = 5)

    color_entry = tk.Entry(root, textvariable = color_var,  width = 12, font='Arial 12')
    color_entry.grid(row=7, column=1,  padx = 4, pady = 4)

    lbl_reg = tk.Label(root, text = 'Registration #', font = 'Arial 12')
    lbl_reg.grid(row=7, column=2, padx = 5)
    
    reg_entry = tk.Entry(root, textvariable = reg_var,  width = 12, font='Arial 12')
    reg_entry.grid(row=7, column=3,  padx = 4, pady = 4)

    evToggle = tk.Checkbutton(root, text='Electric',variable=is_electric_var, onvalue=1, offvalue=0, font='Arial 12')
    evToggle.grid(column=0, row=8,  padx = 4, pady = 4)

    motorToggle = tk.Checkbutton(root, text='Motorcycle',variable=is_motorcycle_var, onvalue=1, offvalue=0, font='Arial 12')
    motorToggle.grid(column=1, row=8,  padx = 4, pady = 4)

    parkBtn = tk.Button(root, command = parkinglot.parkCar, text = "Park Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    parkBtn.grid(column=0, row=9,  padx = 4, pady = 4)

    lbl_slot = tk.Label(root, text = 'Slot #', font = 'Arial 12')
    lbl_slot.grid(row=10, column=0, padx = 5)

    slot_entry = tk.Entry(root, textvariable = remove_slot_var,  width = 12, font='Arial 12')
    slot_entry.grid(row=10, column=1,  padx = 4, pady = 4)

    evToggle = tk.Checkbutton(root, text='Remove EV?',variable=remove_is_electric_var, onvalue=1, offvalue=0, font='Arial 12')
    evToggle.grid(column=2, row=10,  padx = 4, pady = 4)

    removeBtn = tk.Button(root, command = parkinglot.removeCar, text = "Remove Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    removeBtn.grid(column=0, row=11,  padx = 4, pady = 4)

    spacer1 = tk.Label(root, text="")
    spacer1.grid(row=12, column=0)

    slotRegBtn = tk.Button(root, command = parkinglot.slotNumByReg, text = "Get Slot ID by Registration #", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotRegBtn.grid(column=0, row=13,  padx = 4, pady = 4)

    slot1_entry = tk.Entry(root, textvariable = find_slot_by_reg_var,  width = 12, font='Arial 12')
    slot1_entry.grid(row=13, column=1,  padx = 4, pady = 4)

    slotColorBtn = tk.Button(root, command = parkinglot.slotNumByColor, text = "Get Slot ID by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotColorBtn.grid(column=2, row=13,  padx = 4, pady = 4)

    slot2_entry = tk.Entry(root, textvariable = find_slot_by_color_var,  width = 12, font='Arial 12')
    slot2_entry.grid(row=13, column=3,  padx = 4, pady = 4)
    
    regColorBtn = tk.Button(root, command = parkinglot.regNumByColor, text = "Get Registration # by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    regColorBtn.grid(column=0, row=14,  padx = 4, pady = 4)

    reg1_entry = tk.Entry(root, textvariable = find_reg_by_color_var,  width = 12, font='Arial 12')
    reg1_entry.grid(row=14, column=1,  padx = 4, pady = 4)

    chargeStatusBtn = tk.Button(root, command = parkinglot.chargeStatus, text = "EV Charge Status", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    chargeStatusBtn.grid(column=2, row=14,  padx = 4, pady = 4)

    statusBtn = tk.Button(root, command = parkinglot.status, text = "Current Lot Status", font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5 )
    statusBtn.grid(column=0, row=15,  padx = 4, pady = 4)

    tfield.grid(column=0, row=16, padx = 10, pady = 10, columnspan = 4)
    
    root.mainloop()

if __name__ == '__main__':
    main()