import logging
import sys

import uvicorn
from dynamic_hosting import app

# For debug
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000)
