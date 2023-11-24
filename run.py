from src import create_app

flaskApp = create_app()

if __name__ == '__main__':
    flaskApp.run(debug=True)
