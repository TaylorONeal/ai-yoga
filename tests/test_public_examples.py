"""Privacy boundaries for shipped examples, including binary workbook content."""
import csv
import json
import unittest
from pathlib import Path
from zipfile import ZipFile

import openpyxl
import yaml

ROOT = Path(__file__).resolve().parents[1]
JOURNEY = ROOT / 'skills/yoga-journey-tracker'


class PublicExamplesTest(unittest.TestCase):
    def test_practitioner_template_has_no_profile(self):
        profile = yaml.safe_load((JOURNEY / 'config/example_practitioner.yaml').read_text())
        self.assertEqual(profile['name'], 'Your Name')
        self.assertIsNone(profile['practice_start_year'])
        for key in ('pronouns', 'practice_signature', 'featured_trainings', 'in_progress_trainings', 'workshops'):
            self.assertFalse(profile[key])

    def test_sample_visits_are_explicitly_synthetic(self):
        with (JOURNEY / 'templates/sample_data.csv').open() as source:
            rows = list(csv.DictReader(source))
        self.assertEqual(len(rows), 6)
        for row in rows:
            for field in ('Teacher', 'Studio', 'City', 'Country'):
                self.assertTrue(row[field].startswith('Demo '), field)
            self.assertEqual(row['Source'], 'Synthetic fixture')
            self.assertTrue(row['Date'].startswith('2040-'))
        stats = json.loads((JOURNEY / 'examples/example_stats.json').read_text())
        self.assertEqual(stats['total_visits'], len(rows))
        self.assertIn('Entirely synthetic', stats['_description'])

    def test_workbook_has_no_practitioner_rows_or_hidden_payloads(self):
        file = JOURNEY / 'templates/yoga_visits_template.xlsx'
        workbook = openpyxl.load_workbook(file)
        for sheet in workbook:
            self.assertEqual(sheet.sheet_state, 'visible')
            if sheet.title != 'Summary':
                self.assertEqual(sheet.max_row, 1, sheet.title)
            for row in sheet:
                for cell in row:
                    self.assertIsNone(cell.comment)
                    self.assertIsNone(cell.hyperlink)
        self.assertIn(workbook.properties.creator, (None, 'openpyxl'))
        self.assertIsNone(workbook.properties.lastModifiedBy)
        with ZipFile(file) as archive:
            for name in archive.namelist():
                self.assertFalse(any(part in name for part in ('externalLinks/', 'embeddings/', 'comments', 'vbaProject')))
        workbook.close()


if __name__ == '__main__':
    unittest.main()
