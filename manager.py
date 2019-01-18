# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.models.base import db

_Author_ = 'BUPPT'

app = create_app()
# manager = Manager(app)
# Migrate(app, db)
# manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])