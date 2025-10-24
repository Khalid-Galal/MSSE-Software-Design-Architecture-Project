### **Part 1: Initial Refactoring and Anti-Pattern Removal**

The first phase of this project involved analyzing the initial prototype codebase to identify and rectify foundational issues and anti-patterns. The goal of this phase was not to change the application's functionality but to improve its internal quality, making it more readable, maintainable, and scalable. This initial cleanup is a critical prerequisite for implementing more complex software design patterns effectively.

The following improvements were made:

**1. Project File Organization**

*   **Observation:** The initial code consisted of three Python files (`Vehicle.py`, `ElectricVehicle.py`, and `ParkingManager.py`) located in a single, flat directory. This lack of structure is common in prototypes but is not suitable for a production application as it makes navigation and separation of concerns difficult.
*   **Action Taken:** A standard Python project structure was created. All source code was moved into a `src` directory. Within `src`, a `models` directory was created to house the data model classes.
    *   `Vehicle.py` and `ElectricVehicle.py` were moved to `src/models/`.
    *   `ParkingManager.py` was renamed to `src/main.py` to better signify its role as the application's primary entry point.
    *   An empty `src/models/__init__.py` file was added to allow the `models` directory to be treated as a Python package.
*   **Justification:** This structural change immediately improves the project's organization. It establishes a clear separation of concerns between data representation (the models) and application logic/presentation (the main file). This makes the codebase easier to understand and is a fundamental step toward a more robust architecture.

**2. Anti-Pattern: Poor/Non-explicit Variable Names**

*   **Observation:** The code used several short, ambiguous variable names for the Tkinter `StringVar` and `IntVar` objects, such as `num_value`, `ev_value`, `ev_car_value`, and `slot1_value`. It was not immediately clear what part of the UI or data flow these variables corresponded to.
*   **Action Taken:** The Tkinter variables were renamed to be explicit and descriptive.
    *   `num_value` -> `reg_slots_var`
    *   `ev_value` -> `ev_slots_var`
    *   `level_value` -> `level_var`
    *   `ev_car_value` -> `is_electric_var`
    *   `slot1_value` -> `find_slot_by_reg_var`
*   **Justification:** Clear and descriptive variable names are crucial for code readability. This change allows a developer to understand the purpose of a variable at a glance without needing to trace its usage throughout the code. It reduces cognitive overhead and minimizes the risk of errors during future modifications.

**3. Anti-Pattern: Lack of Comments**

*   **Observation:** The original source code was entirely devoid of comments or docstrings. This forced anyone reading the code to deduce the purpose of each class and method solely from its implementation, increasing the time required to understand the system.
*   **Action Taken:** Docstrings were added to all classes and key methods. These docstrings provide a high-level summary of the element's purpose. For example, the `ParkingLot` class now has a docstring explaining that it "Manages the state and operations of a single parking lot level."
*   **Justification:** Documentation in the form of docstrings is a cornerstone of maintainable Python code. It clarifies the intent behind the code, making it easier for team members (and the original author in the future) to use, debug, and extend the system. It also allows for the use of automated documentation generation tools.

**4. Anti-Pattern: Broad or Unused Imports**

*   **Observation:** The main application file contained `import sys`, but the `sys` module was never used within the code.
*   **Action Taken:** The `import sys` statement was removed. The remaining imports were updated to reflect the new project structure (e.g., `from models import Vehicle`).
*   **Justification:** Removing unused imports is a fundamental code hygiene practice. It cleans up the code's namespace, prevents potential confusion, and ensures that the program does not needlessly load modules, which can have a minor impact on startup time and memory usage.

### **Part 2: Architectural Improvement - Separation of Concerns**

Following the initial cleanup, the next major focus was to refactor the application's architecture to address two critical anti-patterns: **global variables** and the **tight coupling of business logic and user interface code**.

**5. Anti-Pattern: Global Variables**

