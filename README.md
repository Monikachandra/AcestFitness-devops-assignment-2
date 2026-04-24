# ACEest Fitness & Performance - DevOps Pipeline

This project establishes a robust, test-driven, and fully automated DevOps pipeline for a fitness and gym management system.

## Features
- **Flask Web App**: Modular and maintainable code representing core gym management.
- **Unit Testing**: Pytest-based automation for reliability.
- **Containerization**: Docker-ready for deployment consistency.
- **CI/CD**: Jenkins pipeline for automated build, test, and deploy.
- **Kubernetes**: Advanced deployment strategies (Canary, Blue-Green, Rolling Update).

## Getting Started

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Access at `http://localhost:5000` (Default credentials: admin/admin).

### Testing
Run automated tests with:
```bash
pytest tests/test_app.py
```

### Docker
Build the container:
```bash
docker build -t aceest-fitness .
```
Run the container:
```bash
docker run -p 5000:5000 aceest-fitness
```

### Jenkins Pipeline
The `Jenkinsfile` defines the following stages:
- **Static Analysis**: SonarQube quality gate.
- **Unit Test**: Pytest execution.
- **Build & Push**: Docker Hub image management.
- **Deploy**: Kubernetes rolling update.

### Kubernetes Deployment
Apply the manifests:
```bash
kubectl apply -f k8s/deployment.yaml
```
Explore strategies in the `k8s/` folder:
- `blue-green.yaml`: Switch traffic between versions.
- `canary.yaml`: Progressive rollout.
- `ab-testing.yaml`: Split testing.
- `shadow.yaml`: Mirror traffic for testing.

## CI/CD Architecture
The pipeline follows a standard DevOps lifecycle:
1. **Source**: GitHub repo triggers Jenkins.
2. **Build & Test**: Jenkins runs lint, tests, and static analysis.
3. **Containerize**: Docker image pushed to Docker Hub.
4. **Deploy**: Kubernetes orchestrates the rollout across multiple pods.
