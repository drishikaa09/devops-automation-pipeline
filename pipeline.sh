#!/bin/bash
if [ -t 0 ]; then
  echo "Enter project name:"
  read project_name
  echo "Enter GitHub repository URL:"
  read repo
else
  project_name=${PROJECT_NAME:-"myproject"}
  repo=${REPO_URL:-"https://github.com/gabrieldemarmiesse/python-on-whales"}
fi
mkdir -p "$project_name"
cd "$project_name" || exit
echo "Project $project_name created at $(date)" > log.txt
git clone "$repo" || { echo "Git clone failed"; exit 1; }
folder=$(basename "$repo")
folder=${folder%.git}
cd "$folder" || exit
echo "Repository cloned at $(date)" >> ../log.txt
if [ -f "app.py" ]; then
echo "Running Python app!!!" >> ../log.txt
if command -v python3 &> /dev/null; then
    python3 app.py
else
    echo "Python not installed" >> ../log.txt
fi
else
echo "No app.py found" >> ../log.txt
fi
echo "Pipeline executed successfully!!"

