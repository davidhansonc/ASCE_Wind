import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from create_report import ReportGenerator

class BuildingPressureCalculator:
    def __init__(self, velocity_pressure, eave_height, building_width, building_length, 
                 flexible="no", enclosure="enclosed",):
        # Building Dimensions
        self.z = eave_height #ft
        self.building_width = building_width #ft
        self.building_length = building_length #ft

		# Pressure on Building
        self.flexible = flexible
        self.enclosure = enclosure
        self.G = 0.85
        if self.flexible == 'yes':
            print("cannot calculate G for flexible buildings yet.")
        self.q_z = velocity_pressure #psf
        self.Cp_windward, self.Cp_leeward, self.sidewall = self.wall_external_pressure_coefficient(self.building_length, \
                                                                                                   self.building_width)
        self.GCpi = self.internal_pressure_coefficient(enclosure)
        self.p_net_windward, self.p_net_leeward, self.p_net_sidewall = self.calculate_net_wind_pressure()


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
        p_windward = self.q_z * self.G * self.Cp_windward - self.q_z * self.GCpi

        # Calculate wind pressure for leeward wall
        p_leeward = self.q_z * self.G * self.Cp_leeward - self.q_z * self.GCpi

        # Calculate wind pressure for side wall
        p_sidewall = self.q_z * self.G * self.sidewall - self.q_z * self.GCpi

        return p_windward, p_leeward, p_sidewall