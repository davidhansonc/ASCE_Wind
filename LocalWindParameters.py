class LocalWindParameters:


    def __init__(self, basic_wind_speed, directionality_factor, exposure, ground_elevation_factor, \
                 velocity_pressure, gust_effect_factor, enclosure_classification, \
                    internal_pressure_coefficient):
        self.basic_wind_speed = basic_wind_speed
        self.directionality_factor = directionality_factor
        self.exposure = exposure
        self.ground_elevation_factor = ground_elevation_factor
        self.velocity_pressure = velocity_pressure
        self.gust_effect_factor = gust_effect_factor
        self.enclosure_classification = enclosure_classification
        self.internal_pressure_coefficient = internal_pressure_coefficient