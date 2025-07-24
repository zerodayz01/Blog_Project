Auto Aero Blog is a Flask-based web application designed for enthusiasts to share and explore posts about aviation, cars, and motorcycles. It was built as a hands-on project to apply AWS services in a real-world deployment.

Features:
- Browse posts by category (aviation, car, motorcycle)
- Submit posts for admin review
- Admin dashboard for approving, editing, and deleting posts

Tech Stack:
- Backend: Flask, SQLAlchemy, MySQL (Amazon Aurora)

Frontend: 
- HTML, CSS, Jinja, jQuery

Hosting: 
- EC2, ALB, Launch Template, Target Group
- Storage & Monitoring: RDS, S3 (static images), CloudWatch

Security & Automation: 
- IAM, VPC, Security Groups, AWS CLI

AWS Integration
- EC2 instance behind Application Load Balancer
- Aurora RDS for data storage
- S3 for serving static images
- CloudWatch for health monitoring
- Billing alarm for cost control
