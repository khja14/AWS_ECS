import os
from flask import Flask
import boto3

app = Flask(__name__)

BUCKET_NAME = 'temp-2025-07-27'
PREFIX = 'my-folder/'  # フォルダ風のS3キー
LOCAL_DIR = './s3/'    # ダウンロード先ローカルディレクトリ

@app.route("/")
def hello():
    return "Hello, World!"


# S3への接続は、タスク作成時に"タスクロール(!タスク実行ロールではない)"で許可 : IAM ROLE に AmazonS3FullAccess を設定
@app.route("/refresh")
def refresh_from_s3():
    s3 = boto3.client('s3')

    # フォルダがなければ作成
    os.makedirs(LOCAL_DIR, exist_ok=True)

    response = None
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    except s3.exceptions.NoSuchBucket:
        return f"指定されたバケットが存在しません: {BUCKET_NAME}"

    # 該当ファイルがあれば処理
    if 'Contents' in response:
        try:
            for obj in response['Contents']:
                key = obj['Key']
                filename = key.split('/')[-1]  # ファイル名だけを抽出
                local_path = os.path.join(LOCAL_DIR, filename)
                
                # ディレクトリはスキップ（キーがフォルダで終わる場合）
                if key.endswith('/'):
                    continue

                print(f"Downloading {key} → {local_path}")
                s3.download_file(BUCKET_NAME, key, local_path)
        except Exception as e:
            return f"エラーが発生しました。: {e}"
    else:
        print("対象のファイルが見つかりません")

    return f"最新データをS3から取得しました。<br> /list で一覧表示できます。"


@app.route("/list")
def list_s3_folder():
    try:
        # フォルダの内容を取得
        files = os.listdir(LOCAL_DIR)
        if not files:
            return "フォルダは空です"
        return "<br>".join(files)  # 改行して一覧表示
    except FileNotFoundError:
        return f"フォルダが存在しません: {LOCAL_DIR}"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)