pipeline {
    agent any
    
    environment {
        AZURE_CREDS = credentials('azure-service-principal')
        SONAR_TOKEN = credentials('sonarqube-token')
        DOCKER_IMAGE = "youracr.azurecr.io/python-app:${BUILD_NUMBER}"
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {
        stage('Setup Python') {
            steps {
                sh """
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                """
            }
        }
        
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/MatheusHenriqueCosta/GS-Olivia-matheusg.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                pip install -r requirements.txt
                pip install pytest pytest-cov sonarqube
                """
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                pytest --cov=./ --cov-report=xml:coverage.xml -v tests/
                """
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh """
                    . ${VENV_DIR}/bin/activate
                    sonar-scanner \
                      -Dsonar.projectKey=sonarmatheus-gs \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=\${SONAR_HOST_URL} \
                      -Dsonar.login=\${SONAR_TOKEN} \
                      -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        
        stage('Push to ACR') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://youracr.azurecr.io', 'azure-acr-creds') {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }
        
        stage('Deploy to Azure App Service') {
            when {
                branch 'main'
            }
            steps {
                azureWebAppPublish(
                    azureCredentialsId: '56a06913-bcca-45f8-aa78-6aa52e0c312c',
                    resourceGroup: 'GS_olivia',
                    appName: 'sonarmatheus-gs',
                    slotName: 'production',
                    publishType: 'docker',
                    dockerImageName: DOCKER_IMAGE
                )
            }
        }
    }
    
    post {
        always {
            emailext body: 'Build ${BUILD_NUMBER} completed with status ${currentBuild.currentResult}. See details: ${BUILD_URL}',
                subject: 'Build Notification',
                to: 'rm96957@fiap.com.br'
            slackSend channel: '#devops',
                     message: "Build ${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
        }
    }
}
