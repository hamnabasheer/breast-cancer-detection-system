from flask import *
from admin import admin
from public import public
from doctor  import doctor

from api import api

app=Flask(__name__)


app.secret_key="abcde"

app.register_blueprint(admin)
app.register_blueprint(public)
app.register_blueprint(doctor)
app.register_blueprint(api)


app.run(debug=True,port=5010,host="0.0.0.0")

