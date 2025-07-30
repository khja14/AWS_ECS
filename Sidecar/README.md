{
    <!-- タスク定義名 -->
  "family": "my-task-family-2025-07-30",
  "networkMode": "awsvpc",
  <!-- Fargate -->
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  <!-- ロール設定 -->
  "executionRoleArn": "arn:aws:iam::773245100111:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::773245100111:role/S3_From_ECR",
  <!-- コンテナ間の共有ボリュームの設定 -->
  "volumes": [
    {
      "name": "shared-data"
    }
  ],
  <!-- コンテナの設定 -->
  "containerDefinitions": [
    <!-- メインコンテナ -->
    {
      "name": "main-app",
      "image": "773245100111.dkr.ecr.ap-northeast-1.amazonaws.com/flask:latest",
      <!-- ポート設定 -->
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      <!-- 共有ボリューム設定 -->
      "mountPoints": [
        {
          "sourceVolume": "shared-data",
          "containerPath": "/app/shared"
        }
      ],
      "essential": true
    },
    <!-- サブコンテナ -->
    {
      "name": "sidecar",
      "image": "773245100111.dkr.ecr.ap-northeast-1.amazonaws.com/soa/sidecar_2025_07_30:latest",
      <!-- 共有ボリューム設定 -->
      "mountPoints": [
        {
          "sourceVolume": "shared-data",
          "containerPath": "/app/shared"
        }
      ],
      "essential": false
    }
  ]
}
