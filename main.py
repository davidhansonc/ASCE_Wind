from WindParameters import WindParameters
from Building.BuildingPressureCalculator import BuildingPressureCalculator
from Building.RoofPressureCalculator import RoofPressureCalculator
from BuildingReportGenerator import BuildingReportGenerator

basic_wind_speed = 105
exposure = "B"
eave_height = 15
ground_elevation = 0
directionality_factor = 0.85
topographic_factor = 1.0

wind_parameters = WindParameters(basic_wind_speed, exposure, eave_height)

building_length = 10
building_width = 8
enclosure = "enclosed"
flexible = "no"

building = BuildingPressureCalculator(wind_parameters.q_z, wind_parameters.z, building_width, \
									  building_length, flexible, enclosure)

roof_type = "monoslope"
roof_slope = 4

# roof_calculator = RoofPressureCalculator(roof_type, roof_slope)

report = BuildingReportGenerator(wind_parameters, building)
report.generate_report()