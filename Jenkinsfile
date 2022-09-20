pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                $ (sudo) pip install pipenv --upgrade
                $ (sudo) pipenv install --system
                $ (sudo) touch .env
            }
        }
    }
}
