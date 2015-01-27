#!/usr/bin/env python
import argparse

from app import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='run tests only',
                        action='store_true', dest='test', default=False)
    args = parser.parse_args()

    if args.test:
        from app import tests

        tests.run_tests()

    else:
        app.run()