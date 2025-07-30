import os
from flask import Flask, request
import boto3

app = Flask(__name__)

BUCKET_NAME = 'temp-2025-07-27'
PREFIX = 'my-folder/'  # フォルダ風のS3キー
LOCAL_DIR = '/app/shared/s3/'    # ダウンロード先ローカルディレクトリ

HTML = """
    リンク一覧
    <!-- <br> <a href='/refresh'>S3から最新データを取得</a> -->
    <br> <a href='/list'>ローカルフォルダの一覧</a>
    <br> <a href='/upload'>ファイルアップロード</a>
"""

@app.route("/")
def hello():
    return HTML + "<br><p>ローカルファイルリスト</p>" + show_folder_list()


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
        return f"指定されたバケットが存在しません: {BUCKET_NAME}<br> <a href='/'>戻る</a>"

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
            return f"エラーが発生しました。: {e} <br> <a href='/'>戻る</a>"
    else:
        print("対象のファイルが見つかりません")

    return f"最新データをS3から取得しました。<br> /list で一覧表示できます。 <br> <a href='/'>戻る</a>"


@app.route("/list")
def show_folder_list():
    try:
        # ファイルパスをすべて再帰的に収集
        file_list = []
        for root, dirs, files in os.walk(LOCAL_DIR):
            for file in files:
                # 相対パスに変換
                rel_dir = os.path.relpath(root, LOCAL_DIR)
                rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                file_list.append(rel_file)

        if not file_list:
            return "フォルダは空です <br> <a href='/'>戻る</a>"

        return "<br>".join(file_list)

    except FileNotFoundError:
        return f"フォルダが存在しません: {LOCAL_DIR}<br><a href='/'>戻る</a>"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}<br><a href='/'>戻る</a>"


@app.route("/upload", methods=["GET", "POST"])
def upload_to_s3():
    if request.method == "GET":
        return '''
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
            <br> <a href='/'>戻る</a>
        '''
    elif request.method == "POST":
        if 'file' not in request.files:
            return "ファイルが選択されていません <br> <a href='/upload'>戻る</a>"

        file = request.files['file']
        if file.filename == '':
            return "ファイル名が空です <br> <a href='/upload'>戻る</a>"
        
        if not file:
            return "ファイルが選択されていません <br> <a href='/upload'>戻る</a>"
        
        os.makedirs(LOCAL_DIR, exist_ok=True)  # フォルダがなければ作成

        file_path = os.path.join(LOCAL_DIR, file.filename)
        file.save(file_path)

        return f"アップロードされたファイル: {file.filename}<br> <a href='/'>戻る</a><br>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)