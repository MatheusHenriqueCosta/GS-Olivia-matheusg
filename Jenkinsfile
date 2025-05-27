pipeline {
    agent any
    
    environment {
        // Variáveis do Azure (pode ser do SonarQube ou Jenkins)
        AZURE_CLIENT_ID = credentials('azure-client-id')
        AZURE_CLIENT_SECRET = credentials('azure-client-secret')
        AZURE_TENANT_ID = credentials('azure-tenant-id')
        
        // Configurações do App Service
        APP_NAME = "sonarmatheus-gs"
        RESOURCE_GROUP = "GS_olivia"
        PYTHON_VERSION = "3.9"
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
                pip install pytest pytest-cov
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
                      -Dsonar.projectKey=python-app \
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
        
        stage('Deploy to Azure App Service') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // 1. Fazer login no Azure
                    sh """
                    az login --service-principal \
                      -u ${AZURE_CLIENT_ID} \
                      -p ${AZURE_CLIENT_SECRET} \
                      --tenant ${AZURE_TENANT_ID}
                    """
                    
                    // 2. Configurar o ambiente do App Service
                    sh """
                    az webapp config appsettings set \
                      --name ${APP_NAME} \
                      --resource-group ${RESOURCE_GROUP} \
                      --settings \
                        WEBSITE_RUN_FROM_PACKAGE=1 \
                        PYTHON_VERSION=${PYTHON_VERSION}
                    """
                    
                    // 3. Criar o pacote de deploy
                    sh """
                    . ${VENV_DIR}/bin/activate
                    pip freeze > requirements.txt
                    zip -r deploy.zip . -x '*.git*' -x '*tests*' -x '*venv*'
                    """
                    
                    // 4. Fazer deploy via ZIP
                    sh """
                    az webapp deployment source config-zip \
                      --name ${APP_NAME} \
                      --resource-group ${RESOURCE_GROUP} \
                      --src deploy.zip
                    """
                }
            }
        }
    }
    
    post {
        always {
            emailext body: 'Build ${BUILD_NUMBER} completed with status ${currentBuild.currentResult}. App URL: https://${APP_NAME}.azurewebsites.net',
                subject: 'Build Notification',
                to: 'rm96957@fiap.com.br'
            slackSend channel: '#devops',
                     message: "Deploy concluído: https://${APP_NAME}.azurewebsites.net"
        }
    }
}
