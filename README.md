![DevOps Pipeline](https://github.com/drishikaa09/devops-automation-pipeline/actions/workflows/pipeline.yml/badge.svg)
# devops-automation-pipeline
A DevOps pipeline I built from scratch to automate project setup and deployment.

## What it does
Give it a project name and a GitHub repo URL — it clones the repo, runs the app if it finds one, and logs everything with timestamps.

## Tech used
Bash, Docker, GitHub Actions

## Run it locally
```bash
bash pipeline.sh
```

## Run in Docker
```bash
docker build -t devops-pipeline .
docker run -it devops-pipeline
```

## Project structure
```
├── smart.sh        # sets up the environment
├── deploy.sh       # clones and runs code from GitHub  
├── pipeline.sh     # runs the full pipeline
├── Dockerfile      # containerises everything
└── .github/workflows/pipeline.yml  # CI/CD
```
