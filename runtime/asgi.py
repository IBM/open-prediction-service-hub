import logging
import sys
from pathlib import Path

from dynamic_hosting import app

# For debug
if __name__ == "__main__":
    import uvicorn

    storage: Path = Path(__file__).resolve().parent.joinpath('storage')

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='debug', debug=True)
