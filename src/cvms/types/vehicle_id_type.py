from enum import Enum


class VehicleIdType(str, Enum):
    vehicleId = "vehicleId"
    unitNumber = "unitNumber"
    quoteNumber = "quoteNumber"
    vin = "vin"
