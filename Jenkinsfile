pipeline {
    agent none 
    stages {
        stage('Test') {
            agent {
                dockerfile true
            }
            steps {
                sh docker-compose -f postgres.yml up  -d
                sh 'pytest --verbose --junit-xml test-reports/results.xml'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}
