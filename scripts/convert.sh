#!/bin/bash

jupyter nbconvert ../notebooks/src/*.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags sl --to notebook --output-dir='../notebooks/en'
jupyter nbconvert ../notebooks/src/*.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags en --to notebook --output-dir='../notebooks/sl' 