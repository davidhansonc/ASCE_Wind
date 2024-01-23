import pandas as pd
from scipy.interpolate import interp1d
from create_report import ReportGenerator

class BuildingPressureCalculator:
    def __init__(self, exposure, eave_height, building_width, building_length, basic_wind_speed=105, flexible="no", enclosure="enclosed"):
        # Building Dimensions
        self.eave_height = eave_height #ft
        self.building_width = building_width #ft
        self.building_length = building_length #ft

		# Velocity Pressure
        self.exposure = exposure
        self.Kz = self.velocity_pressure_coefficient()
        self.Kzt = 1.0
        self.Kd = 0.85
        self.Ke = 1.0
        self.V = basic_wind_speed #mph
        self.q = self.calculate_velocity_pressure()

		# Pressure on Building
        self.flexible = flexible
        self.enclosure = enclosure
        self.G = 0.85
        if self.flexible == 'yes':
            print("cannot calculate G for flexible buildings yet.")
        self.Cp_windward, self.Cp_leeward, self.sidewall = self.wall_external_pressure_coefficient(self.building_length, self.building_width)
        self.GCpi = self.internal_pressure_coefficient(enclosure)
        self.p_net_windward, self.p_net_leeward, self.p_net_sidewall = self.calculate_net_wind_pressure()


    def calculate_velocity_pressure(self):
        q = 0.00256 * self.Kz * self.Kzt * self.Kd * self.Ke * self.V**2
        return q


    def velocity_pressure_coefficient(self):
        # Define the Kz values for different exposures and heights
        Kz_values = {
            'B': {0: 0.57, 15: 0.57, 20: 0.62, 25: 0.66, 30: 0.70, 40: 0.76, 50: 0.81, 60: 0.85, 70: 0.89, 80: 0.93, 90: 0.96, 100: 0.99, 120: 1.04, 140: 1.09, 160: 1.13, 180: 1.17, 200: 1.20, 250: 1.28, 300: 1.35, 350: 1.41, 400: 1.47, 450: 1.52, 500: 1.56},
            'C': {0: 0.85, 15: 0.85, 20: 0.90, 25: 0.94, 30: 0.98, 40: 1.04, 50: 1.09, 60: 1.13, 70: 1.17, 80: 1.21, 90: 1.24, 100: 1.26, 120: 1.31, 140: 1.36, 160: 1.39, 180: 1.43, 200: 1.46, 250: 1.53, 300: 1.59, 350: 1.64, 400: 1.69, 450: 1.73, 500: 1.77},
            'D': {0: 1.03, 15: 1.03, 20: 1.08, 25: 1.12, 30: 1.16, 40: 1.22, 50: 1.27, 60: 1.31, 70: 1.34, 80: 1.38, 90: 1.40, 100: 1.43, 120: 1.48, 140: 1.52, 160: 1.55, 180: 1.58, 200: 1.61, 250: 1.68, 300: 1.73, 350: 1.78, 400: 1.82, 450: 1.86, 500: 1.89}
        }

        # Extract the heights and corresponding Kz values for the given exposure
        heights = list(Kz_values[self.exposure].keys())
        Kz_vals = list(Kz_values[self.exposure].values())

        # Create an interpolation function
        interpolation_func = interp1d(heights, Kz_vals, kind='linear')

        # Use the interpolation function to find the Kz value for the given eave_height
        self.Kz = interpolation_func(self.eave_height)

        return self.Kz

    
    def wind_pressure_enclosed_part_enclosed(self):
        pass


    def topographic_factor(self):
        pass


    def ground_elevation_factor(self):
        pass


    def wind_directionality_factor(self):
        pass


    def wall_external_pressure_coefficient(self, L, B):
        # Wall pressure coefficients, Cp, for wall surfaces
        L_B = L / B

        # Check for invalid L/B ratio
        if L_B < 0:
            raise ValueError("L/B ratio cannot be less than 0")

        # Define the L/B ratios and corresponding Cp_leeward_wall values
        L_B_values = {1: -0.5, 2: -0.3, 4: -0.2}
        L_B_ratios = list(L_B_values.keys())
        Cp_values = list(L_B_values.values())

        # Create an interpolation function for L/B ratios between 1 and 4
        if 1 < L_B < 4:
            interpolation_func = interp1d(L_B_ratios, Cp_values, kind='linear')
            Cp_leeward_wall = float(interpolation_func(L_B))
        elif L_B <= 1:
            Cp_leeward_wall = -0.5
        elif L_B >= 4:
            Cp_leeward_wall = -0.2
        else:
            print('Invalid L/B ratio')

        Cp_windward_wall = 0.8
        Cp_sidewall = -0.7

        return Cp_windward_wall, Cp_sidewall, Cp_leeward_wall


    def internal_pressure_coefficient(self, enclosure):
        # Define the internal pressure coefficients for different enclosure types
        coefficients = {
            "enclosed": 0.18,
            "partially enclosed": 0.55,
            "partially open": 0.18,
            "open": 0
        }

        # Check if the enclosure type is valid and calculate the coefficient
        if enclosure in coefficients:
            return coefficients[enclosure]
        else:
            raise ValueError(f"Invalid enclosure type '{enclosure}'. Valid types are: {list(coefficients.keys())}")


    def enclosure_selection(self):
        pass

    def calculate_net_wind_pressure(self):
        # Calculate wind pressure for windward wall
        p_windward = self.q * self.G * self.Cp_windward - self.q * self.GCpi

        # Calculate wind pressure for leeward wall
        p_leeward = self.q * self.G * self.Cp_leeward - self.q * self.GCpi

        # Calculate wind pressure for side wall
        p_sidewall = self.q * self.G * self.sidewall - self.q * self.GCpi

        return p_windward, p_leeward, p_sidewall


# Usage
calculator = BuildingPressureCalculator(exposure='C', eave_height=15, building_length=10, building_width=10)
report_generator = ReportGenerator(calculator)
report_generator.generate_report()