# ACEest Fitness & Gym DevOps Assignment

A small Flask REST application prepared for the BITS Pilani Introduction to DevOps assignment. It demonstrates Git/GitHub version control, Pytest, Docker, GitHub Actions, and a Jenkins BUILD quality gate.

## Features

- Service health endpoint
- Fitness program catalogue
- Create, retrieve, and delete clients
- Input validation and appropriate HTTP status codes
- Automated Pytest suite
- Non-root Docker container

## Project structure

```text
.
├── .github/workflows/main.yml
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.11+
- Git
- Docker Desktop
- Optional: Jenkins with Git and Pipeline plugins, and access to the Docker CLI

## Local setup on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000/` and `http://localhost:5000/health`.

## Run tests manually

```powershell
pytest -v
```

## Docker

```powershell
docker build -t aceest-fitness:1.0 .
docker run --rm -p 5000:5000 --name aceest-app aceest-fitness:1.0
```

In another terminal:

```powershell
docker run --rm aceest-fitness:1.0 pytest -q
```

Stop the web container with `Ctrl+C`.

## API examples

```powershell
curl.exe http://localhost:5000/programs
curl.exe -X POST http://localhost:5000/clients -H "Content-Type: application/json" -d '{"name":"Devi","goal":"beginner"}'
curl.exe http://localhost:5000/clients/Devi
```

Supported goals are `beginner`, `fat-loss`, and `muscle-gain`.

## Git and GitHub submission workflow

```powershell
git init
git branch -M main
git add app.py requirements.txt test_app.py .gitignore
git commit -m "feat: add ACEest Flask API and unit tests"
git add Dockerfile .dockerignore
git commit -m "build: containerize ACEest application"
git add .github/workflows/main.yml Jenkinsfile README.md
git commit -m "ci: add GitHub Actions and Jenkins pipelines"
git remote add origin https://github.com/YOUR_USERNAME/aceest-devops-assignment.git
git push -u origin main
```

Create the empty **public** GitHub repository before adding the remote. Do not initialize it with a README because this project already contains one.

Recommended branch demonstration:

```powershell
git switch -c feature/health-endpoint
# make a small documented change
git add .
git commit -m "feat: improve health endpoint"
git push -u origin feature/health-endpoint
```

Then open a pull request into `main`, wait for ACEest CI to pass, and merge it.

## GitHub Actions logic

`.github/workflows/main.yml` runs on pushes and pull requests. It checks out the repository, configures Python 3.11, installs dependencies, checks Python syntax, builds the Docker image, and executes Pytest inside that image.

## Jenkins BUILD setup

1. Install Jenkins and the Git and Pipeline plugins.
2. Ensure the Jenkins agent can run `python3` and `docker`; add the Jenkins service account to the Docker group where applicable, then restart Jenkins.
3. Select **New Item**, enter `ACEest-Build`, choose **Pipeline**, and select **OK**.
4. Under **Build Triggers**, choose **GitHub hook trigger for GITScm polling** if a webhook is available. Otherwise use **Poll SCM** with `H/5 * * * *` for demonstration.
5. Under **Pipeline**, select **Pipeline script from SCM**.
6. Select **Git**, add the public GitHub repository URL, set the branch to `*/main`, and set Script Path to `Jenkinsfile`.
7. Save and select **Build Now**. The expected stages are Checkout, Build and Lint, Docker Build, and Test in Docker.

For automatic public GitHub webhook triggering, set the GitHub repository webhook payload URL to `http://YOUR_JENKINS_URL/github-webhook/` and select push events. The Jenkins URL must be reachable by GitHub.

## Evidence and submission checklist

- Public GitHub repository URL
- Repository file list screenshot
- Meaningful Git commit history screenshot
- Successful GitHub Actions workflow screenshot showing all steps
- Successful Jenkins build screenshot showing all stages
- Local `pytest -v` output screenshot
- Docker build output screenshot
- Running application or `/health` response screenshot

Submit the repository link in the assignment portal. Keep screenshots in a separate submission document only if the portal asks for evidence; they do not need to be committed unless instructed.

## Important note

The supplied `Aceestver-3.2.4.py` is a Tkinter desktop application. The assignment explicitly requires a Flask application and containerized CI testing, so this submission preserves the ACEest fitness domain while converting it into a testable Flask REST service.
