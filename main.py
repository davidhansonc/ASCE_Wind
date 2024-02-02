from BuildingPressureCalculator import BuildingPressureCalculator
from RoofPressureCalculator import RoofPressureCalculator

calculator = BuildingPressureCalculator(exposure='C', eave_height=15, building_length=10, building_width=10)

# Example instantiation and usage
roof_calculator = RoofPressureCalculator(roof_slope=30, exposure='B', eave_height=10, building_width=20, building_length=30)
print(roof_calculator.calculate_roof_load())


report_generator = ReportGenerator(calculator)
report_generator.generate_report()