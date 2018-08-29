node {
    docker.image('postgres:10.1').withRun('-e "POSTGRES_PASSWORD=pass1234" -p 5432:5432') { c ->
        docker.image('python:2').inside("--link ${c.id}:db") {
            try {
                sh 'pip install -r requirements.txt'
                sh 'pytest --verbose --junit-xml test-reports/results.xml'
            } finally {
                junit 'test-reports/results.xml'
            }
        }
    }
}
