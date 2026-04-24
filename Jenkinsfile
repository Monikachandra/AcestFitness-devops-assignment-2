pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *') // Requirement 4: Continuously poll Git repository
    }

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
                    // Requirement 7: static code analysis
                    sh 'sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_AUTH_TOKEN}'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Requirement 5: Package into Docker image
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Unit Testing (Inside Container)') {
            steps {
                script {
                    echo "Executing tests inside the containerized environment..."
                    // Requirement 7: Execute tests inside the containerized environment
                    sh "docker run --rm ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} pytest tests/test_app.py --junitxml=test-reports/results.xml"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Requirement 5: Store in central registry
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
                    // Requirement 6: Continuous Delivery (Rolling Update is standard in deployment.yaml)
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl rollout status deployment/aceest-fitness"
                }
            }
        }

        stage('Advanced Deployments (Simulated)') {
            steps {
                script {
                    echo "Demonstrating Advanced Deployment Strategies..."
                    // Requirement 6: Blue-Green, Canary, Shadow, A/B Testing
                    sh 'echo "Applying Blue-Green Strategy..." && kubectl apply -f k8s/blue-green.yaml'
                    sh 'echo "Applying Canary Release..." && kubectl apply -f k8s/canary.yaml'
                    sh 'echo "Applying A/B Testing..." && kubectl apply -f k8s/ab-testing.yaml'
                    sh 'echo "Applying Shadow Deployment..." && kubectl apply -f k8s/shadow.yaml'
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
            script {
                echo "Build Failed. Initiating Rollback..."
                // Requirement 6: Rollback mechanisms
                sh "kubectl rollout undo deployment/aceest-fitness"
                echo "Rollback to last stable version complete."
            }
        }
    }
}
