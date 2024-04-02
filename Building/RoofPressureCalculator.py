from Building.BuildingPressureCalculator import BuildingPressureCalculator

class RoofPressureCalculator(BuildingPressureCalculator):
    def __init__(self, roof_slope, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roof_slope = roof_slope
        # Initialize additional attributes for roof types
        self.roof_type = None
        self.roof_attributes_attributes = {}

    def set_roof_type(self, roof_type, **attributes):
        self.roof_type = roof_type
        # Define supported roof types and their required attributes
        supported_roof_types = {
            "monoslope": ["area", "pitch"],
            "gabled": ["ridge_height", "pitch"],
            "hipped": ["ridge_length", "pitch"],
        }

        if roof_type not in supported_roof_types:
            raise ValueError(f"Unsupported roof type '{roof_type}'. Supported types are: {list(supported_roof_types.keys())}.")

        # Check if all required attributes for the selected roof type are provided
        required_attributes = supported_roof_types[roof_type]
        missing_attributes = [attr for attr in required_attributes if attr not in attributes]
        if missing_attributes:
            raise ValueError(f"Missing required attributes for roof type '{roof_type}': {missing_attributes}.")

        # All checks passed, set the roof attributes
        self.roof_attributes = attributes

    # Example usage of the roof attributes in a method
    def calculate_roof_load(self):
        if self.roof_type == "flat":
            # Example calculation for flat roof
            load = self.roof_attributes["area"] * 0.5  # Simplified example calculation
            return load
        elif self.roof_type == "gabled":
            # Example calculation for gabled roof
            load = self.roof_attributes["ridge_height"] * self.roof_attributes["pitch"] * 0.75  # Simplified example calculation
            return load
        elif self.roof_type == "hipped":
            # Example calculation for hipped roof
            load = self.roof_attributes["ridge_length"] * self.roof_attributes["pitch"] * 0.85  # Simplified example calculation
            return load
        else:
            raise ValueError(f"Load calculation for roof type '{self.roof_type}' is not implemented.")