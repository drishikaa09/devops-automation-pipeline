#!/bin/bash
echo "Enter Github repository URL:"
read repo
git clone "$repo"
folder=$(basename "$repo" .git)
cd "$folder" || exit
echo "Project cloned successfully!!"
if [ -f "app.py" ]; then
echo "Running Python app"
python3 app.py
else
echo "No app.py found in this project"
fi
