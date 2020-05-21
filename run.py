import sys

from kotidostories import create_app

if __name__ == '__main__':
    production = sys.argv[1] if len(sys.argv) == 2 else None

    app = create_app(production=production)
    app.run(host='0.0.0.0')
