# Stock Flask App Deployment Guide

This guide outlines the steps to deploy the Stock Flask App using GitLab CI/CD pipelines to a Kubernetes cluster managed by k3s.

## Prerequisites

- A GitLab account and a GitLab Runner with Docker executor configured.
- A Kubernetes cluster (k3s) with `kubectl` configured to interact with it.
- Docker installed for building and pushing the Docker image.

## Setup Steps

### 1. Kubernetes (k3s) Configuration

Apply the k3s configurations to create the necessary roles and service account for the GitLab Runner:

```bash
kubectl apply -f k3s/role.yml
kubectl apply -f k3s/rolebinding.yml
kubectl apply -f k3s/sa-token-secret.yml
```

### 2. GitLab CI/CD Configuration

Set up CI/CD Variables in your GitLab project's **Settings > CI / CD > Variables**:

- `KUBE_URL`: The API endpoint of your k3s cluster.
- `KUBE_TOKEN`: The token from `sa-token-secret.yml`.
- `KUBE_NAMESPACE`: The namespace where the app will be deployed.

Ensure the `.gitlab-ci.yml` file includes steps for building the Docker image, pushing it to a registry, and applying the Kubernetes `deployment.yml`.

### 3. Deployment

Triggering the pipeline in GitLab will start the CI/CD process, deploying the app to your Kubernetes cluster.

## Obtaining the Service IP or Hostname

After deployment, determine how your app is exposed:

```bash
# For LoadBalancer service
kubectl get svc -n $KUBE_NAMESPACE -o wide

# For NodePort service
kubectl get nodes -o wide
```

Use the external IP or node's IP along with the port to access your app.

## Running the Application

Navigate to the following URL, replacing `EXTERNAL_IP` with the obtained IP address:

```
http://EXTERNAL_IP/stock-price?symbol=AAPL
```

### Expected Response

The application will return a JSON response with the current stock price for the queried symbol.

## Troubleshooting

Ensure the Kubernetes service for the Flask app is correctly configured and exposed. For detailed logs, inspect the pod logs within your Kubernetes cluster:

```bash
kubectl logs <pod-name> -n $KUBE_NAMESPACE
```

