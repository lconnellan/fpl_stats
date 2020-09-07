#!env/bin/python
from db import app

app.run(debug=False, host='0.0.0.0', port="1234")
