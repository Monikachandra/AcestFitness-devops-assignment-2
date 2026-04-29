#!/bin/bash

echo "Checking Minikube status..."
minikube status >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Starting Minikube..."
    minikube start
else
    echo "Minikube is already running."
fi

echo "Pointing Docker to Minikube's internal registry..."
eval $(minikube -p minikube docker-env)

echo "Building the Docker image inside Minikube..."
docker build -t monikachandra/aceest-fitness:latest .

echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml

echo "Deployment complete! Waiting for pods to be ready..."
kubectl rollout status deployment/aceest-fitness

echo "Exposing the service..."
echo "Running 'minikube service aceest-fitness-service' to open the app..."
minikube service aceest-fitness-service
