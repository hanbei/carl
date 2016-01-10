import os

from carl import app

port = int(os.environ.get('PORT', 5000))
app.run(debug=True, port=port, host='0.0.0.0')
