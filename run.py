import argparse

from kotidostories import create_app

environments = ['test', 'production', 'docker']
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', help="environment to choose")
    args = parser.parse_args()
    environment = None
    try:
        if args.env in environments:
            environment = args.env
    except AttributeError:
        print('err')
    app = create_app(environment=environment)
    app.run(host='0.0.0.0')
