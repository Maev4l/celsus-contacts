pipeline { 
    agent any
    options { 
        buildDiscarder(logRotator(numToKeepStr: '3'))
        disableConcurrentBuilds()
        ansiColor('xterm')
    } 
    triggers {
        githubPush()
    }
    stages {
        stage ('Build') {
            environment {
                COVERALLS_TOKEN = credentials('celsus-contacts-coveralls-token')
            }
            steps {
                script {
                    docker.image('postgres:10.3-alpine').withRun('--name mypostgres --network host -e POSTGRES_PASSWORD=  -d') { db ->
                        docker.image('localstack/localstack:0.12.11').withRun('--name localstack -d --network host -e SERVICES=s3 -e DEFAULT_REGION=eu-central-1') { localstack ->
                            docker.image('671123374425.dkr.ecr.eu-central-1.amazonaws.com/jenkins/python:3.8').inside("-u root --privileged --network host -e COVERALLS_GIT_BRANCH=${env.GIT_BRANCH} -e COVERALLS_SERVICE_NAME=internal-jenkins -e COVERALLS_REPO_TOKEN=${COVERALLS_TOKEN}") {
                                // Has to use a debian image, otherwise need to rebuild the postgreSQL drier from source
                                sh 'pip install -r requirements.txt pytest pytest-env pytest-cov coveralls'
                                sh './wait-localstack.sh'
                                // pytest-cov needs the module name for the --cov flag
                                sh 'pytest --cov=contacts'
                                sh 'coveralls'
                            }
                        }
                    }
                }
            }
        }
    }
}