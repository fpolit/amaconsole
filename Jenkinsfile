pipeline{
    environment {
        LOGLEVEL='DEBUG'
        CMAKE_COMPILER_WALL='ON'
        CMAKE_BUILD_TYPE='Debug'
        CMAKE_BUILD_TESTS='ON'
    }

    agent {
        dockerfile {
            filename "ubuntu20.04-python3.8.dockerfile"
            dir 'data/agents/'
        }
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                mkdir -p build
                cmake -S . -B build -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} \
                                    -DCMAKE_COMPILER_WALL=${CMAKE_COMPILER_WALL} \
                                    -DCMAKE_BUILD_TESTS= ${CMAKE_BUILD_TESTS}\
                                    --log-level=${LOGLEVEL} || exit 1
                make -C build
                '''
            }
        }
        stage('Install'){
            steps {
                sh 'make -C build install'
            }
        }

        stage('Tests') {
            steps {
                sh '''
                make -C build test
                make -C build pytest
                '''
            }
        }
    }
}
