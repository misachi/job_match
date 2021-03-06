env.TEST_IMAGE = 'misachi/matcher_python:20180917.0.1'
env.POSTGRES_IMG = 'postgres:10.1'
env.THRESHOLD = '70'
env.app = "misachi/matcher:${env.BUILD_ID}"
env.db_psql = ''

node('master') {
    stage('Clone Repository') {
        checkout scm
    }

    stage('Build') {
        if (isUnix()) {
            env.db_psql = env.POSTGRES_IMG
            docker.build(env.app, ".")
        }
    }

    stage ('Test') {
        docker.image(env.db_psql).withRun('-e "POSTGRES_PASSWORD=pass1234" -p 5432:5432') { c ->
            docker.image(env.app).inside("--link ${c.id}:db -u root") {
                // if (env.BRANCH_NAME == 'master') {
                if (env.BRANCH_NAME == 'Test-Multibranch-Jenkins') {
                    try {
                        // sh 'pytest --verbose --junit-xml test-reports/results.xml'
                        sh 'python run_tests.py'
                        env.WORKSPACE = pwd()
                        def file_path = "${env.WORKSPACE}/test_report.txt"
                        if (fileExists(file_path)) {
                            def cov_total = readFile file_path
                            currentBuild.result = 'SUCCESS'

                            if (cov_total > env.THRESHOLD) {
                                mail body: "Project build successful. Coverage is ${cov_total} and threshold is ${env.THRESHOLD}",
                                     from: 'bpaynotifications@busaracenter.org',
                                     subject: 'Project build successful ',
                                     to: 'brian.misachi@busaracenter.org'
                            } else {
                                mail body: "Project build does not meet threshold. Coverage is ${cov_total} and threshold is ${env.THRESHOLD}",
                                 from: 'bpaynotifications@busaracenter.org',
                                 subject: 'Threshold not satisfied',
                                 to: 'brian.misachi@busaracenter.org'
                            }
                            echo cov_total
                        } else {
                            echo 'File does not exist'
                        }

                    } catch (Exception err) {
                        echo err
                        currentBuild.result = 'FAILURE'
                        mail body: 'Project build failure',
                             from: 'bpaynotifications@busaracenter.org',
                             subject: 'project build failure',
                             to: 'brian.misachi@busaracenter.org'
                    }

                    if (currentBuild.result == 'SUCCESS') {
                        junit 'test-reports/results.xml'
                    } else if (currentBuild.result == 'FAILURE') {
                        // TODO: Email Here
                        echo "RESULT: ${currentBuild.result}"
                        echo "CHANGE ID: ${env.CHANGE_ID}"
                    } else {
                        echo 'Did not match any status'
                    }
                } else {
                    echo 'Not to be tested'
                }
            }
        }
    }

    stage ('Cleanup') {
        sh "docker rmi -f ${env.app}"
        // Dangling Containers
         //sh 'docker ps -q -f status=exited | xargs --no-run-if-empty docker rm'

        // Dangling Images
        //sh 'docker images -q -f dangling=true | xargs --no-run-if-empty docker rmi'

        // Dangling Volumes
        //sh 'docker volume ls -qf dangling=true | xargs -r docker volume rm'
    }
}