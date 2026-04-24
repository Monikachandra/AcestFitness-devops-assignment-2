pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "monikachandra"
        IMAGE_NAME = "aceest-fitness"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        SONAR_PROJECT_KEY = "aceest-fitness"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/monikachandra/AcestFitness-devops-assignment-2.git'
            }
        }

        stage('Static Analysis (SonarQube)') {
            steps {
                script {
                    echo "Running SonarQube Analysis..."
                    // Integration with SonarQube Scanner
                    sh 'sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_AUTH_TOKEN}'
                }
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'export PYTHONPATH=$PYTHONPATH:. && pytest tests/test_app.py --junitxml=test-reports/results.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Requires docker-hub-credentials to be configured in Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes using Rolling Update Strategy..."
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl rollout status deployment/aceest-fitness"
                }
            }
        }
    }

    post {
        always {
            junit 'test-reports/*.xml'
            cleanWs()
        }
        success {
            echo "Build and Deployment Finished Successfully!"
        }
        failure {
            echo "Build Failed. Please check the logs."
        }
    }
}
