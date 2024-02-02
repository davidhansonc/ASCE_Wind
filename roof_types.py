class MonoslopeRoof:
    def __init__(self, roof_slope, eave_height, parapet_height, parapet_enclosure):
        self.roof_slope = roof_slope
        self.eave_height = eave_height
        self.parapet_height = parapet_height
        self.parapet_enclosure = parapet_enclosure
        self.gust_effect_factor = 0.85


class GabledRoof:
    def __init__(self, roof_slope, eave_height, parapet_height, parapet_enclosure):
        self.roof_slope = roof_slope
        self.eave_height = eave_height
        self.parapet_height = parapet_height
        self.parapet_enclosure = parapet_enclosure


class HippedRoof:
    def __init__(self, roof_slope_1, roof_slope_2, eave_height, parapet_height, parapet_enclosure):
        self.roof_slope_1 = roof_slope_1
        self.roof_slope_2 = roof_slope_2
        self.eave_height = eave_height
        self.parapet_height = parapet_height
        self.parapet_enclosure = parapet_enclosure