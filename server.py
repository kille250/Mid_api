from application import create_app
from loginmanager import create_loginmanager
from database import create_database


def main():
    app = create_app()
    create_database(app)
    create_loginmanager(app)
    app.run(host=app.config['IP'], port=app.config['PORT'])


if __name__ == "__main__":
    main()
