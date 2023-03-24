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
	stage('Push to DockerHub') {
	    steps {
		script {
	            bat 'docker tag flask_image i191656/mlops_repo:flask_image'
	            bat 'docker push i191656/mlops_repo:flask_image'
	    	}
	    }
	}
    }
}