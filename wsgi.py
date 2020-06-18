from application import create_app


def main():
    app = create_app()
    app.run(port=5050)


if __name__ == "__main__":
    main()