*   **Observation:** The `root` Tkinter window and the primary `parkinglot` object were instantiated in the global scope. This practice is problematic because it allows any function or method within the file to access and modify this global state, leading to unpredictable behavior and making the code difficult to debug.
*   **Action Taken:** The entire application's state and behavior were encapsulated within a new class, `ParkingLotApp`. This class is instantiated once in the main execution block. The `ParkingLot` object and all Tkinter widgets now exist as instance variables (`self.parking_lot`, `self.tfield`), eliminating the need for any global variables.
*   **Justification:** Encapsulation is a core principle of object-oriented programming. By removing global state, we make the data flow explicit and controlled. The application is now more robust, and its state is easier to manage and reason about.

**6. Decoupling Business Logic from the User Interface**

*   **Observation:** The most significant architectural flaw in the original prototype was the mixing of concerns. The `ParkingLot` class, which should only manage the rules and state of a parking lot, was directly dependent on the Tkinter framework. For example, its `status()` method contained the line `tfield.insert(tk.INSERT, output)`, directly manipulating a UI widget. This made the core logic impossible to test without a running GUI and impossible to reuse in any other context (e.g., a web application).
*   **Action Taken:**
    1.  The `ParkingLot` class was moved to its own file (`parking_lot.py`) and all `tkinter` dependencies were removed.
    2.  Methods that previously printed to the UI were refactored to `return` the results as strings or other data structures. For instance, `get_status()` now compiles and returns a complete status report string.
    3.  A new UI-centric class, `ParkingLotApp`, was created in `app.py`. This class is responsible for building the GUI.
    4.  The `ParkingLotApp` holds an *instance* of the `ParkingLot` class. Its event handler methods (e.g., `_handle_park_car`) now act as intermediaries: they gather input from the UI, call the appropriate methods on the `parking_lot` instance, receive the returned data, and then update the UI accordingly.
*   **Justification:** This refactoring establishes a clear boundary between the *model* (the `ParkingLot` class, which handles data and business rules) and the *view/presenter* (the `ParkingLotApp` class, which handles presentation and user interaction). This separation is a cornerstone of robust software design. It dramatically improves **testability** (we can now write unit tests for `ParkingLot`), **reusability** (the `ParkingLot` logic can be imported anywhere), and **maintainability** (UI changes will not affect the core logic, and vice versa).
### **Part 3: Implementing Design Patterns and Principles**

With a clean architecture in place, the project's focus shifted to improving the object-oriented design by applying established principles and design patterns. This phase addressed code duplication and improper separation of responsibilities.

**7. Anti-Pattern: Unnecessary Abstractions and Code Duplication**

*   **Observation:** The codebase contained two parallel class hierarchies for vehicles: one starting with a `Vehicle` base class and another with an `ElectricVehicle` base class. Both base classes duplicated common attributes (`regnum`, `make`, `model`, `color`) and their corresponding getter methods. This is a classic violation of the **Don't Repeat Yourself (DRY)** principle, which leads to maintenance issues.
*   **Action Taken:** The `ElectricVehicle.py` file was eliminated entirely. The `Vehicle` class in `models/Vehicle.py` was refactored to be the single base class for all vehicle types. It was enhanced to include an `is_electric` flag and a `charge` attribute, which are conditionally initialized. This creates a single, unified, and logical inheritance tree where an "electric car" is simply a `Car` object with its `is_electric` flag set to true.
*   **Justification:** This change dramatically simplifies the domain model. By creating a single source of truth for vehicle attributes, we make the code easier to understand and modify. Future changes to vehicle properties only need to be made in one place, reducing development effort and the likelihood of introducing bugs.

**8. Design Pattern: Factory Method for Object Creation**

*   **Observation:** The `park` method within the `ParkingLot` class was responsible for both parking a vehicle *and* creating the vehicle object itself. This violated the **Single Responsibility Principle (SRP)**, which states that a class should have only one reason to change. The `ParkingLot` was coupled to the concrete `Car` and `Motorcycle` classes, meaning if a new vehicle type were added, the `ParkingLot` class itself would need to be modified.
*   **Action Taken:** The **Factory Method** creational design pattern was implemented.
    1.  A new `VehicleFactory` class was created. Its sole purpose is to handle the logic of instantiating and returning specific vehicle objects based on input parameters (e.g., `vehicle_type`).
    2.  The `ParkingLot` class was refactored to use this factory. Instead of containing `if/else` logic to create vehicles, it now simply calls `self.factory.create_vehicle(...)`.
