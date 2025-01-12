#!/bin/bash
pip install -U pip setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm
