#!/bin/bash
echo "Enter project name:"
read project_name
echo "Enter GitHub repository URL:"
read repo
mkdir -p "$project_name"
cd "$project_name" || exit
echo "Project $project_name created at $(date)" > log.txt
git clone "$repo"
folder=$(basename "$repo" .git)
cd "$folder" || exit
echo "Repository cloned at $(date)" >> ../log.txt
if [ -f "app.py" ]; then
echo "Running Python app!!!" >> ../log.txt
python3 app.py
else
echo "No app.py found" >> ../log.txt
fi
echo "Pipeline executed successfully!!"

