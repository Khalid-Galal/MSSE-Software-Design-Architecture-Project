# Parking Lot Management System - Refactoring Project

This project is a comprehensive refactoring of an initial prototype for a parking lot management application. The goal was to take a functional but flawed codebase, identify key anti-patterns and design issues, and systematically improve it by applying object-oriented design principles and established software design patterns.

The project also includes a high-level architectural proposal for scaling the system using Domain-Driven Design (DDD) and a microservices-based approach to support future business growth, including the management of multiple facilities and Electric Vehicle (EV) charging stations.

## Table of Contents

1.  [Initial Problem Statement](#initial-problem-statement)
2.  [Refactoring and Improvements](#refactoring-and-improvements)
    *   [Phase 1: Code Refactoring & Anti-Pattern Removal](#phase-1-code-refactoring--anti-pattern-removal)
    *   [Phase 2: Software Design Patterns & Principles](#phase-2-software-design-patterns--principles)
3.  [Final Project Structure](#final-project-structure)
4.  [Design Patterns Used](#design-patterns-used)
    *   [Factory Method Pattern](#factory-method-pattern)
    *   [Strategy Pattern](#strategy-pattern)
5.  [How to Run the Application](#how-to-run-the-application)


## Initial Problem Statement

The original codebase was a single-file Tkinter application with several common anti-patterns that hindered its maintainability, testability, and scalability:
- **Poor Structure:** All code, including data models and UI, was in a few files in a flat directory.
- **Tight Coupling:** Business logic was mixed directly with UI code, making the core logic non-reusable and difficult to test.
- **Global State:** The application relied on global variables, making the state difficult to track and manage.
- **Code Duplication:** A parallel and redundant class hierarchy existed for `Vehicle` and `ElectricVehicle`.
- **Lack of Robustness:** The application would crash on invalid user input.
- **Inefficient Logic:** Repetitive loops were used for different data queries.

## Refactoring and Improvements

The codebase was improved in a series of systematic, incremental steps.

### Phase 1: Code Refactoring & Anti-Pattern Removal

This phase focused on cleaning the code and establishing a solid foundation.
- **Project Scaffolding:** Organized the code into a logical `src` directory with a `models` sub-directory for data classes.
- **Improved Readability:** Renamed ambiguous variables to be more descriptive and added docstrings to all classes and methods.
- **Removed Global State:** Encapsulated all application logic and state within a main `ParkingLotApp` class, eliminating global variables.
- **Robust Error Handling:** Implemented `try-except` blocks to catch `ValueError` from user input, preventing application crashes and providing user-friendly error messages.
- **Code Cleanup:** Removed unused imports and deprecated/dead code (e.g., an unused `edit` method).

### Phase 2: Software Design Patterns & Principles

This phase introduced formal design patterns to improve the architecture and object-oriented design.
- **Separation of Concerns:** The core business logic (`ParkingLot` class) was completely decoupled from the Tkinter UI (`ParkingLotApp` class). The `ParkingLot` class now has zero UI dependencies and can be tested or reused independently.
- **Unified Vehicle Hierarchy:** The redundant `ElectricVehicle` class hierarchy was removed. A single `Vehicle` base class now manages electric properties, adhering to the **Don't Repeat Yourself (DRY)** principle.
- **Implementation of Design Patterns:** Introduced the **Factory Method** and **Strategy** patterns to improve flexibility and reduce code duplication (see below).

## Final Project Structure

The final structure of the application is clean and logically organized:

```
parking_lot_manager/
├── src/
│   ├── models/
│   │   ├── __init__.py         # Makes 'models' a Python package
│   │   └── Vehicle.py          # Unified data models for all vehicle types
│   ├── app.py                  # Contains the ParkingLotApp class (UI and event handling)
│   ├── main.py                 # The main entry point for the application
│   ├── parking_lot.py          # Contains the ParkingLot class (core business logic)
│   └── vehicle_factory.py      # Implements the Factory for creating vehicles
└── README.md
```

## Design Patterns Used

Two distinct design patterns were implemented to solve specific problems in the codebase.

### Factory Method Pattern

- **Problem:** The `ParkingLot` class was directly responsible for creating instances of `Car` and `Motorcycle`. This violated the Single Responsibility Principle and coupled the parking lot to concrete vehicle classes.
- **Solution:** A `VehicleFactory` was created to encapsulate all vehicle creation logic. The `ParkingLot` now delegates the creation of vehicle objects to the factory.
- **Benefit:** If a new vehicle type (`Van`, `Truck`) is added in the future, only the factory needs to be modified. The `ParkingLot` class remains unchanged, making the system more extensible and maintainable.

### Strategy Pattern

- **Problem:** The `ParkingLot` class had multiple query methods (`find_slot_by_reg`, `find_slot_by_color`, etc.) that each contained duplicated loops for iterating through the slots.
- **Solution:** A single private `_find_vehicles` method was created. This method accepts a `condition` function (a "strategy") as an argument. The public query methods now define their specific search logic as a `lambda` function and pass it to this central method.
- **Benefit:** This eliminates redundant code (DRY) and makes adding new types of queries trivial. The logic for iteration is in one place, while the specific "strategy" for what to find is injected at runtime.

## How to Run the Application

To run the Parking Lot Management application, follow these steps:

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.
2.  **Clone/Download:** Get the project files and place them in a directory named `parking_lot_manager`.
3.  **Navigate to the Directory:** Open a terminal or command prompt and navigate to the root of the project directory.
    ```bash
    cd path/to/parking_lot_manager
    ```
4.  **Run the Application:** Execute the main entry point file.
    ```bash
    python src/main.py
    ```
5.  The application GUI should launch, and you can now interact with it.

