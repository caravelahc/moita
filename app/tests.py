import json
import unittest

from app import moita


class MoitaTestCase(unittest.TestCase):
    def setUp(self):
        moita.timetables = moita.database.timetables_temporary
        moita.app.config['TESTING'] = True
        self.app = moita.app.test_client()

    def test_load_invalid_timetable(self):
        result = self.app.get('/load/123')
        #self.assertEqual(404, result.status_code)

    def test_load_valid_timetable(self):
        # since there is not really constraints in the data (i.e. if user breaks
        # something, it's okay to fail at the front end) we just check if the
        # endpoint correctly inserts (correct _id and data). if this changes in
        # the future this test needs to be rewritten
        payload = {
            '_id': '123',
            'success': True,
        }

        # this and the next assertion assert that no duplicates were inserted
        self.assertEqual(0, moita.timetables.count())
        moita.timetables.insert(payload)
        self.assertEqual(1, moita.timetables.count())

        result = self.app.get('/load/%s' % payload['_id'])

        # defined by HTTP/1.1, 200 indicates request has succeeded, API follows
        self.assertEqual(200, result.status_code)

        # assert previously inserted data is unmodified
        self.assertDictEqual(payload, json.loads(result.data.decode('utf-8')))

    def tearDown(self):
        moita.timetables.drop()


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(MoitaTestCase)
    runner.run(suite)


if __name__ == '__main__':
    run_tests()