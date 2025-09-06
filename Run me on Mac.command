#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/source"
python3 "final points calculation.py"