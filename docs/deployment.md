# Deployment Guide - Strands Agents SDK Sample Project

This guide covers various deployment options for Strands Agents applications, from local development to production cloud deployments.

## Table of Contents

1. [Local Development](#local-development)
2. [AWS Lambda Deployment](#aws-lambda-deployment)
3. [AWS Fargate Deployment](#aws-fargate-deployment)
4. [Amazon EKS Deployment](#amazon-eks-deployment)
5. [Amazon EC2 Deployment](#amazon-ec2-deployment)
6. [Production Considerations](#production-considerations)

## Local Development

### Development Server Setup

**1. Basic Flask/FastAPI Server:**
```python
# app.py
from flask import Flask, request, jsonify
from strands import Agent
from strands_tools import calculator

app = Flask(__name__)

# Initialize agent
agent = Agent(
    tools=[calculator],
    system_prompt="You are a helpful assistant."
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        response = agent(user_message)
        return jsonify({
            'response': str(response),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**2. Running Locally:**
```bash
# Install web framework
pip install flask

# Run development server
python app.py

# Test the endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2 + 2?"}'
```

### Docker Development

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  strands-agent:
    build: .
    ports:
      - "5000:5000"
    environment:
      - AWS_REGION=us-west-2
      - LOG_LEVEL=INFO
    volumes:
      - ~/.aws:/root/.aws:ro  # Mount AWS credentials
```

**Commands:**
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d
```

## AWS Lambda Deployment

AWS Lambda is ideal for serverless, event-driven agent applications.

### Lambda Function Code

**lambda_function.py:**
```python
import json
import os
from strands import Agent
from strands_tools import calculator

# Initialize agent outside handler for reuse
agent = Agent(
    tools=[calculator],
    system_prompt="You are a helpful assistant.",
    max_parallel_tools=2  # Limit for Lambda
)

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    try:
        # Parse input
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        user_message = body.get('message', '')
        
        if not user_message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Message is required'})
            }
        
        # Process with agent
        response = agent(user_message)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': str(response),
                'metrics': {
                    'processing_time': response.metrics.total_time_seconds,
                    'tool_calls': response.metrics.tool_calls
                }
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Deployment with AWS SAM

**template.yaml:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 300
    MemorySize: 1024
    Runtime: python3.11

Resources:
  StrandsAgentFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: lambda_function.lambda_handler
      Environment:
        Variables:
          AWS_REGION: !Ref AWS::Region
          LOG_LEVEL: INFO
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - bedrock:InvokeModel
                - bedrock:InvokeModelWithResponseStream
              Resource: '*'
      Events:
        ChatApi:
          Type: Api
          Properties:
            Path: /chat
            Method: post

Outputs:
  ChatApi:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/chat/"
```

**Deployment Commands:**
```bash
# Install SAM CLI
pip install aws-sam-cli

# Build and deploy
sam build
sam deploy --guided

# Test deployment
curl -X POST https://your-api-id.execute-api.us-west-2.amazonaws.com/Prod/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### Lambda Optimization Tips

1. **Cold Start Reduction:**
   ```python
   # Initialize agent outside handler
   agent = Agent(...)  # Global initialization
   
   def lambda_handler(event, context):
       # Handler code
   ```

2. **Memory Configuration:**
   - Start with 1024 MB for Strands agents
   - Monitor CloudWatch metrics and adjust
   - More memory = faster CPU and better performance

3. **Timeout Settings:**
   - Set timeout to 5+ minutes for complex agents
   - Consider async processing for long-running tasks

## AWS Fargate Deployment

Fargate provides containerized deployment without server management.

### Fargate Task Definition

**task-definition.json:**
```json
{
  "family": "strands-agent-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "strands-agent",
      "image": "your-account.dkr.ecr.region.amazonaws.com/strands-agent:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_REGION",
          "value": "us-west-2"
        },
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/strands-agent",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Deployment with CDK

**fargate_stack.py:**
```python
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2
)

class StrandsAgentFargateStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # VPC
        vpc = ec2.Vpc(self, "StrandsVPC", max_azs=2)
        
        # ECS Cluster
        cluster = ecs.Cluster(self, "StrandsCluster", vpc=vpc)
        
        # Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self, "StrandsTaskDef",
            memory_limit_mib=2048,
            cpu=1024
        )
        
        # Add Bedrock permissions
        task_definition.task_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                resources=["*"]
            )
        )
        
        # Container
        container = task_definition.add_container(
            "StrandsContainer",
            image=ecs.ContainerImage.from_registry("your-image:latest"),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="strands-agent",
                log_group=logs.LogGroup(
                    self, "StrandsLogGroup",
                    retention=logs.RetentionDays.ONE_WEEK
                )
            ),
            environment={
                "AWS_REGION": self.region,
                "LOG_LEVEL": "INFO"
            }
        )
        
        container.add_port_mappings(
            ecs.PortMapping(container_port=5000)
        )
        
        # Fargate Service
        service = ecs.FargateService(
            self, "StrandsService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2
        )
        
        # Load Balancer
        lb = elbv2.ApplicationLoadBalancer(
            self, "StrandsLB",
            vpc=vpc,
            internet_facing=True
        )
        
        listener = lb.add_listener(
            "StrandsListener",
            port=80,
            default_targets=[service]
        )
