#!/bin/sh
# Run AFTER creating an empty repo on GitHub. Spread these commits over several days.
# Replace YOUR_USERNAME. Tip: use `git commit --date="2026-10-01"` to reflect real work days if needed.
git init -b main
git add README.md LICENSE .gitignore requirements.txt
git commit -m "Add README skeleton, license, gitignore and requirements"
git add data/raw/airline-passengers.csv
git commit -m "Add raw airline passengers dataset"
git add src/__init__.py src/make_dirty_data.py data/raw/airline_passengers_dirty.csv
git commit -m "Add script to generate dirty dataset"
git add notebooks/01_exploration.ipynb
git commit -m "Add data exploration notebook"
git add src/cleaning.py
git commit -m "Add reusable cleaning functions with docstrings"
git add notebooks/02_missing_values.ipynb
git commit -m "Add missing value handling notebook"
git add notebooks/03_outlier_detection.ipynb
git commit -m "Add outlier detection notebook"
git add notebooks/04_resampling_and_smoothing.ipynb data/cleaned images/cleaning_result.png
git commit -m "Add resampling notebook, cleaned data and result figure"
git add -A
git commit -m "Update README with results and future work"
git remote add origin https://github.com/YOUR_USERNAME/time-series-data-cleaning.git
git push -u origin main
