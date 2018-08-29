pipeline {
    agent none 
    stages {
        stage('Test') {
            agent {
                dockerfile true
            }
            steps {
                sh 'docker run -t -d --name test_db -e POSTGRES_PASSWORD=pass1234 -p 5432:5432 postgres'
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
