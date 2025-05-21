from enum import Enum
from collections import deque
from datetime import datetime
import math
import unittest
from time import sleep
class VehicleTypes(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    TRUCK = "TRUCK"
    
class ParkingTypes(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Vehicle():
    def __init__(self, vehicle_type, license_plate):
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        
        
        
class ParkingSpot():
    def __init__(self, lot_id, lot_type):
        self.lot_id = lot_id
        self.lot_type = lot_type
        self.license_plate = None
        self.start_time = None
        
        
    def occupy(self, license_plate, lot_type):
        if self.license_plate:
            return False
        if lot_type != self.lot_type:
            return False
        self.start_time = datetime.now()
        self.license_plate = license_plate
        return True

    def vacate(self, license_plate):
        if license_plate != self.license_plate:
            return -1.0
        duration = (datetime.now() - self.start_time).total_seconds() 
        self.license_plate = None
        self.start_time = None
        return round(duration, 2)
        
    
class ParkingLot():
    
    def __init__(self, num_small, num_medium, num_large):
        self.available_space = {
            ParkingTypes.SMALL: deque(),
            ParkingTypes.MEDIUM: deque(),
            ParkingTypes.LARGE: deque()
        }
        self.occupied_space = {} #{license_plate: ParkingSpot}
        for i in range(num_small):
            self.available_space[ParkingTypes.SMALL].append(ParkingSpot(f"S{i}", ParkingTypes.SMALL))
        for i in range(num_medium):
            self.available_space[ParkingTypes.MEDIUM].append(ParkingSpot(f"M{i}", ParkingTypes.MEDIUM))     
        for i in range(num_large):
            self.available_space[ParkingTypes.LARGE].append(ParkingSpot(f"L{i}", ParkingTypes.LARGE))
    def vehicle_types_to_parking_types(self, vehicle_type):
        mapping = {
            VehicleTypes.MOTORCYCLE: ParkingTypes.SMALL,
            VehicleTypes.CAR: ParkingTypes.MEDIUM,
            VehicleTypes.TRUCK: ParkingTypes.LARGE
        }    
        return mapping[vehicle_type]
    def is_enough_spot(self, lot_type):
        
        if len(self.available_space[lot_type]) > 0:
            return True
        else:
            return False
    def park(self, license_plate, vehicle_type):
        lot_type = self.vehicle_types_to_parking_types(vehicle_type)
        if not self.is_enough_spot(lot_type):
            return False
        if license_plate in self.occupied_space:
            return False
        cur_spot = self.available_space[lot_type].popleft()
        
        is_parked = cur_spot.occupy(license_plate, lot_type)
        if not is_parked:
            return False
            
        self.occupied_space[license_plate] = cur_spot
        return True
    def calculate_fee(self, duration, spot_type):
        parking_rate = {
            ParkingTypes.SMALL: 1.5,
            ParkingTypes.MEDIUM: 2.5,
            ParkingTypes.LARGE: 3.5
        }
        # 将秒转换为小时
        duration_hours = duration / 3600.0
        if duration_hours < 0.25:
            return 0.0
        duration_hours = math.ceil(duration_hours / 0.25) * 0.25
        fee = parking_rate[spot_type] * duration_hours
        return fee           
    def leave(self, license_plate):
        if license_plate not in self.occupied_space:
            return -1.0
        #spot_type vheicle type混用
        #离开之后要删除占用记录
        cur_spot = self.occupied_space.pop(license_plate)
        if license_plate != cur_spot.license_plate:
            return -1.0
        duration = cur_spot.vacate(license_plate)
        fee = self.calculate_fee(duration, cur_spot.lot_type)
        #忘记把车位加回去了
        self.available_space[cur_spot.lot_type].append(cur_spot)
        return fee
    


class TestParkingLot(unittest.TestCase):
    def setUp(self):
        # 初始化一个有 1 个中车位的停车场
        self.parking_lot = ParkingLot(1, 1, 1)

    def test_successful_park_and_leave(self):
        # 测试正常停车和离场
        self.assertTrue(self.parking_lot.park("TEST123", VehicleTypes.CAR))
        fee = self.parking_lot.leave("TEST123")
        # 如果车辆刚刚停车离场，费用可能为 0（15 分钟内免费）
        self.assertEqual(fee, 0.0)

    def test_duplicate_vehicle(self):
        self.parking_lot.park("DUPLICATE", VehicleTypes.MOTORCYCLE)
        with self.assertRaises(DuplicateVehicleError):
            self.parking_lot.park("DUPLICATE", VehicleTypes.MOTORCYCLE)

    def test_no_available_spot(self):
        # 只有 1 个中车位，第二个应当失败
        self.parking_lot.park("CAR1", VehicleTypes.CAR)
        with self.assertRaises(NoAvailableSpotError):
            self.parking_lot.park("CAR2", VehicleTypes.CAR)

    def test_fee_calculation(self):
        # 模拟停车 30 分钟
        self.parking_lot.park("FEE123", VehicleTypes.CAR)
        spot = self.parking_lot.occupied_space["FEE123"]
        # 模拟停车 30 分钟（1800秒）
        spot.start_time = datetime.now() - timedelta(seconds=1800)
        fee = self.parking_lot.leave("FEE123")
        # 30 分钟按 0.5 小时计费，向上取整为 0.5 小时，费率为 2.5
        self.assertEqual(fee, 2.5 * 0.5)

if __name__ == '__main__':
    unittest.main()

