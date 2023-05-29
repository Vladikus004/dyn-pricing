pipeline {
  agent any
  triggers {
    cron('0 0 * * *')
  }
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/Vladikus004/cicd_with_docker', branch: 'main')
      }
    }

    stage('Log') {
      steps {
        sh 'ls -la'
      }
    }

    stage('Build docker') {
      steps {
        sh 'sudo docker build -t pelanglene/test .'
      }
    }

    stage('Run docker') {
      steps {
        sh '''sudo docker run -v ~/data_from_docker:/usr/src/app/data pelanglene/test
'''
      }
    }

  }
}