```

## Amazon EKS Deployment

For Kubernetes-based deployments with advanced orchestration needs.

### Kubernetes Manifests

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strands-agent
  labels:
    app: strands-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: strands-agent
  template:
    metadata:
      labels:
        app: strands-agent
    spec:
      serviceAccountName: strands-agent-sa
      containers:
      - name: strands-agent
        image: your-account.dkr.ecr.region.amazonaws.com/strands-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: AWS_REGION
          value: "us-west-2"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: strands-agent-service
spec:
  selector:
    app: strands-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

**serviceaccount.yaml:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: strands-agent-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT:role/StrandsAgentRole
```

### Deployment Commands

```bash
# Create EKS cluster
eksctl create cluster --name strands-cluster --region us-west-2

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f serviceaccount.yaml

# Check deployment
kubectl get pods
kubectl get services

# Scale deployment
kubectl scale deployment strands-agent --replicas=5
```

## Amazon EC2 Deployment

Traditional server deployment with full control.

### EC2 Setup Script

**user-data.sh:**
```bash
#!/bin/bash
yum update -y
yum install -y python3 python3-pip git

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Clone and setup application
cd /home/ec2-user
git clone https://github.com/your-repo/strands-agent.git
cd strands-agent

# Install dependencies
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/strands-agent.service << EOF
[Unit]
Description=Strands Agent Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/strands-agent
ExecStart=/usr/bin/python3 app.py
Restart=always
Environment=AWS_REGION=us-west-2
Environment=LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl daemon-reload
systemctl enable strands-agent
systemctl start strands-agent
```

### Auto Scaling Group

**CloudFormation template:**
```yaml
Resources:
  LaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: StrandsAgentTemplate
      LaunchTemplateData:
        ImageId: ami-0abcdef1234567890  # Amazon Linux 2
        InstanceType: t3.medium
        IamInstanceProfile:
          Arn: !GetAtt InstanceProfile.Arn
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            # User data script here
        SecurityGroupIds:
          - !Ref SecurityGroup

  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
      MinSize: 1
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      TargetGroupARNs:
        - !Ref TargetGroup
```

## Production Considerations

### Security

**1. IAM Roles and Policies:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

**2. Network Security:**
- Use VPC with private subnets
- Configure security groups with minimal required access
- Enable VPC Flow Logs
- Use AWS WAF for web applications

**3. Secrets Management:**
```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Use in application
api_key = get_secret('strands-agent/api-key')
```

### Monitoring and Observability

**1. CloudWatch Metrics:**
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def put_custom_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='StrandsAgent',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit
            }
        ]
    )

# Usage
put_custom_metric('AgentRequests', 1)
put_custom_metric('ResponseTime', response_time, 'Seconds')
```

**2. Structured Logging:**
```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName
        }
        return json.dumps(log_entry)

# Configure logger
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

**3. Distributed Tracing:**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Use in application
with tracer.start_as_current_span("agent_request"):
    response = agent(user_message)
```

### Performance Optimization

**1. Connection Pooling:**
```python
import boto3
from botocore.config import Config

# Configure with connection pooling
config = Config(
    max_pool_connections=50,
    retries={'max_attempts': 3}
)

bedrock_client = boto3.client('bedrock-runtime', config=config)
```

**2. Caching:**
```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='elasticache-endpoint')

def cached_agent_response(user_message):
    # Create cache key
    cache_key = hashlib.md5(user_message.encode()).hexdigest()
    
    # Check cache
    cached_response = redis_client.get(cache_key)
    if cached_response:
        return json.loads(cached_response)
    
    # Generate response
    response = agent(user_message)
    
    # Cache response (expire in 1 hour)
    redis_client.setex(
        cache_key, 
        3600, 
        json.dumps(str(response))
    )
    
    return response
```

**3. Load Balancing:**
- Use Application Load Balancer for HTTP traffic
- Configure health checks
- Enable sticky sessions if needed
- Set up auto-scaling based on metrics

### Cost Optimization

**1. Right-sizing:**
- Monitor resource utilization
- Use appropriate instance types
- Consider Spot instances for non-critical workloads

**2. Model Selection:**
- Choose cost-effective models for your use case
- Consider model caching and batching
- Monitor Bedrock usage and costs

**3. Auto-scaling:**
```yaml
# CloudWatch alarm for scaling
ScaleUpAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: StrandsAgent-HighCPU
    MetricName: CPUUtilization
    Namespace: AWS/ECS
    Statistic: Average
    Period: 300
    EvaluationPeriods: 2
    Threshold: 70
    ComparisonOperator: GreaterThanThreshold
    AlarmActions:
      - !Ref ScaleUpPolicy
```

This deployment guide provides comprehensive options for running Strands Agents applications in production environments, from serverless to containerized deployments.
