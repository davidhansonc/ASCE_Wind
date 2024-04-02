import os
import subprocess
from jinja2 import Environment, FileSystemLoader

class BuildingReportGenerator:
    def __init__(self, wind_parameters, building, report_name="test"):
        self.report_name = report_name
        self.filename = f"{report_name}.tex"
        self.wind_parameters = wind_parameters
        self.building = building
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('report_template.tex')

    def prepare_data(self):
        # Prepare the data to be inserted into the LaTeX template
        data = {
            'V': self.wind_parameters.V,
            'exposure': self.wind_parameters.exposure,
            'Kh': round(self.wind_parameters.Kz, 3),
            'Kzt': self.wind_parameters.Kzt,
            'Kd': self.wind_parameters.Kd,
            'Ke': round(self.wind_parameters.Ke, 2),
            'q_h': round(self.wind_parameters.q_z, 2),
            'building_width': self.building.building_width,
            'building_length': self.building.building_length,
            'eave_height': self.building.h,
            'enclosure': self.building.enclosure,
            'flexible': self.building.flexible,
            'p_net_windward': round(self.building.p_net_windward, 2),
            'p_net_leeward': round(self.building.p_net_leeward, 2),
            'p_net_sidewall': round(self.building.p_net_sidewall, 2),
        }
        return data

    def render_template(self, data):
        return self.template.render(data)

    def write_to_file(self, content, filename):
        with open(filename, "w") as fh:
            fh.write(content)

    def compile_latex(self, filename):
        subprocess.run(['pdflatex', filename])

    def cleanup_aux_files(self, report_name, extensions=['.aux', '.log', '.out']):
        for ext in extensions:
            file_to_remove = f'{report_name}{ext}'
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

    def generate_report(self):
        data = self.prepare_data()
        output_from_parsed_template = self.render_template(data)
        self.write_to_file(output_from_parsed_template, self.filename)
        self.compile_latex(self.filename)
        self.cleanup_aux_files(self.report_name)