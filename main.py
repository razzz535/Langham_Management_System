"""
Project Name: Hotel Management Application System for 'LANGHAM Hotels'
Author Name: Raj Jaiswal
Student ID: 850003154
Date: 27/11/2024
Application Purpose: Develop software application for 'LANGHAM Hotels' to manage their day-to-day operations like allocation of rooms, deallocation of rooms, displaying status of rooms, and other functionality.
"""

import os
from datetime import datetime

# Define a class for hotel rooms
class Room:
    """Represents a hotel room with room number and allocation status."""
    def __init__(self, room_no):
        self.room_no = room_no  # Unique room number
        self.is_allocated = False  # Allocation status (default: False)

# Define a class for hotel customers
class Customer:
    """Represents a customer with a unique number and name."""
    def __init__(self, customer_no, customer_name):
        self.customer_no = customer_no  # Unique customer number
        self.customer_name = customer_name  # Customer name

# Define a class to manage room allocations
class RoomAllocation:
    """Represents the allocation of a room to a specific customer."""
    def __init__(self, room_no, customer):
        self.allocated_room_no = room_no  # Room number allocated
        self.allocated_customer = customer  # Customer details

# Define the main hotel management system class
class HotelManagementSystem:
    """Handles all operations for managing a hotel's rooms and allocations."""
    def __init__(self):
        self.rooms = []  # List of Room objects
        self.room_allocations = []  # List of RoomAllocation objects
        self.file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'lhms_850003154.txt')  # File path for saving allocations
        self.file_path_backup = os.path.join(os.path.expanduser('~'), 'Documents', 'lhms_850003154_backup.txt')  # Backup file path

    # Add new rooms to the system
    def add_rooms(self):
        """Allows the user to add new rooms to the hotel."""
        try:
            print("You have selected 'ADD ROOMS' from menu")
            num_rooms = int(input("Please enter the total number of rooms in the Hotel: "))
            print(f"Hotel has {num_rooms} rooms in total")
            print("*" * 75)

            for i in range(num_rooms):
                while True:
                    try:
                        room_no = int(input(f"Please enter room number {i + 1}: "))
                        # Check if room number already exists
                        if any(room.room_no == room_no for room in self.rooms):
                            print("Same room number already exists\nPlease enter a new room number")
                            continue
                        self.rooms.append(Room(room_no))  # Add new room
                        print(f"Room {room_no} has been added successfully")
                        break
                    except ValueError as e:
                        print(f"Error: {e}\nPlease enter a valid room number")

        except ValueError as e:
            print(f"Error: {e}\nPlease try again")
            self.add_rooms()  # Retry on invalid input

    # Delete rooms from the system
    def delete_rooms(self):
        """Allows the user to delete existing rooms from the hotel."""
        if not self.rooms:
            print("No rooms to delete\nPlease add rooms first")
            return

        try:
            print("You have selected 'DELETE ROOMS' from menu")
            num_delete = int(input("How many rooms would you like to delete?: "))
            
            if num_delete > len(self.rooms):
                print(f"Cannot delete more rooms than exist. Only {len(self.rooms)} rooms available.")
                return

            for i in range(num_delete):
                while True:
                    try:
                        print("*" * 75)
                        print(f"Room Deletion {i + 1}:")
                        room_no = int(input("Enter room number to delete: "))
                        
                        # Find the room to delete
                        room = next((r for r in self.rooms if r.room_no == room_no), None)
                        
                        if room is None:
                            print("Room not found. Please enter a valid room number.")
                            continue
                            
                        if room.is_allocated:
                            print(f"Room {room_no} is currently occupied and cannot be deleted.")
                            continue
                            
                        self.rooms.remove(room)  # Remove the room
                        print(f"Room {room_no} has been deleted")
                        break

                    except ValueError as e:
                        print(f"Error: {e}\nPlease enter a valid room number")

        except ValueError as e:
            print(f"Error: {e}\nPlease try again")

    # Display details of all rooms
    def display_rooms(self):
        """Displays all rooms with their details such as status and allocation."""
        if not self.rooms:
            print("No rooms to display\nPlease add rooms first")
            return

        print("You have selected 'DISPLAY ROOMS' from menu")
        print("*" * 75)
        print("Room Details:")
        print("-" * 40)
        
        for room in self.rooms:
            status = "Occupied" if room.is_allocated else "Available"
            print(f"Room Number: {room.room_no}")
            print(f"Status: {status}")
            if room.is_allocated:
                # Show customer details for allocated rooms
                allocation = next((a for a in self.room_allocations if a.allocated_room_no == room.room_no), None)
                if allocation:
                    print(f"Occupied By: {allocation.allocated_customer.customer_name}")
                    print(f"Customer Number: {allocation.allocated_customer.customer_no}")
            print("-" * 40)

    # Allocate rooms to customers
    def allocate_rooms(self):
        """Allocates available rooms to customers."""
        if not self.rooms:
            print("No rooms available. Please add rooms first.")
            return

        try:
            print("You have selected 'ALLOCATE ROOMS' from menu")
            num_allocate = int(input("How many rooms would you like to allocate?: "))
            available_rooms = len([room for room in self.rooms if not room.is_allocated])

            if num_allocate > available_rooms:
                print(f"Cannot allocate more rooms than available. Only {available_rooms} rooms available.")
                return

            for i in range(num_allocate):
                print("*" * 75)
                print(f"Room Allocation {i + 1}:")
                while True:
                    try:
                        room_no = int(input("Please search Room Number to allocate: "))
                        room = next((r for r in self.rooms if r.room_no == room_no), None)

                        if room is None:
                            print("Room not found. Please enter a valid room number.")
                            continue
                        if room.is_allocated:
                            print(f"Room {room_no} is already occupied\nPlease choose another room")
                            continue

                        # Get customer details
                        customer_no = int(input("Please enter Customer Number to allocate: "))
                        customer_name = input("Please enter Customer Name to allocate: ")
                        customer = Customer(customer_no, customer_name)

                        # Create allocation
                        room.is_allocated = True
                        allocation = RoomAllocation(room_no, customer)
                        self.room_allocations.append(allocation)
                        print(f"Room {room_no} has been allocated to {customer_name}")
                        break

                    except ValueError as e:
                        print(f"Error: {e}\nPlease enter valid details")

        except ValueError as e:
            print(f"Error: {e}\nPlease try again")

    # Deallocate rooms from customers
    def deallocate_rooms(self):
        """Deallocates rooms that are currently occupied by customers."""
        if not self.room_allocations:
            print("No allocated rooms to deallocate.")
            return

        try:
            print("You have selected 'DEALLOCATE ROOMS' from menu")
            num_deallocate = int(input("How many rooms would you like to deallocate?: "))

            if num_deallocate > len(self.room_allocations):
                print("Cannot deallocate more rooms than currently allocated.")
                return

            for i in range(num_deallocate):
                print("*" * 75)
                print(f"Room Deallocation {i + 1}:")
                while True:
                    try:
                        room_no = int(input("Please enter Room Number to deallocate: "))
                        # Find room and allocation entry
                        room = next((r for r in self.rooms if r.room_no == room_no), None)
                        allocation = next((a for a in self.room_allocations if a.allocated_room_no == room_no), None)

                        if room is None or allocation is None:
                            print("Room not found or not allocated.")
                            continue

                        # Remove allocation and mark room as available
                        room.is_allocated = False
                        self.room_allocations.remove(allocation)
                        print(f"Room {room_no} has been deallocated")
                        break

                    except ValueError as e:
                        print(f"Error: {e}\nPlease enter a valid room number")

        except ValueError as e:
            print(f"Error: {e}\nPlease try again")

    # Display all room allocations
    def display_allocations(self):
        """Displays all current room allocations including customer details."""
        if not self.room_allocations:
            print("No allocated rooms to display\nPlease allocate rooms first")
            return

        print("You have selected 'DISPLAY ROOM ALLOCATION DETAILS' from menu")
        for allocation in self.room_allocations:
            print("*" * 75)
            print(f"Room Number: {allocation.allocated_room_no}")
            print(f"Customer Number: {allocation.allocated_customer.customer_no}")
            print(f"Customer Name: {allocation.allocated_customer.customer_name}")

    # Save room allocations to a file
    def save_allocations(self):
        """Saves all room allocation details to a text file."""
        if not self.room_allocations:
            print("No allocations to save.")
            return

        try:
            print("You have selected 'SAVE THE ROOM ALLOCATIONS TO A FILE' from menu")
            print("*" * 75)
            
            with open(self.file_path, 'w') as file:
                now = datetime.now()
                for allocation in self.room_allocations:
                    allocation_details = (
                        "*" * 75 + "\n"
                        f"Room Number: {allocation.allocated_room_no}\n"
                        f"Customer Number: {allocation.allocated_customer.customer_no}\n"
                        f"Customer Name: {allocation.allocated_customer.customer_name}\n"
                        f"Current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    file.write(allocation_details)
            
            print(f"File saved as 'lhms_850003154.txt' under Documents folder")

        except PermissionError:
            print("Error: Permission denied. Unable to write to file.")
        except IOError as e:
            print(f"Error writing to file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving: {e}")

    # Display room allocations from file
    def show_allocations(self):
        """Reads and displays room allocation details from the saved file."""
        try:
            print("You have selected 'SHOW THE ROOM ALLOCATIONS FROM A FILE' from menu")
            print("*" * 75)

            if not os.path.exists(self.file_path):
                raise FileNotFoundError("Allocation file not found. Please save allocations first.")

            with open(self.file_path, 'r') as file:
                content = file.read()
                if not content:
                    print("No allocations found in file.")
                    return
                print(content)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except PermissionError:
            print("Error: Permission denied. Unable to read file.")
        except IOError as e:
            print(f"Error reading file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading: {e}")

    # Backup allocations to a separate file
    def backup(self):
        """Creates a backup of the allocation file and removes the original."""
        try:
            print("You have selected 'BACKUP' from menu")
            print("*" * 75)

            if not os.path.exists(self.file_path):
                raise FileNotFoundError("No allocation file found to backup.")

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.file_path_backup.replace('.txt', f'_{timestamp}.txt')

            # Remove existing backup if exists
            if os.path.exists(backup_path):
                print(f"Existing backup file found - will be replaced")
                os.remove(backup_path)

            # Create backup
            with open(self.file_path, 'r') as source:
                content = source.read()
                with open(backup_path, 'w') as backup:
                    backup.write(content)

            # Delete original file after successful backup
            os.remove(self.file_path)
            print(f"Backup created successfully as '{os.path.basename(backup_path)}'")
            print("Original file has been deleted")

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except PermissionError:
            print("Error: Permission denied while creating backup.")
        except IOError as e:
            print(f"Error during backup process: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during backup: {e}")

    # Display the main menu and handle user input
    def menu(self):
        """Displays the main menu and handles user selections."""
        while True:
            try:
                print("*" * 75)
                print("                 LANGHAM HOTEL MANAGEMENT SYSTEM                  ")
                print("                            MENU                                 ")
                print("*" * 75)
                print("0. Exit")
                print("1. Add Rooms")
                print("2. Delete Rooms")
                print("3. Display Rooms")
                print("4. Allocate Rooms")
                print("5. De-Allocate Rooms")
                print("6. Display Room Allocation Details")
                print("7. Save the Room Allocations To a File")
                print("8. Show the Room Allocations From a File")
                print("9. Backup")
                print("*" * 75)

                choice = int(input("Enter Your Choice Number Here (0-9): "))

                if choice == 0:
                    print("Thank you for using LANGHAM HOTEL MANAGEMENT SYSTEM")
                    break
                elif choice == 1:
                    self.add_rooms()
                elif choice == 2:
                    self.delete_rooms()
                elif choice == 3:
                    self.display_rooms()
                elif choice == 4:
                    self.allocate_rooms()
                elif choice == 5:
                    self.deallocate_rooms()
                elif choice == 6:
                    self.display_allocations()
                elif choice == 7:
                    self.save_allocations()
                elif choice == 8:
                    self.show_allocations()
                elif choice == 9:
                    self.backup()
                else:
                    print("Please enter a valid number between 0-9")

            except ValueError as e:
                print(f"Error: {e}\nPlease enter a valid number")
            except Exception as e:
                print(f"An unexpected error occurred: {e}\nPlease try again")

def main():
    # Main function to start the application
    hotel_system = HotelManagementSystem()
    hotel_system.menu()

if __name__ == "__main__":
    main()