*   **Justification:** The introduction of a factory decouples the `ParkingLot` (the *client*) from the concrete `Vehicle` classes (the *products*). This is a powerful technique that localizes the logic for object creation. The `ParkingLot` no longer needs to know about every type of vehicle that exists. To add a new `Van` type, we would only need to update the `VehicleFactory`, with no changes required in `ParkingLot`, making the system more flexible, scalable, and easier to maintain.

### **Part 4: Ensuring Application Robustness**

A key requirement for any software is the ability to handle unexpected or invalid user input without failing. The original prototype was brittle and would crash if the user did not provide input in the exact format the program expected. This phase focused on rectifying this issue.

**9. Anti-Pattern: Crashing on Invalid User Input / Improper Exception Handling**

*   **Observation:** The application performed direct type conversions on user input (e.g., `int(reg_slots_var.get())`). If a user entered text that could not be converted, such as "five" or leaving the field blank, the program would raise a `ValueError` and immediately crash. This provides a poor user experience and demonstrates a lack of defensive programming.
*   **Action Taken:**
    1.  The code sections responsible for unsafe type conversions in the `app.py` file were wrapped in `try...except` blocks.
    2.  These blocks are configured to specifically catch the `ValueError` exception.
    3.  Within the `except` block, instead of allowing the program to terminate, a clear error message is generated and displayed to the user in the application's own output text field. For example, `_output("ERROR: Please enter valid numbers for slots and level.\n")`.
    4.  Additionally, basic validation was added to the car parking handler to ensure all necessary fields are filled out.
*   **Justification:** This demonstrates the correct way to handle exceptions. We are not just preventing the application from crashing; we are providing direct, contextual feedback to the user, guiding them to correct their input. This makes the application significantly more robust and user-friendly. By catching a *specific* exception (`ValueError`), we avoid masking other potential bugs, which is a common pitfall of overly broad `except:` clauses. This directly addresses the anti-pattern of improper exception handling and is a critical step in creating reliable software.

### **Part 5: Improving Logic with the Strategy Pattern**

The final code improvement phase focused on refining the internal algorithms of the `ParkingLot` class to reduce complexity and duplication, which was accomplished by implementing a second design pattern.

**10. Anti-Pattern: Clumsy, Unnecessary Loop Statements**

*   **Observation:** Within the `ParkingLot` class, multiple methods existed to query vehicle information (`find_reg_nums_by_color`, `find_slot_nums_by_color`, `find_slot_num_by_reg`). Each of these methods contained its own `for` loops to iterate through the `slots` and `evSlots` lists. This resulted in significant code duplication, as the looping mechanism was repeated in every method, with only the inner conditional logic being different.
*   **Action Taken:** The **Strategy** behavioral design pattern was implemented to eliminate this redundancy.
    1.  A single private helper method, `_find_vehicles`, was created. This method contains the master logic for iterating through all occupied slots (both regular and EV).
    2.  This helper method accepts a callable function, `condition`, as an argument. This function represents the "strategy" and encapsulates the specific filtering logic (e.g., checking for a matching color or registration number).
    3.  The original public query methods were refactored to be simple, concise one-liners. They now define their specific search criteria using a `lambda` function (the strategy) and pass it to the `_find_vehicles` method.
*   **Justification:** This refactoring provides several benefits. It perfectly adheres to the **Don't Repeat Yourself (DRY)** principle by centralizing the iteration logic. It is a practical and effective implementation of the Strategy pattern, where different algorithms (search criteria) are encapsulated and made interchangeable. Most importantly, it makes the system highly extensible. To add a new query, such as "find vehicles by make," a developer only needs to add a new one-line public method with the appropriate lambda strategy, without writing any new loops, thereby reducing development time and the potential for error.