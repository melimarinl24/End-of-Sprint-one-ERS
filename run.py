"""
Safer runner for local development. Reads FLASK_DEBUG and binds to localhost.
Usage: python run.py
"""
import os
from project import create_app
import logging

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    # configure basic file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    app.logger.info('Starting app (debug=%s)', debug)
    app.run(debug=debug, host='127.0.0.1')
