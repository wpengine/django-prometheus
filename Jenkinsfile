#!groovy
@Library('wpshared') _

node ('docker') {
    wpe.pipeline('Giant Meteor') {
        stage('Test') {
            sh 'make test'

// TODO: Add a junit report to the test run

//            junit 'src/reports/junit.xml'
//            cobertura 'src/reports/coverage.xml'
//            violations(100) {
//              sourcePathPattern '**/src'
//              pep8(1, 5, 100, 'src/reports/pep8.report')
//              pylint(10, 50, 100, 'src/reports/pylint.report')
//            }

// TODO: Add coverage report to the test run

//            publishHTML (target: [
//                allowMissing: false,
//                alwaysLinkToLastBuild: false,
//                keepAll: true,
//                reportDir: 'src/reports/coverage',
//                reportFiles: '*',
//                reportName: 'Test Coverage'
//            ])
        }
        stage('Build') {
            sh 'make sdist'
        }
        stage('Publish') {
            def packagePath = sh(returnStdout: true, script: 'ls dist/*.tar.gz').trim()
            gemFury.publishPackage(packagePath)
        }
    }
}
