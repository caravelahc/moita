import config
import json
import unittest

from app import moita


class MoitaTestCase(unittest.TestCase):
    def setUp(self):
        app = moita.create_app(**{
            'APPLICATION_ROOT': '',
            'DATABASE': '_'.join([config.DATABASE, 'temporary']),
            'TESTING': True,
        })

        self.app = app.test_client()
        self.database = moita.connection[app.config.get('DATABASE')].timetables

    def test_load_invalid_timetable(self):
        result = self.app.get('/load/123')
        self.assertEqual(404, result.status_code)

    def test_load_valid_timetable(self):
        # since there is not really constraints in the data (i.e. if user breaks
        # something, it's okay to fail at the front end) we just check if the
        # endpoint correctly inserts (correct _id and data). if this changes in
        # the future this test needs to be rewritten
        payload = {
            '_id': '123',
            'success': 'yes',
        }

        # this and the next assertion assert that no duplicates were inserted
        previous = self.database.count()
        self.database.insert(payload)
        self.assertEqual(previous + 1, self.database.count())

        result = self.app.get('/load/%s' % payload['_id'])

        # defined by HTTP/1.1, 200 indicates request has succeeded, API follows
        self.assertEqual(200, result.status_code)

        # assert previously inserted data is unmodified
        del payload['_id']  # returned data should not contain _id
        self.assertDictEqual(payload, json.loads(result.data.decode('utf-8')))

    def test_save_timetable(self):
        # use a different _id from above!
        payload = {
            'success': 'yes',
        }

        previous = self.database.count()
        result = self.app.put('/store/456', data=payload)

        # assert that request was completed and data was stored exactly once
        self.assertEqual(204, result.status_code)
        self.assertEqual(previous + 1, self.database.count())

        # assert that data in the database is the same that was sent
        data = self.database.find_one('456')
        del data['_id']
        self.assertDictEqual(payload, data)

    def test_replace_timetable(self):
        payload = {
            'success': 'no',
        }

        previous = self.database.count()
        self.app.put('/store/789', data=payload)
        self.assertEqual(previous + 1, self.database.count())

        payload = {
            'success': 'yes'
        }
        result = self.app.put('/store/789', data=payload)
        self.assertEqual(204, result.status_code)
        self.assertEqual(previous + 1, self.database.count())

        data = self.database.find_one('789')
        del data['_id']
        self.assertDictEqual(payload, data)

    def test_ping_icalendar(self):
        # the payload is a real example extracted from ramiropolla/capim and
        # it is rather big, so I opted to read it from a sample file
        with open('sample.ics', 'r') as f:
            payload = f.read()

        r = self.app.post('/ical/903', data=payload)

        # this mimetype is recommended for iCalendar
        self.assertEqual('text/calendar', r.headers['Content-Type'])
        self.assertEqual('attachment; filename=903.ics',
                         r.headers['Content-Disposition'])

        # the data comes as bytes, and needs to be decoded
        self.assertEqual(payload, r.data.decode('UTF-8'))

    def tearDown(self):
        self.database.drop()


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(MoitaTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()