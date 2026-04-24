# 🚀 DevOps Automation Pipeline

A modular, containerized DevOps pipeline that automates application setup, testing, and deployment with built-in failure handling and rollback mechanisms.

---

## ⚙️ Tech Stack
Bash • Docker • GitHub Actions • Linux

---

## 🔧 What it does
- Clones a GitHub repository dynamically  
- Sets up the environment automatically  
- Builds and runs the application inside a container  
- Executes automated tests using Bats  
- Implements fail-fast error handling and rollback on failure  
- Logs all pipeline steps with structured timestamps  
- Runs as a CI/CD workflow using GitHub Actions  

---

## 🏗️ Pipeline Flow
Input → Clone → Setup → Build → Test → Deploy  
↓  
Logs + Error Handling + Rollback  

---

## ▶️ Run Locally
```bash
bash pipeline.sh
```
## 🐳 Run With Docker
```
docker build -t devops-pipeline .
docker run -it devops-pipeline
```
