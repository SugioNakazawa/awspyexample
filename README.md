# AWS Lambda sample for python
Lambda 関数のサンプルを python で作成してみました。
pandasを利用したs3からのcsv読み込み、Athenaからのデータ取得、webAPIコールを試しています。
## 利用環境
- macOS:11.2.3
- AWS Lambda,S3,Athena,CloudFormation,CloudWatchLogs
## 事前準備
- pipenv：pipenvでpython環境を構築しています。ipfile.lockから同一バージョンのパッケージをインストールします。
  - macの場合はbrewで
    ```shell
    brew install pipenv
    ```
  - windowsの場合はpipで
    ```shell
    pip install pipenv
    ```
    pythonが入っていないと使えません、pythonをインストールしてから行ってください。
- AWS CLI バージョン2：AWSへのデプロイ、実行で利用します。[AWSサイト](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2.html)
- AWSアカウント：unittestでs3、Athenaにアクセスするために必要です。
### ソースコードのダウンロード
```shell
git clone git@github.com:SugioNakazawa/awspyexample.git
```
### pythonパッケージのインストール
```shell
cd awspyexample
pipenv install
```
### その他
- aws-mfa：AWSアカウントがMFA認証の場合には便利。
- vscode：コードの実装以外にもAWSへの接続が便利。

## 実行手順
IDEなどを用いてunittestが完了した後にAWS Lambda関数としてのテストをシェルにて実行します。
### リソース用S3バケットの作成
```shell
./1-create-bucket.sh
```
リソースを格納するランダムな名前のS3を作成します。
### Lambda layerに格納するリソースの準備
```shell
2-build-layer.sh
```
Pipfile.lockからrequirements.txtを作成してpackage/pythonにインストールします。
今回はpandasにてCライブラリを使用するためあらかじめ用意したpackage.tarを解凍して使用します。
### AWSへのデプロイ
```shell
3-deploy.sh [関数の識別（app1やapp2）]
```
template.ymlによってAWSへのデプロイを行います。template.ymlを配置したディレクトリ（app1やapp2）を指定します。
### Lambda関数の実行
```shell
4-invoke.sh  [関数の識別（app1やapp2）]
```
event.jsonの内容を引数としてLambda関数を実行します。
event.jsonを配置したディレクトリ（app1やapp2）を指定します。
### リソースの削除
```shell
5-cleanup.sh [関数の識別（app1やapp2）]
```
AWSに登録したリソースを削除します。デプロイ時の引数にてスタックが作成されていますので削除時にも同じ引数を渡します。このコマンドにて最初に作成したS3バケットも削除します。

## プログラム構造
Lambdaから呼ばれる関数はsrc直下のfunc1,func2...に定義します。各関数で共通利用するモジュールはsrc/utils配下に置き各関数から呼びます。
AWS Lambdaへアップロードするソースはtemplate.ymlのCodeUrlで指定するsrc配下全てとなります。
```
このため各関数には使用されない他の関数もアップロードされてしまいますが実装する関数が少ないこととアップロード時のディレクトリ構造の変換を不要にするためこのような構造となっています。
```
### ソースツリー
0-xxxxから5-xxxxはAWS CLIを利用してAWSへのデプロイと実行を行います。
```shell
├── 1-create-bucket.sh    # レイヤの格納先作成
├── 2-build-layer.sh      # ビルド
├── 3-deploy.sh           # awsへデプロイ
├── 4-invoke.sh           # 実行
├── 5-cleanup.sh          # アップしたリソースの全削除
├── LICENSE               # ライセンスファイル（MIT）
├── Pipfile               # pipenvでinstallされたパッケージ
├── Pipfile.lock          # pipienvでinstallしたパッケージ・バージョン
├── README.md             # このドキュメント
├── app1                  # 関数１のデプロイと実行情報
│   ├── event.json        # 関数１の実行時引数
│   └── template.yml      # 関数１のデプロイ用テンプレート
├── app2                  # 関数２のデプロイと実行情報
│   ├── event.json        # 関数２の実行時引数
│   └── template.yml      # 関数２のデプロイ用テンプレート
├── app3                  # 関数３のデプロイと実行情報
│   ├── event.json        # 関数３の実行時引数
│   └── template.yml      # 関数３のデプロイ用テンプレート
├── package.tar           # Lambda Layerに配置する外部パッケージ
├── requirements.txt      # 標準形式のパッケージ情報（Pipfileから手動で生成）
├── src                   # ソースコード。Lambdaへ登録するディレクトリ
│   ├── __init__.py
│   ├── func1.py          # 関数１(webAPIの利用)モジュール
│   ├── func2.py          # 関数２(S3csv→pandas)モジュール
│   ├── func3.py          # 関数３(Athena→pandas)モジュール
│   ├── funcXXX.py
│   └── utils
│       ├── __init__.py
│       ├── athena.py     # Athenaアクセスのヘルパー
│       ├── config.ini    # 環境別定数定義
│       ├── config.py     # 定数アクセスモジュール
│       └── logger.py     # ログ設定
└── tests                 # テストコード、テストデータ
    ├── datas             # テストデータ
    │   ├── data1.csv     # s3に配置するcsvデータ
    │   └── weather.csv   # テスト用Athenaへ登録するデータ
    ├── drop_db_athena.py # テスト用AthenaのDB削除（手動実行）
    ├── prepare_athena.py # テスト用AthenaのDB作成（手動実行）
    ├── test_func1.py     # 関数１テストケース(webAPI Mock)
    ├── test_func2.py     # 関数１テストケース
    └── test_func3.py     # 関数１テストケース
```
## その他
### layer作成時の注意
pandasにはCライブラリが存在するため、AmazonLinux上でインストールしたライブラリが必要です。package.tarに圧縮してあります。
新たなパッケージが必要な場合にはpipenv install [パッケージ]にてローカルテストを行います。デプロイする前にAmazonLinuxにてパッケージを作成してpackage.tarを再作成してください。

以下は参考リンクです

https://s10i.me/whitenote/post/46

Dockerによるパッケージ作成
```shell
cd python_module_builder
docker container run --rm -v ${PWD}/python:/opt/python python_module_builder pandas
```


### 参考
https://dev.classmethod.jp/articles/aws-lambda-dev-test-deploy-ci/
