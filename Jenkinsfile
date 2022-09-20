pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                pip install pipenv --upgrade
                pipenv install --system
                touch .env
            }
        }
    }
}
