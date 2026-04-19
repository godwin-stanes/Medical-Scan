import re
from parser_generic import MedicalDocParser

class PatientDetailsParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            'patient_name': self.get_patient_name(),
            'phone_number': self.get_patient_phone_number(),
            'medical_problems': self.get_medical_problems(),
            'hepatitis_b_vaccination': self.get_hepatitis_b_vaccination()
        }

    def get_patient_name(self):
        pattern = r'Patient Information Birth Date\s+([A-Za-z]+ [A-Za-z]+)'
        matches = re.findall(pattern, self.text)
        if matches:
            return matches[0].strip()
        return None

    def get_patient_phone_number(self):
        pattern = r'\((\d{3})\)\s*(\d{3}-\d{4})'
        matches = re.findall(pattern, self.text)
        if matches:
            return f'({matches[0][0]}) {matches[0][1]}'
        return None

    def get_hepatitis_b_vaccination(self):
        pattern = r'Hepatitis B vaccination\?\s*\n+\s*(Yes|No)'
        matches = re.findall(pattern, self.text, flags=re.IGNORECASE)
        if matches:
            return matches[0].strip()
        return None

    def get_medical_problems(self):
        pattern = r'List any Medical Problems.*?\n+\s*([A-Za-z][^\n]+)'
        matches = re.findall(pattern, self.text, flags=re.IGNORECASE)
        if matches:
            return matches[0].strip()
        return None