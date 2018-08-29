pipeline {
    agent none 
    stages {
        stage('Test') {
            agent {
                dockerfile true
            }
            steps {
                sh 'service postgres start'
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
