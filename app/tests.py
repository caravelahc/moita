import config
import flask
import json
import unittest

from app import moita


class MoitaTestCase(unittest.TestCase):
    def setUp(self):
        self.bucket = moita.s3.create_bucket('matrufsc_test')

        app = moita.create_app(**{
            'APPLICATION_ROOT': '',
            'AWS_BUCKET_NAME': 'matrufsc_test',
            'TESTING': True,
        })

        self.app = app.test_client()

    def test_load_invalid_timetable(self):
        result = self.app.get('/load/123')
        self.assertEqual(404, result.status_code)

    def test_load_valid_timetable(self):
        # since there is not really constraints in the data (i.e. if user
        # breaks something, it's okay to fail at the front end) we just check
        # if the endpoint correctly inserts (correct _id and data). if this
        # changes in the future this test needs to be rewritten
        payload = {
            'success': 'yes',
        }

        # this and the next assertion assert that no duplicates were inserted
        previous = len(list(self.bucket.list()))
        moita.upload(self.bucket, '123', payload)
        next = len(list(self.bucket.list()))
        self.assertEqual(previous + 1, next)

        result = self.app.get('/load/123')

        # defined by HTTP/1.1, 200 indicates request has succeeded, API follows
        self.assertEqual(200, result.status_code)

        # assert previously inserted data is unmodified
        self.assertDictEqual(payload, json.loads(result.data.decode('utf-8')))

    def test_save_timetable(self):
        # use a different _id from above!
        payload = {
            'success': 'yes',
        }

        previous = len(list(self.bucket.list()))
        result = self.app.put('/store/456', data=payload)

        # assert that request was completed and data was stored exactly once
        self.assertEqual(204, result.status_code)
        self.assertEqual(previous + 1, len(list(self.bucket.list())))

        # assert that data in the database is the same that was sent
        data = moita.download(self.bucket, '456')
        self.assertDictEqual(payload, data)

    def test_replace_timetable(self):
        payload = {
            'success': 'no',
        }

        previous = len(list(self.bucket.list()))
        self.app.put('/store/789', data=payload)
        self.assertEqual(previous + 1, len(list(self.bucket.list())))

        payload = {
            'success': 'yes'
        }
        result = self.app.put('/store/789', data=payload)
        self.assertEqual(204, result.status_code)
        self.assertEqual(previous + 1, len(list(self.bucket.list())))

        data = moita.download(self.bucket, '789')
        self.assertDictEqual(payload, data)

    def tearDown(self):
        for key in self.bucket.list():
            key.delete()
        moita.s3.delete_bucket('matrufsc_test')


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(MoitaTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()
