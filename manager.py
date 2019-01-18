# -*- coding: utf-8 -*-
from app import create_app

_Author_ = 'BUPPT'

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])