import tkinter as tk
from parking_lot import ParkingLot

class ParkingLotApp:
    """
    This class encapsulates the entire Tkinter GUI application.
    It handles UI creation and user event handling.
    """
    def __init__(self, root):
        self.root = root
        self.parking_lot = ParkingLot()

        self.root.title("Parking Lot Manager")
        self.root.geometry("650x850")
        self.root.resizable(0, 0)
        
        # --- UI Variables ---
        self.reg_slots_var = tk.StringVar()
        self.ev_slots_var = tk.StringVar()
        self.level_var = tk.StringVar(value="1")
        self.make_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.reg_var = tk.StringVar()
        self.is_electric_var = tk.IntVar()
        self.is_motorcycle_var = tk.IntVar()
        self.remove_slot_var = tk.StringVar()
        self.remove_is_electric_var = tk.IntVar()
        self.find_slot_by_reg_var = tk.StringVar()
        self.find_slot_by_color_var = tk.StringVar()
        self.find_reg_by_color_var = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        """Creates and lays out all the widgets in the main window."""
        # --- Output Text Field ---
        self.tfield = tk.Text(self.root, width=70, height=15)
        
        # --- Lot Creation Frame ---
        label_head = tk.Label(self.root, text='Parking Lot Manager', font='Arial 14 bold')
        label_head.grid(row=0, column=0, padx=10, columnspan=4)
        
        lot_frame = tk.LabelFrame(self.root, text="Lot Creation", font='Arial 12 bold', padx=5, pady=5)
        lot_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        tk.Label(lot_frame, text='Number of Regular Spaces', font='Arial 12').grid(row=0, column=0, padx=5, sticky="w")
        tk.Entry(lot_frame, textvariable=self.reg_slots_var, width=6, font='Arial 12').grid(row=0, column=1, padx=4, pady=2)
        tk.Label(lot_frame, text='Number of EV Spaces', font='Arial 12').grid(row=0, column=2, padx=5, sticky="w")
        tk.Entry(lot_frame, textvariable=self.ev_slots_var, width=6, font='Arial 12').grid(row=0, column=3, padx=4, pady=4)
        tk.Label(lot_frame, text='Floor Level', font='Arial 12').grid(row=1, column=0, padx=5, sticky="w")
        tk.Entry(lot_frame, textvariable=self.level_var, width=6, font='Arial 12').grid(row=1, column=1, padx=4, pady=4)
        tk.Button(lot_frame, command=self._handle_make_lot, text="Create Parking Lot", font="Arial 12", bg='lightblue').grid(row=2, column=0, padx=4, pady=4)
        
        # --- Car Management Frame ---
        car_frame = tk.LabelFrame(self.root, text="Car Management", font='Arial 12 bold', padx=5, pady=5)
        car_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        tk.Label(car_frame, text='Make', font='Arial 12').grid(row=0, column=0, padx=5, sticky="w")
        tk.Entry(car_frame, textvariable=self.make_var, width=12, font='Arial 12').grid(row=0, column=1, padx=4, pady=4)
        tk.Label(car_frame, text='Model', font='Arial 12').grid(row=0, column=2, padx=5, sticky="w")
        tk.Entry(car_frame, textvariable=self.model_var, width=12, font='Arial 12').grid(row=0, column=3, padx=4, pady=4)
        tk.Label(car_frame, text='Color', font='Arial 12').grid(row=1, column=0, padx=5, sticky="w")
        tk.Entry(car_frame, textvariable=self.color_var, width=12, font='Arial 12').grid(row=1, column=1, padx=4, pady=4)
        tk.Label(car_frame, text='Registration #', font='Arial 12').grid(row=1, column=2, padx=5, sticky="w")
        tk.Entry(car_frame, textvariable=self.reg_var, width=12, font='Arial 12').grid(row=1, column=3, padx=4, pady=4)
        
        tk.Checkbutton(car_frame, text='Electric', variable=self.is_electric_var, onvalue=1, offvalue=0, font='Arial 12').grid(column=0, row=2, padx=4, pady=4)
        tk.Checkbutton(car_frame, text='Motorcycle', variable=self.is_motorcycle_var, onvalue=1, offvalue=0, font='Arial 12').grid(column=1, row=2, padx=4, pady=4)
        tk.Button(car_frame, command=self._handle_park_car, text="Park Car", font="Arial 11", bg='lightblue').grid(column=0, row=3, padx=4, pady=4)
        
        tk.Label(car_frame, text='Slot #', font='Arial 12').grid(row=4, column=0, padx=5, sticky="w")
        tk.Entry(car_frame, textvariable=self.remove_slot_var, width=12, font='Arial 12').grid(row=4, column=1, padx=4, pady=4)
        tk.Checkbutton(car_frame, text='Is EV?', variable=self.remove_is_electric_var, onvalue=1, offvalue=0, font='Arial 12').grid(column=2, row=4, padx=4, pady=4)
        tk.Button(car_frame, command=self._handle_remove_car, text="Remove Car", font="Arial 11", bg='lightblue').grid(column=0, row=5, padx=4, pady=4)
        
        # --- Queries Frame ---
        query_frame = tk.LabelFrame(self.root, text="Queries", font='Arial 12 bold', padx=5, pady=5)
        query_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        tk.Button(query_frame, command=self._handle_slot_num_by_reg, text="Get Slot # by Reg", font="Arial 11", bg='lightblue').grid(column=0, row=0, padx=4, pady=4)
        tk.Entry(query_frame, textvariable=self.find_slot_by_reg_var, width=12, font='Arial 12').grid(row=0, column=1, padx=4, pady=4)
        tk.Button(query_frame, command=self._handle_slot_num_by_color, text="Get Slot # by Color", font="Arial 11", bg='lightblue').grid(column=2, row=0, padx=4, pady=4)
        tk.Entry(query_frame, textvariable=self.find_slot_by_color_var, width=12, font='Arial 12').grid(row=0, column=3, padx=4, pady=4)
        tk.Button(query_frame, command=self._handle_reg_num_by_color, text="Get Reg # by Color", font="Arial 11", bg='lightblue').grid(column=0, row=1, padx=4, pady=4)
        tk.Entry(query_frame, textvariable=self.find_reg_by_color_var, width=12, font='Arial 12').grid(row=1, column=1, padx=4, pady=4)

        # --- Status Frame ---
        status_frame = tk.LabelFrame(self.root, text="Status", font='Arial 12 bold', padx=5, pady=5)
        status_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        tk.Button(status_frame, command=self._handle_charge_status, text="EV Charge Status", font="Arial 11", bg='lightblue').grid(column=0, row=0, padx=4, pady=4)
        tk.Button(status_frame, command=self._handle_status, text="Current Lot Status", font="Arial 11", bg='PaleGreen1').grid(column=1, row=0, padx=4, pady=4)

        self.tfield.grid(column=0, row=5, padx=10, pady=10, columnspan=4)
    
    # --- Private Handler Methods ---
    def _output(self, message):
        """Helper method to insert text into the output field."""
        self.tfield.insert(tk.INSERT, message)

    def _handle_make_lot(self):
        result = self.parking_lot.create_parking_lot(
            int(self.reg_slots_var.get()), 
            int(self.ev_slots_var.get()), 
            int(self.level_var.get())
        )
        self._output(result)

    def _handle_park_car(self):
        result = self.parking_lot.park(
            self.reg_var.get(), 
            self.make_var.get(), 
            self.model_var.get(), 
            self.color_var.get(), 
            self.is_electric_var.get(), 
            self.is_motorcycle_var.get()
        )
        self._output(result)

    def _handle_remove_car(self):
        result = self.parking_lot.leave(
            int(self.remove_slot_var.get()), 
            self.remove_is_electric_var.get()
        )
        self._output(result)

    def _handle_slot_num_by_reg(self):
        result = self.parking_lot.find_slot_num_by_reg(self.find_slot_by_reg_var.get())
        self._output(result)

    def _handle_slot_num_by_color(self):
        result = self.parking_lot.find_slot_nums_by_color(self.find_slot_by_color_var.get())
        self._output(result)

    def _handle_reg_num_by_color(self):
        result = self.parking_lot.find_reg_nums_by_color(self.find_reg_by_color_var.get())
        self._output(result)

    def _handle_status(self):
        result = self.parking_lot.get_status()
        self._output(result)

    def _handle_charge_status(self):
        result = self.parking_lot.get_charge_status()
        self._output(result)