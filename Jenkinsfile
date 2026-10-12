pipeline {
    agent any
    options { timestamps() }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Build and Lint') {
            steps {
                sh 'python3 -m py_compile app.py test_app.py'
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t aceest-fitness:${BUILD_NUMBER} .' }
        }
        stage('Test in Docker') {
            steps { sh 'docker run --rm aceest-fitness:${BUILD_NUMBER} pytest -q' }
        }
    }
    post {
        always { sh 'docker image rm aceest-fitness:${BUILD_NUMBER} || true' }
    }
}
