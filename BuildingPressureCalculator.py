import pandas as pd
import numpy as np
from create_report import ReportGenerator

class BuildingPressureCalculator:
    def __init__(self, exposure, eave_height, building_width, building_length, basic_wind_speed=105, flexible="no", enclosure="enclosed", topographic_factor=1.0, ground_elevation=0):
        # Building Dimensions
        self.eave_height = eave_height #ft
        self.building_width = building_width #ft
        self.building_length = building_length #ft
        self.z_g = ground_elevation #ft

		# Velocity Pressure
        self.exposure = exposure
        self.Kh = self.velocity_pressure_coefficient(self.eave_height)
        self.Kzt = topographic_factor #modified by the TopographicCalculator class if needed.
        self.Kd = 0.85 #this is fixed for any building structure
        self.Ke = np.e**(-0.0000362 * self.z_g)
        self.V = basic_wind_speed #mph
        self.q_h = self.calculate_velocity_pressure(self.Kh)

		# Pressure on Building
        self.flexible = flexible
        self.enclosure = enclosure
        self.G = 0.85
        if self.flexible == 'yes':
            print("cannot calculate G for flexible buildings yet.")
        self.Cp_windward, self.Cp_leeward, self.sidewall = self.wall_external_pressure_coefficient(self.building_length, self.building_width)
        self.GCpi = self.internal_pressure_coefficient(enclosure)
        self.p_net_windward, self.p_net_leeward, self.p_net_sidewall = self.calculate_net_wind_pressure()


    def calculate_velocity_pressure(self, Kz):
        q = 0.00256 * Kz * self.Kzt * self.Kd * self.Ke * self.V**2
        return q


	# Need to update method for the equations in Table 26.10-1 footnotes rather than interpolating the table.
    def velocity_pressure_coefficient(self, height):
        z = height #ft
        z_g = 0
        α = 0
        
        exposure_to_params = {
            "B": (7.0, 1200),
            "C": (9.5, 900),
            "D": (11.5, 700),
        }
        
        if self.exposure in exposure_to_params:
            α, z_g = exposure_to_params[self.exposure]
        else:
            # If the exposure is not one of the expected values, raise an error
            valid_exposures = ", ".join(exposure_to_params.keys())
            raise ValueError(f"Unsupported exposure '{self.exposure}'. Valid exposures are: {valid_exposures}.")

        Kz = 2.01 * (z / z_g)**(2 / α)
        return Kz


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


    def calculate_net_wind_pressure(self):
        # Calculate wind pressure for windward wall
        p_windward = self.q_h * self.G * self.Cp_windward - self.q_h * self.GCpi

        # Calculate wind pressure for leeward wall
        p_leeward = self.q_h * self.G * self.Cp_leeward - self.q_h * self.GCpi

        # Calculate wind pressure for side wall
        p_sidewall = self.q_h * self.G * self.sidewall - self.q_h * self.GCpi

        return p_windward, p_leeward, p_sidewall