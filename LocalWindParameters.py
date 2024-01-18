class LocalWindParameters:
    def __init__(self, basic_wind_speed, directionality_factor, exposure, ground_elevation_factor, \
                 velocity_pressure, gust_effect_factor, enclosure):
        self.basic_wind_speed = basic_wind_speed
        self.directionality_factor = directionality_factor
        self.exposure = exposure
        self.ground_elevation_factor = ground_elevation_factor
        self.velocity_pressure = velocity_pressure
        self.gust_effect_factor = gust_effect_factor
        self.enclosure_coefficient = self.internal_pressure_coefficient(enclosure)


    def internal_pressure_coefficient(self, enclosure):
        coeff = 0
        if enclosure == "enclosed":
            coeff = 0.18
        elif enclosure == "partially enclosed":
            coeff = 0.55
        elif enclosure == "partially open":
            coeff = 0.18
        elif enclosure == "open":
            coeff = 0
        else:
            print("Invalid enclosure entry!")
        internal_pressure_coefficient = coeff

        return internal_pressure_coefficient