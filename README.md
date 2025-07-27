# AWS ECS 
=> ↓の方法でやってみるしかない
* https://qiita.com/takoikatakotako/items/1b6be6397a145be77e87
* cmd ( コマンドは、AWSでコピー可能 )
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 773245100111.dkr.ecr.ap-northeast-1.amazonaws.com


# 順番
1. ECR : リポジトリの作成 > https://ap-northeast-1.console.aws.amazon.com/ecr/private-registry/repositories?region=ap-northeast-1
2. ローカル → ECR : イメージをプッシュ
3. タスク定義 : ECR の ARN を使って、タスク定義を作成
4. クラスター : クラスターの作成
5. クラスター > タスク : タスク定義 を使って、タスクを作成する
   1. タスク作成の際に、ネットワーキング設定で、SGを設定すると、外部からPubIPを使ってアクセスできる
