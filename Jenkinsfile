pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'github-creds',
                    url: 'https://github.com/alx-backend-python/alx-backend-python.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r messaging_app/requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest messaging_app/ --junitxml=test-results.xml'
            }
        }

        stage('Archive Test Results') {
            steps {
                junit 'test-results.xml'
            }
        }
    }

    triggers {
        // Manual trigger, so no SCM or schedule triggers here
    }
}

