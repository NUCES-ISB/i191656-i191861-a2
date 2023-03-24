pipeline {
    agent any
    stages {
	stage('Build') {
	    steps {
		script {
	            bat 'pip install requirements.txt'
	    	}
	    }
	}
        stage('Run Server') {
            steps {
		script {
		    bat "python app.py"
            	}
	    }
        }
    }
}