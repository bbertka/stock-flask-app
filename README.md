# Stock Flask App Deployment Guide

This guide outlines the steps to deploy the Stock Flask App using GitLab CI/CD pipelines to a Kubernetes cluster managed by k3s.

## Prerequisites

- A GitLab account and a GitLab Runner with Docker executor configured.
- A Kubernetes cluster (k3s) with `kubectl` configured to interact with it.
- Docker installed for building and pushing the Docker image.

## Setup Steps

### 1. Kubernetes (k3s) Configuration

First, apply the k3s configurations to create the necessary roles and service account for the GitLab Runner:

```bash
kubectl apply -f k3s/role.yml
kubectl apply -f k3s/rolebinding.yml
kubectl apply -f k3s/sa-token-secret.yml
```

Refer to the `k3s/README.md` for detailed instructions.

### 2. GitLab CI/CD Configuration

1. **Set up CI/CD Variables**: In your GitLab project, navigate to **Settings > CI / CD > Variables** and add the following:
   - `KUBE_URL`: The API endpoint of your k3s cluster.
   - `KUBE_TOKEN`: The token from `sa-token-secret.yml`.
   - `KUBE_NAMESPACE`: The namespace where the app will be deployed.

2. **GitLab CI/CD Pipeline**: The `.gitlab-ci.yml` file defines the pipeline stages for deploying the app. Ensure it includes steps for building the Docker image, pushing it to a registry, and applying the Kubernetes `deployment.yml`.

2. Change the name of the Docker image as you see fit.

### 3. Deployment

Committing changes to the repository or manually triggering the pipeline in GitLab will start the CI/CD process. The pipeline will build the Docker image, push it to a registry, and apply the `deployment.yml` to deploy the app to your Kubernetes cluster.

