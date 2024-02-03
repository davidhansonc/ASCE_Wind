import numpy as np

class WindParameters:
    def __init__(self, basic_wind_speed, exposure, eave_height, ground_elevation=0, directionality_factor=0.85, topographic_factor=1.0):
        self.exposure = exposure
        self.α, self.z_g = self._terrain_exposure()
        self.V = basic_wind_speed #mph
        self.Kzt = topographic_factor
        self.Kd = directionality_factor #0.85 for building structures
        self.Ke = np.e**(-0.0000362 * self.z_g)
        self.Kz = self.velocity_pressure_coefficient(eave_height)
        self.q_z = 0.00256 * self.Kz * self.Kzt * self.Kd * self.Ke * self.V**2
		  

    def velocity_pressure_coefficient(self, eave_height):
        z = eave_height
        Kz = 2.01 * (z / self.z_g)**(2 / self.α)
        return Kz
			

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