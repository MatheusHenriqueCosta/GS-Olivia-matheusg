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
    }

    stages {
        stage('Instalar dependências') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Setup Python VirtualEnv') {
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
                sh '~/.local/bin/pytest --cov=app --cov-report=xml'
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarAzure') {
                    sh '/opt/sonar-scanner/bin/sonar-scanner'
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

