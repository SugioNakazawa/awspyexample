# AWS lambda 開発 for python
## 事前準備
### 開発環境
- git ソース管理
- aws-cli awsコマンド
- python3 実装言語
- aws-mfa MFA認証対応
- vscode IDE
### python仮想環境
- pipen python & package バージョン管理

## ソースツリー
function1、function2がバッチに対応します。
0-xxxxから5-xxxxは
```
├── 0-run.sh              # ローカル実行（不要？）
├── 1-create-bucket.sh    # レイヤの格納先作成
├── 2-build-layer.sh      # ビルド
├── 3-deploy.sh           # awsへデプロイ
├── 4-invoke.sh           # 実行
├── 5-cleanup.sh          # アップしたリソースの全削除
├── Pipfile               # pipenvでinstallされたパッケージ
├── Pipfile.lock          # pipienvでinstallした詳細
├── README.md             # このドキュメント
├── function1             # １つのLambda関数の情報
│   ├── event.json        # invokeで与えるパラメータ
│   ├── function1.py      # 関数の実装
│   └── template.yml      # deploy設定
├── function2
│   └── function2.py
├── requirements.txt      # Pipfileから生成する
└── tests                 # テストケース
    └── test_function1.py
```
## その他
### パッケージの更新時の注意
pipenvでパッケージを更新、追加した場合には「2-build-layer.sh」の処理にてAWSへアップするパッケージも最新化されます。このため、pip installではなく必ず、`pipenv install`を行なってください。
### layer作成時の注意
numpyにはCライブラリが存在するため、AmazonLinux上でnumpyをインストールしたライブラリが必要です。それを含めたものをぱckage_bakに配置してあります。
```
cd python_module_builder
docker container run --rm -v ${PWD}/python:/opt/python python_module_builder numpy
docker container run --rm -v ${PWD}/python:/opt/python python_module_builder pandas
```
https://s10i.me/whitenote/post/46


### 参考
https://dev.classmethod.jp/articles/aws-lambda-dev-test-deploy-ci/
