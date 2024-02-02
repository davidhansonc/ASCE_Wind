import os
import subprocess
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    def __init__(self, calculator):
        self.calculator = calculator
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('report_template.tex')

    def prepare_data(self):
        # Prepare the data to be inserted into the LaTeX template
        data = {
            'exposure': self.calculator.exposure,
            'eave_height': self.calculator.eave_height,
            'building_width': self.calculator.building_width,
            'building_length': self.calculator.building_length,
            'V': self.calculator.V,
            'Kh': round(self.calculator.Kh, 3),
            'Kzt': self.calculator.Kzt,
            'Kd': self.calculator.Kd,
            'Ke': round(self.calculator.Ke, 2),
            'q_h': round(self.calculator.q_h, 2),
            'flexible': self.calculator.flexible,
            'enclosure': self.calculator.enclosure,
            'p_net_windward': round(self.calculator.p_net_windward, 2),
            'p_net_leeward': round(self.calculator.p_net_leeward, 2),
            'p_net_sidewall': round(self.calculator.p_net_sidewall, 2),
        }
        return data

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