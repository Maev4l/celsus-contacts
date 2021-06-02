def withDockerNetwork(Closure inner) {
    try {
        networkId = UUID.randomUUID().toString()
        sh "docker network create ${networkId}"
        inner.call(networkId)
    } finally {
        sh "docker network rm ${networkId}"
    }
}

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
                    withDockerNetwork { n ->
                        docker.image('postgres:10.3-alpine').withRun("--name postgres-${n} --network ${n} -e POSTGRES_PASSWORD=  -d") { db ->
                            docker.image('localstack/localstack:0.12.11').withRun("--name localstack-${n} -d --network ${n} -e SERVICES=s3 -e DEFAULT_REGION=eu-central-1") { localstack ->
                                docker.image('671123374425.dkr.ecr.eu-central-1.amazonaws.com/jenkins/python:3.8').inside("--network ${n} -e PGHOST=postgres-${n} -e MOCK_AWS=localstack-${n} -e COVERALLS_GIT_BRANCH=${env.GIT_BRANCH} -e COVERALLS_SERVICE_NAME=internal-jenkins -e COVERALLS_REPO_TOKEN=${COVERALLS_TOKEN}") {
                                    
                                    // Has to use a debian image, otherwise need to rebuild the postgreSQL driver from source
                                    sh "pip install -r requirements.txt pytest pytest-env pytest-cov coveralls"
                                    sh "./wait-localstack.sh localstack-${n}"
                                    // pytest-cov needs the module name for the --cov flag
                                    sh 'python -m pytest --cov=contacts'
                                    if (env.GIT_BRANCH == 'master') {
                                        sh 'python -m coveralls'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}