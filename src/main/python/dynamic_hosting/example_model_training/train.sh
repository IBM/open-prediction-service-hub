#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

find "${DIR}" -name '[!_]*.py' -exec python3 {} \;
