import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as efs from 'aws-cdk-lib/aws-efs';
import * as sm from 'aws-cdk-lib/aws-secretsmanager';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

export class IacStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. VPC
    const vpc = new ec2.Vpc(this, 'AppVPC', {
      maxAzs: 2,
      natGateways: 1,
      // Disable the custom resource that adds an asset ►
      restrictDefaultSecurityGroup: false,
    });

    // 2. ECS Cluster
    const cluster = new ecs.Cluster(this, 'AppCluster', {
      vpc,
      clusterName: 'chatbot-cluster',
    });

    // 3. EFS for RAG_DATA_DIR
    const fileSystem = new efs.FileSystem(this, 'DataEFS', {
      vpc,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      lifecyclePolicy: efs.LifecyclePolicy.AFTER_14_DAYS,
    });

    // 4. SecretsManager for OpenAI API Key
    const openAiSecret = new sm.Secret(this, 'OpenAIKeySecret', {
      secretName: 'chatbot/openai_api_key',
      description: 'OpenAI API Key for backend service',
    });

    // 5. Fargate Task Definition (Backend)
    const backendTaskDef = new ecs.FargateTaskDefinition(this, 'BackendTaskDef', {
      cpu: 256,
      memoryLimitMiB: 512,
    });

    // Add EFS volume
    backendTaskDef.addVolume({
      name: 'efs-vol',
      efsVolumeConfiguration: { fileSystemId: fileSystem.fileSystemId },
    });

    // Add Backend container
    const backendContainer = backendTaskDef.addContainer('BackendContainer', {
      image: ecs.ContainerImage.fromRegistry(
        `${props?.env?.account}.dkr.ecr.${props?.env?.region}.amazonaws.com/chatbot-backend:latest`
      ),
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'backend' }),
      environment: {
        RAG_DATA_DIR: '/mnt/data',
      },
      secrets: {
        OPENAI_API_KEY: ecs.Secret.fromSecretsManager(openAiSecret),
      },
      portMappings: [{ containerPort: 8000 }],
    });

    // Mount EFS into container
    backendContainer.addMountPoints({
      sourceVolume: 'efs-vol',
      containerPath: '/mnt/data',
      readOnly: false,
    });

    // 6. Fargate Service
    const backendService = new ecs.FargateService(this, 'BackendService', {
      cluster,
      taskDefinition: backendTaskDef,
      desiredCount: 1,
    });

    // Allow ECS Service to access EFS
    fileSystem.connections.allowDefaultPortFrom(backendService, 'Allow ECS tasks to EFS');

    // 7. Application Load Balancer
    const alb = new elbv2.ApplicationLoadBalancer(this, 'AppALB', {
      vpc,
      internetFacing: true,
    });
        // For local synth without ACM certificates, use HTTP listener on port 80
    const listener = alb.addListener('HttpListener', {
      port: 80,
      open: true,
    });
    listener.addTargets('BackendTG', {
      port: 8000,
      targets: [backendService],
      healthCheck: { path: '/health' },
    });
  }
}
