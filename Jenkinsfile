env.POSTGRES_IMG = 'postgres:10.1'
env.TEST_IMAGE = 'misachi/matcher_python:20180904'

node('master') {
    checkout scm

    stage('Build') {
        if (isUnix()) {
            docker.image(env.POSTGRES_IMG)
            docker.image(env.TEST_IMAGE)
        }
    }

    stage ('Test') {
        docker.image(env.POSTGRES_IMG).withRun('-e "POSTGRES_PASSWORD=pass1234" -p 5432:5432') { c ->
            docker.image(env.TEST_IMAGE).inside("--link ${c.id}:db -u root") {
                try {
                    sh 'pytest --verbose --junit-xml test-reports/results.xml'
                } finally {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }

    stage ('Deliver') {
        echo 'Delivered'
    }
}