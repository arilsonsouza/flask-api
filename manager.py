from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from app.ext.db import db

app = create_app()
app.app_context().push()

manager = Manager(app)

@manager.command
def run():    
    app.run()

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()