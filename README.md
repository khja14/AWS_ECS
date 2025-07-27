# AWS ECS 
* https://qiita.com/takoikatakotako/items/1b6be6397a145be77e87
* cmd ( コマンドは、AWSでコピー可能 )


# 順番
1. ECR : リポジトリの作成
   * https://ap-northeast-1.console.aws.amazon.com/ecr/private-registry/repositories?region=ap-northeast-1
2. ローカル → ECR : イメージをプッシュ 
   * コマンドは、AWS ECRでコピー可能
3. タスク定義 : ECR の ARN を使って、タスク定義を作成
4. クラスター : クラスターの作成
   1. (任意) クラスター > サービス : サービスの作成
      * タスクをまとめて管理する仕組み
   2. (サービスがあれば不要) クラスター > タスク : タスク定義 をもとに タスク を作成する
      * サービスを作成していると、サービスの設定に則ってタスクが自動で起動される
      1. タスク作成の際に、ネットワーキング設定で、SGを設定すると、外部からPubIPを使ってアクセスできる
