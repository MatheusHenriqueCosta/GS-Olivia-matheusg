// Descrição: Pipeline para rodar testes com cobertura e análise de código com SonarQube
// pipeline {
//     agent any
//     environment {
//         SONARQUBE = 'SonarGS' // Nome configurado no Jenkins

//     }
//     stages {
//         stage('Instalar dependências') {
//             steps {
//                 sh 'pip install -r requirements.txt'
//             }
//         }
//         stage('Rodar testes com cobertura') {
//             steps {
//                 sh 'pytest --cov=app --cov-report=xml'
//             }
//         }
//         stage('Análise com SonarQube') {
//             steps {
//                 withSonarQubeEnv("${SONARQUBE}") {
//                     sh '/opt/sonar-scanner/bin/sonar-scanner'
//                 }
//             }
//         }
//     }
// }
pipeline {
    agent any

    environment {
        AZURE_APP_NAME = "meu-app-python"
        AZURE_RG = "GS_olivia"
        AZURE_CREDENTIALS_ID = "azure-sp"
        AZURE_TENANT_ID = "11dbbfe2-89b8-4549-be10-cec364e59551"
        SONARQUBE_SERVER = "SonarGS"  // Nome da configuração do servidor no Jenkins
        SONAR_PROJECT_KEY = "meu-app-python"
        COVERAGE_REPORT_PATH = "coverage.xml"
    }

    stages {
        stage('Preparar ambiente Python') {
            steps {
            sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }


        stage('Testes e cobertura') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH=$(pwd)
                    pytest --cov=app --cov-report=xml
                '''
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    // Executa o SonarQube Scanner
                    sh '''
                        . venv/bin/activate
                        /opt/sonar-scanner/bin/sonar-scanner \
                          -Dsonar.projectKey=meu-app-python \
                          -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                          -Dsonar.sources=app \
                          -Dsonar.host.url=${SONAR_HOST_URL} \
                          -Dsonar.login=${SONAR_AUTH_TOKEN} \
                          -Dsonar.python.coverage.reportPaths=${COVERAGE_REPORT_PATH} \
                            -Dsonar.python.version=3 \
                            -Dsonar.verbose=true \
                    '''
                }
            }
        }

        stage('Login no Azure') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${AZURE_CREDENTIALS_ID}", usernameVariable: 'AZURE_APP_ID', passwordVariable: 'AZURE_PASSWORD')]) {
                    sh '''
                        az login --service-principal -u $AZURE_APP_ID -p $AZURE_PASSWORD --tenant 11dbbfe2-89b8-4549-be10-cec364e59551
                    '''
                }
            }
        }

        stage('Deploy App') {
            steps {
                sh '''
                    zip -r app.zip .
                    az webapp deployment source config-zip \
                        --resource-group $AZURE_RG \
                        --name $AZURE_APP_NAME \
                        --src app.zip
                '''
            }
        }
    }
}

