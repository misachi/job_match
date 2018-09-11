env.TEST_IMAGE = 'misachi/matcher_python:20180904'
env.POSTGRES_IMG = 'postgres:10.1'

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
                if (env.BRANCH_NAME == 'master') {
                    try {
                        sh 'pytest --verbose --junit-xml test-reports/results.xml'
                        currentBuild.result = 'SUCCESS'
                    catch (Exception err) {
                        currentBuild.result = 'FAILURE'
                    }

                    if (currentBuild.result == 'SUCCESS') {
                        echo 'Successful'
                        junit 'test-reports/results.xml'
                    } else if (currentBuild.result == 'FAILURE') {
                        echo 'Failure'
                    } else {
                        echo 'Not testable'
                    }
                } else {
                    echo 'Not to be tested'
                }
            }
        }
    }

    stage ('Deliver') {
        echo 'Delivered'
    }
}