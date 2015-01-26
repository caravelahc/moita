import unittest
from app import moita

class MoitaTestCase(unittest.TestCase):
    def setUp(self):
        moita.timetables = moita.database.timetables_temporary
        moita.app.config['TESTING'] = True
        self.app = moita.app.test_client()

    def test_load_invalid_timetable(self):
        result = self.app.get('/load/123')
        assert result.status_code == 404

    def tearDown(self):
        moita.timetables.drop()

def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(MoitaTestCase)
    runner.run(suite)

if __name__ == '__main__':
    run_tests()