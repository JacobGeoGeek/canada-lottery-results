from enum import Enum


class Region(str, Enum):
    """Enum of Regions for the lotto max"""
    ATLANTIC = "atlantic"
    BRITISH_COLUMBIA = "britishColumbia"
    ONTARIO = "ontario"
    QUEBEC = "quebec"
    WESTERN_CANADA = "westernCanada"
