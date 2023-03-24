pipeline {
    agent any
    stages {
	stage('Build') {
	    steps {
		script {
	            bat 'docker build -t flask_image .'
	            CONTAINER_ID = bat(script: '@docker run -d flask_image -p 5000:5000', returnStdout: true).trim()	
	    	}
	    }
	}
        stage('Run Server') {
            steps {
		script {
		    bat "docker exec ${CONTAINER_ID} python app.py"
            	}
	    }
        }
    }
}