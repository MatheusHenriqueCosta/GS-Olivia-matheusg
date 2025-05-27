pipeline {
    agent any
    environment {
        SONARQUBE = 'SonarGS' // Nome configurado no Jenkins
    }
    stages {
        stage('Preparar') {
            steps {
                sh 'pip install -r requirements.txt || true'
            }
        }
        stage('Análise com SonarQube') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    sh '/opt/sonar-scanner/bin/sonar-scanner'
                }
            }
        }
    }
}
