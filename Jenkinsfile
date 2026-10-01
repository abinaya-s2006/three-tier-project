pipeline {  
agent any
    stages{
        stage ('clone') {
            steps{
                git branch: 'master',
                    url:'https://github.com/abinaya-s2006/three-tier-project.git'
            }
        }
        stage ('Build frontend') {
            steps{
                sh '''
                cd frontend
                docker build -t abinayasenguttuvan/three-tier-frontend .

                '''
            }
        }
        stage ('Build backend') {
            steps{
                sh '''
                cd backend
                docker build -t abinayasenguttuvan/three-tier-backend .
                '''
            }
        }
        stage ('Docker Push') {
            steps{
                sh '''
                docker push abinayasenguttuvan/three-tier-frontend:latest
                docker push abinayasenguttuvan/three-tier-backend:latest
                '''
            }
        }
        stage('Deploy Kubernetes') {
            steps{
                sh '''
                kubectl apply -f k8s
                '''
            }
        }

    }
}
