pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Install + Test') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
          mkdir -p reports
          pytest -q --junitxml=reports/pytest.xml
        '''
      }
    }
  }

  post {
    always {
      junit testResults: 'reports/pytest.xml', allowEmptyResults: true
      archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
    }
  }
}
