import numpy as np

class WindParameters:
    def __init__(self, basic_wind_speed, exposure, eave_height, ground_elevation=0, \
                 directionality_factor=0.85, topographic_factor=1.0):
        self.exposure = exposure
        self.z_elev = ground_elevation #ft
        self.z = eave_height #ft
        self.α, self.z_g = self._terrain_exposure()
        self.V = basic_wind_speed #mph
        self.Kzt = topographic_factor
        self.Kd = directionality_factor #0.85 for building structures
        self.Ke = self.elevation_factor()
        self.Kz = self.velocity_pressure_coefficient()
        self.q_z = self.calculate_velocity_pressure()
		  

    def velocity_pressure_coefficient(self):
        Kz = 2.01 * (self.z / self.z_g)**(2 / self.α)
        return Kz

    
    def elevation_factor(self):
        Ke = np.e**(-0.0000362 * self.z_elev)
        return Ke
			

    def _terrain_exposure(self):
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
		
        return α, z_g

    
    def calculate_velocity_pressure(self):
        q = 0.00256 * self.Kz * self.Kzt * self.Kd * self.Ke * self.V**2
        return q