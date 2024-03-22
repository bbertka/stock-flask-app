To set up your K3s cluster for the GitLab pipeline, you will need to follow a series of steps to ensure the cluster is ready for deployments. This guide will take you through preparing your K3s cluster, assuming you have the necessary Kubernetes YAML files (`sa-token-secret.yml`, `role.yml`, `rolebinding.yml`) and that you're starting with a basic K3s installation.

### Preparing Your K3s Cluster for GitLab CI/CD

#### Step 1: Create the Namespace

First, create the namespace where your application and related Kubernetes resources will reside. If you're using a namespace named `dev01`, you can create it with the following command:

```shell
kubectl create namespace dev01
```

#### Step 2: Apply the Role

The `role.yml` file defines permissions within the `dev01` namespace. Apply this file to create the Role.

```shell
kubectl apply -f role.yml
```

This Role should grant permissions for operations on resources like deployments, replicasets, and services, which are necessary for your CI/CD pipeline to deploy your application.

#### Step 3: Apply the RoleBinding

The `rolebinding.yml` file associates the Role you just created with a service account. Apply this file to create the RoleBinding.

```shell
kubectl apply -f rolebinding.yml
```

This RoleBinding will ensure that the service account has the permissions defined in the Role within the `dev01` namespace.

#### Step 4: Create the Service Account

Before applying `sa-token-secret.yml`, ensure the service account named `gitlab-deployer` is created, as this account will be used by GitLab CI/CD to interact with your K3s cluster.

```shell
kubectl create serviceaccount gitlab-deployer -n dev01
```

#### Step 5: Apply the Service Account Token Secret

The `sa-token-secret.yml` file should contain the configuration for a secret that stores a token for the `gitlab-deployer` service account. This token is used for authentication by GitLab CI/CD.

```shell
kubectl apply -f sa-token-secret.yml
```

Make sure the secret is correctly linked to the service account by checking the service account's secrets.

```shell
kubectl get serviceaccount gitlab-deployer -n dev01 -o yaml
```

#### Step 6: Retrieve the Service Account Token

Extract and decode the service account token for use in your GitLab CI/CD pipeline settings.

```shell
SECRET_NAME=$(kubectl get serviceaccount gitlab-deployer -n dev01 -o jsonpath='{.secrets[0].name}')
kubectl get secret $SECRET_NAME -n dev01 -o jsonpath='{.data.token}' | base64 --decode
```

#### Step 7: Configure GitLab CI/CD Variables

In your GitLab project, navigate to **Settings** > **CI / CD** > **Variables** and configure the following variables:

- `KUBE_URL`: Your K3s cluster API endpoint.
- `KUBE_TOKEN`: The service account token retrieved in the previous step.
- `KUBE_NAMESPACE`: `dev01` (or your chosen namespace).


### Conclusion

Following these steps prepares your K3s cluster for continuous integration and deployment with GitLab CI/CD. It ensures that your cluster is configured with the necessary roles, permissions, and service account for GitLab to deploy your applications successfully.
