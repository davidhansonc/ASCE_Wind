class MonoslopeRoof:
    def __init__(self, roof_slope, eave_height, parapet_height, parapet_enclosure):
        self.roof_slope = roof_slope
        self.eave_height = eave_height
        self.parapet_height = parapet_height
        self.parapet_enclosure = parapet_enclosure


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


class Building:
    def __init__(self, building_name, roof_type, roof_slope, eave_height, parapet_height, \
                 parapet_enclosure):
        if roof_type == 'monoslope':
            MonoslopeRoof.__init__(self, roof_slope, eave_height, parapet_height, parapet_enclosure)
        elif roof_type == 'gabled':
            GabledRoof.__init__(self, roof_slope, eave_height, parapet_height, parapet_enclosure)
        else:
            raise ValueError("Invalid roof type. Expected 'monoslope' or 'gabled'.")
        self.building_name = building_name