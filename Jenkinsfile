pipeline {
    agent any
    stages {
	stage('Build') {
	    steps {
		script {
	            bat 'docker build -t flask_image .'
	            bat 'docker run -d -p 5000:5000 flask_image'
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