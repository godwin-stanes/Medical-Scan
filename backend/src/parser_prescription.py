import re
from parser_generic import MedicalDocParser

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            'patient_name': self.get_field('patient_name'),
            'patient_address': self.get_field('patient_address'),
            'medicines': self.get_field('medicines'),
            'directions': self.get_field('directions'),
            'refills': self.get_field('refills')
        }

    def get_field(self, field_name):
        pattern_dict = {
            'patient_name': {'pattern': r'Name:\s*(.*?)\s*Date:', 'flags': 0},
            'patient_address': {'pattern': r'Address:\s*(.*?)\n', 'flags': 0},
            'medicines': {'pattern': r'Address:.*?\n\s*\n([A-Za-z].*?)(?:Directions:|L month|\Z)', 'flags': re.DOTALL},
            'directions': {'pattern': r'Directions:\s*(.*?)(?:Refill:|$)', 'flags': re.DOTALL},
            'refills': {'pattern': r'Refill:\s*(\d+)\s*times', 'flags': 0},
        }
        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object['pattern'], self.text, flags=pattern_object['flags'])
            if len(matches) > 0:
                return matches[0].strip()
        return None