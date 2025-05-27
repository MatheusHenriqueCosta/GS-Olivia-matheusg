pipeline {
  agent any

  environment {
    SONARQUBE = 'sonarmatheus-gs' // nome configurado no Jenkins
    AZURE_APP_NAME = 'sonarmatheus-gs'
    RESOURCE_GROUP = 'GS_olivia'
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/MatheusHenriqueCosta/GS-Olivia-matheusg.git'
      }
    }

    stage('Build') {
      steps {
        sh 'mvn clean package'
      }
    }

    stage('Testes') {
      steps {
        sh 'mvn test'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv("${SONARQUBE}") {
          sh 'mvn sonar:sonar'
        }
      }
    }

    stage('Deploy to Azure') {
      steps {
        sh """
        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
        az webapp deploy --resource-group $RESOURCE_GROUP --name $AZURE_APP_NAME --src-path target/*.jar
        """
      }
    }
  }
}
}
