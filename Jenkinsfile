pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        stage('deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
    post {
        always {
            script {
                sh 'docker-compose down'
            }
        }
    }
}
