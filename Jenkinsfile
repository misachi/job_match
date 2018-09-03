node {
    checkout scm
    docker.image('postgres:10.1').withRun('-e "POSTGRES_PASSWORD=pass1234" -p 5432:5432') { c ->
        docker.image('misachi/jenkins_ubuntu_py:20180309.0.1').inside("--link ${c.id}:db -u root") {
            try {
                sh 'pytest --verbose --junit-xml test-reports/results.xml'
            } finally {
                junit 'test-reports/results.xml'
            }
        }
    }
}
