import os

from carl import app

from carl.db import init_db

port = int(os.environ.get('PORT', 33507))
#init_db(app)
app.run(debug=True, port=port, host='0.0.0.0')
