import os
import subprocess
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    def __init__(self, calculator):
        self.calculator = calculator
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('report_template.tex')

    def prepare_data(self):
        return {
            'exposure': self.calculator.exposure,
            'eave_height': self.calculator.eave_height,
            'building_width': self.calculator.building_width,
            'building_length': self.calculator.building_length,
            'basic_wind_speed': self.calculator.V,
            'flexible': self.calculator.flexible,
            'enclosure': self.calculator.enclosure,
            'Kz': self.calculator.Kz,
            'p_net_windward': self.calculator.p_net_windward,
            'p_net_leeward': self.calculator.p_net_leeward,
            'p_net_sidewall': self.calculator.p_net_sidewall,
        }

    def render_template(self, data):
        return self.template.render(data)

    def write_to_file(self, content, filename="report.tex"):
        with open(filename, "w") as fh:
            fh.write(content)

    def compile_latex(self, filename="report.tex"):
        subprocess.run(['pdflatex', filename])

    def cleanup_aux_files(self, extensions=['.aux', '.log', '.out']):
        for ext in extensions:
            file_to_remove = f'report{ext}'
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

    def generate_report(self):
        data = self.prepare_data()
        output_from_parsed_template = self.render_template(data)
        self.write_to_file(output_from_parsed_template)
        self.compile_latex()
        self.cleanup_aux_files()