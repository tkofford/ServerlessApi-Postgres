from enum import Enum


class EndpointType(str, Enum):
    customers = "customers"
    vehicles = "vehicles"
