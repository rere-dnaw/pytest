pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'pip install pipenv --upgrade'
                sh 'pipenv install --system'
                sh 'touch .env'
            }
        }
    }
}
