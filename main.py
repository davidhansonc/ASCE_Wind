from WindParameters import WindParameters
from BuildingPressureCalculator import BuildingPressureCalculator
from RoofPressureCalculator import RoofPressureCalculator

basic_wind_speed = 105
exposure = "B"
eave_height = 15
ground_elevation = 0
directionality_factor = 0.85
topographic_factor = 1.0

wind_location = WindParameters(basic_wind_speed, exposure, eave_height)

building_length = 10
building_width = 8
enclosure = "enclosed"
flexible = "no"

building = BuildingPressureCalculator()

roof_type = "monoslope"
roof_slope = 4

roof_calculator = RoofPressureCalculator(roof_type, roof_slope)