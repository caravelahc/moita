#!/usr/bin/env python
from app import moita

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='run tests only',
                        action='store_true', dest='test', default=False)
    args = parser.parse_args()

    if args.test:
        from app import tests

        tests.run_tests()

    else:
        application = moita.create_app()
        application.run()