# CI/CD Pipeline for Dockerized Flask Application

This project demonstrates a full CI/CD pipeline using **GitHub Actions**, **Docker**, and **DockerHub**.

## Pipeline Overview
- Code pushed to GitHub triggers CI pipeline
- CI pipeline builds, tests, and Dockerizes the app
- CD pipeline pushes image to DockerHub

## Technologies Used
- Flask, Redis, PostgreSQL
- Docker, Docker Compose
- GitHub Actions, DockerHub

## CI/CD Workflow
```bash
GitHub Push → GitHub Actions → Docker Build/Test → DockerHub Push → Deployment
```
