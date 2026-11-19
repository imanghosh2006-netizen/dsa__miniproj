from collections import deque
import time

class ParkingLotSystem:
    def __init__(self, capacity):
        self.capacity = capacity
        # Stack for available parking slots (LIFO allocation)
        self.available_slots = [i for i in range(capacity, 0, -1)]
        # Hash Map: plate_number -> {slot, entry_time}
        self.parked_vehicles = {}
        # Queue: waiting list for cars when lot is full (FIFO)
        self.waiting_queue = deque()

    def vehicle_entry(self, plate):
        plate = plate.upper()
        if plate in self.parked_vehicles:
            print(f"[!] Vehicle {plate} is already parked in Slot {self.parked_vehicles[plate]['slot']}.")
            return
        if plate in self.waiting_queue:
            print(f"[!] Vehicle {plate} is already in the waiting queue.")
            return

        if self.available_slots:
            slot = self.available_slots.pop()  # Pop from stack
            self.parked_vehicles[plate] = {
                "slot": slot,
                "entry_time": time.strftime("%H:%M:%S")
            }
            print(f"[✓] TICKET ISSUED: Vehicle {plate} -> Allocated Slot #{slot} at {self.parked_vehicles[plate]['entry_time']}")
        else:
            self.waiting_queue.append(plate)  # Enqueue
            print(f"[FULL] Lot at max capacity ({self.capacity}). {plate} added to Waiting Queue (Position: {len(self.waiting_queue)}).")

    def vehicle_exit(self, plate):
        plate = plate.upper()
        if plate not in self.parked_vehicles:
            print(f"[!] Vehicle {plate} not found in the parking lot.")
            return

        record = self.parked_vehicles.pop(plate)  # Remove from Hash Map
        freed_slot = record["slot"]
        exit_time = time.strftime("%H:%M:%S")
        print(f"[✓] EXIT PROCESSED: {plate} left Slot #{freed_slot} (In: {record['entry_time']} | Out: {exit_time})")

        # Push freed slot back to stack
        self.available_slots.append(freed_slot)

        # Immediately assign to next car in FIFO waiting queue if any
        if self.waiting_queue:
            next_plate = self.waiting_queue.popleft()
            print(f"[->] Auto-assigning freed Slot #{freed_slot} to waiting vehicle {next_plate}...")
            self.vehicle_entry(next_plate)

    def display_status(self):
        print("\n" + "="*50)
        print(f"PARKING LOT STATUS (Available Slots: {len(self.available_slots)}/{self.capacity})")
        print("="*50)
        print(f"Available Stack : {sorted(self.available_slots)}")
        print("Parked Vehicles (Hash Map):")
        if not self.parked_vehicles:
            print("  None")
        else:
            for plate, info in self.parked_vehicles.items():
                print(f"  - {plate:<10} | Slot #{info['slot']:<3} | Entry: {info['entry_time']}")
        print(f"Waiting Queue   : {list(self.waiting_queue)}")
        print("="*50 + "\n")

def main():
    lot = ParkingLotSystem(capacity=3)  # Small capacity to easily demo waiting queue
    while True:
        print("1. Vehicle Entry | 2. Vehicle Exit | 3. Lot Status | 4. Exit Program")
        choice = input("Select option: ").strip()
        if choice == '1':
            plate = input("Enter License Plate (e.g., WB-02-AB-1234): ").strip()
            if plate:
                lot.vehicle_entry(plate)
        elif choice == '2':
            plate = input("Enter License Plate to Exit: ").strip()
            if plate:
                lot.vehicle_exit(plate)
        elif choice == '3':
            lot.display_status()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()