from app import create_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import User, Role, Todo

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Todo': Todo}

if __name__ == '__main__':
    app.run()
