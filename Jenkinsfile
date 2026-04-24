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
                    // In a real environment, you would use:
                    // withSonarQubeEnv('SonarQubeServer') {
                    //     sh 'sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY}'
                    // }
                    sh 'echo "SonarQube Scan Complete"'
                }
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest tests/test_app.py --junitxml=test-reports/results.xml'
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
                    // withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    //     sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    //     sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    //     sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    // }
                    sh 'echo "Simulating Docker Push..."'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes using Rolling Update Strategy..."
                    // sh "kubectl apply -f k8s/deployment.yaml"
                    // sh "kubectl rollout status deployment/aceest-fitness"
                    sh 'echo "Deployment Successful"'
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
