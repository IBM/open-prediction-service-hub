#!/usr/bin/env python3

from dynamic_hosting import app

# For debug
if __name__ == "__main__":
    import os
    from pathlib import Path

    import uvicorn

    os.environ['model_storage'] = str(Path(__file__).resolve().parent.joinpath('storage'))

    uvicorn.run(app, host='127.0.0.1', port=8080, log_level='debug', debug=True)
