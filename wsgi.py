from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()

# Ensure Gunicorn can find the app object
application = app