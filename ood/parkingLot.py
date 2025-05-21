from collections import deque
from enum import Enum
from datetime import datetime
import time

class VehicleType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    COMPACT = "COMPACT"
    LARGE = "LARGE"
    
class ParkingSpotType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    COMPACT = "COMPACT"
    LARGE = "LARGE"
    
    

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: ParkingSpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.parked_vehicle = None
        self.entry_time = None
        
    def is_available(self) -> bool:
        return not self.is_occupied
    
    def park(self, vehicle) -> None:
        self.parked_vehicle = vehicle
        self.is_occupied = True
        self.entry_time = datetime.now()
        
    def leave(self, duration_seconds=None) -> float:
        if not self.parked_vehicle:
            return 0.0
        if duration_seconds is None:
            exit_time = datetime.now()
            hours_parked = (exit_time - self.entry_time).total_seconds() / 3600
        else:
            hours_parked = duration_seconds / 3600  # Simulated duration for testing
        self.parked_vehicle = None
        self.is_occupied = False
        self.start_time = None
        return hours_parked
        
class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        
class ParkingLot:
    
    PARKING_RATES = {
        ParkingSpotType.MOTORCYCLE: 1.5,
        ParkingSpotType.COMPACT: 2.5,
        ParkingSpotType.LARGE: 3.5
    }
    def __init__(self, num_compact: int, num_large: int, num_motorcycle: int):
        self.available_spots = {
            ParkingSpotType.COMPACT: deque(),
            ParkingSpotType.LARGE: deque(),
            ParkingSpotType.MOTORCYCLE: deque()
        }
        self.occupied_spots = {} #{license_plate: ParkingSpot}
        
        for i in range(num_compact):
            self.available_spots[ParkingSpotType.COMPACT].append(ParkingSpot(f"C{i}", ParkingSpotType.COMPACT))
            self.available_spots[ParkingSpotType.LARGE].append(ParkingSpot(f"L{i}", ParkingSpotType.LARGE))
            self.available_spots[ParkingSpotType.MOTORCYCLE].append(ParkingSpot(f"M{i}", ParkingSpotType.MOTORCYCLE))
    
    def find_spot(self, vehicle: Vehicle) -> bool:
        spot_type = self.get_spot_type(vehicle)
        if not self.available_spots[spot_type]:
            return False
        spot = self.available_spots[spot_type].popleft()
        spot.park(vehicle)
        self.occupied_spots[vehicle.license_plate] = spot
        return True
    
    def leave_vehicle(self, license_plate: str, duration_seconds=None) -> float:
        if license_plate not in self.occupied_spots:
            return -1.0
        
        spot = self.occupied_spots.pop(license_plate)
        duration_hours = spot.leave(duration_seconds)
        parking_fee = duration_hours * self.PARKING_RATES[spot.spot_type]
        self.available_spots[spot.spot_type].append(spot)
        return round(parking_fee, 2)
    
    def get_spot_type(self, vehicle: Vehicle) -> ParkingSpotType:
        return ParkingSpotType[vehicle.vehicle_type.name]
    
    def get_available_spots_count(self) -> dict:
        return {spot_type: len(self.available_spots[spot_type]) for spot_type in self.available_spots}
    
    def is_vehicle_parked(self, license_plate: str) -> bool:
        return license_plate in self.occupied_spots
    
    
# Initialize a parking lot
parking_lot = ParkingLot(num_compact=5, num_large=5, num_motorcycle=5)

# Create vehicles
vehicle1 = Vehicle("CAR001", VehicleType.COMPACT)
vehicle2 = Vehicle("CAR002", VehicleType.LARGE)
vehicle3 = Vehicle("CAR003", VehicleType.MOTORCYCLE)

# Park vehicles
parking_lot.find_spot(vehicle1)
parking_lot.find_spot(vehicle2)
parking_lot.find_spot(vehicle3)

# Simulated durations in seconds (1.2, 1.8, and 2.3 hours)
durations = [1.2 * 3600, 1.8 * 3600, 2.3 * 3600]

# Calculate parking fees
fee1 = parking_lot.leave_vehicle("CAR001", durations[0])
fee2 = parking_lot.leave_vehicle("CAR002", durations[1])
fee3 = parking_lot.leave_vehicle("CAR003", durations[2])

# Print results
print(f"Car1 (1.2 hours) Parking Fee: ${fee1}")
print(f"Car2 (1.8 hours) Parking Fee: ${fee2}")
print(f"Car3 (2.3 hours) Parking Fee: ${fee3}")
