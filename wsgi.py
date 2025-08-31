import os
from app import app

# The app is already created in app.py

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
