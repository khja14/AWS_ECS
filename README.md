# AWS ECS 
=> ↓の方法でやってみるしかない
* https://qiita.com/takoikatakotako/items/1b6be6397a145be77e87
* cmd ( コマンドは、AWSでコピー可能 )
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 773245100111.dkr.ecr.ap-northeast-1.amazonaws.com
