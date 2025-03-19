# PySpark ACK Template Repository

## Overview
This repository serves as a **template repository** for deploying and running **PySpark jobs on Alibaba Cloud Kubernetes (ACK)**. It includes a **structured project setup**, **CI/CD pipelines**, **SonarQube integration**, and **Poetry-based dependency management**.

## Features
✅ **Pre-configured PySpark Job**: Reads from and writes to OSS (Alibaba Object Storage Service).  
✅ **Helm & Kubernetes Integration**: Deploys Spark jobs seamlessly on ACK.  
✅ **CI/CD via GitHub Actions**: Automates linting, testing, building, and deploying Spark jobs.  
✅ **SonarQube Code Quality Checks**: Ensures code coverage and quality gate checks.  
✅ **Poetry for Dependency Management**: Manages Python dependencies efficiently.  
✅ **Pre-commit Hooks**: Ensures code formatting, linting, and security scans before commits.

## Getting Started

### Prerequisites
- Python 3.10
- Poetry (Dependency Management)
- Docker
- Alibaba Cloud CLI (For Deployment)
- Kubernetes (ACK Cluster)

### **Using This Template Repository**
In order to use this as a **GitHub template repository**, you have to select ** Use this template **. Make sure to replace occurrences of `pyspark-template-repo` with your **custom repository name**.

To automate renaming, you can run the following command if you are using MacOS:
``` 
$ find . -type f \( -name "*.yaml" -o -name "*.toml" -o -name "*.md" \) -exec sed -i '' "s/pyspark-template/YOUR_PROJECT_NAME/g" {} +
```

### **Installation**

Install dependencies using Poetry:
```bash
$ poetry install
```

### **Running Tests & Linting**
Run **pytest** for unit tests and coverage:
```bash
$ poetry run pytest --cov=spark_jobs --cov-report=xml
```
Run **linting and formatting checks**:
```bash
$ poetry run black --check .
$ poetry run isort --check-only .
$ poetry run flake8 .
```

### **Building & Running the Spark Job**
Build the Docker image:
```bash
$ docker build -t pyspark-template-job .
```
Run the Spark job locally:
```bash
$ docker run --rm pyspark-template-job python spark_jobs/example_spark_job.py --input oss://your-bucket/input --output oss://your-bucket/output
```

### **CI/CD Pipeline**
GitHub Actions automates:
- **Code Linting & Formatting**
- **Unit Tests & Coverage Checks**
- **Building & Pushing Docker Images**
- **Deploying to ACK**

Triggers:
- **On push to `main`** (Deployment happens)
- **On pull request** (Validation only, no deployment)

### **SonarQube Integration**
SonarQube performs **static code analysis** and **enforces quality gates**.
To manually trigger SonarQube analysis:
```bash
$ sonar-scanner -Dsonar.projectKey=your_project -Dsonar.sources=./spark_jobs -Dsonar.tests=./spark_jobs/tests -Dsonar.python.coverage.reportPaths=coverage.xml
```

---
💡 _This repository is designed as a GitHub template repo. Click `Use this template` to create your own customized PySpark project._ 🚀
