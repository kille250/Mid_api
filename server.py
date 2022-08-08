from application import create_app


def main():
    app = create_app()
    app.run(host=app.config['IP'], port=app.config['PORT'])


if __name__ == "__main__":
    main()
