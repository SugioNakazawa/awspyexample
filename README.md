# AWS Lambda sample for python
Lambda 関数のサンプルを python で作成してみました。
pandasを利用したs3からのcsv読み込み、Athenaからのデータ取得、webAPIコールを試しています。
- 利用環境
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
- (Windows)Windowsでのpipenvのインストールは以下を参照。
  https://qiita.com/Haaamaaaaa/items/a2852ed0b3e0b7c4d1ab
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
# 開発用もインストール
pipenv install --dev
```
### その他
- aws-mfa：AWSアカウントがMFA認証の場合には便利。
- vscode：コードの実装以外にもAWSへの接続が便利。

## VSCODEでの実行
プロジェクトのホームにてpipenvの仮想環境に入ってVSCODEを起動します。
```shell
pipenv shell

code .
```
ダウンロードソースは特定のS3バケットにアクセスしてしまうのでsrc/utils/config.ini の MY_BUCKET 変数の値(your-unique-number)を変更してしてください。

### テーブルの作成
- src/tests/prepare_athena.py を実行することによりAthena DB、テーブルを作成します。バケットがない場合には上記に記載した バケット名+.ユーザ名 でバケットを作成します。
- src/tests/drop_db_athena.py はAthenaDBを削除します。バケットは削除しません。
### テスト実行
VSCODE のテストより実行を行い全てがOKになることを確認してください。

## Lmbda実行手順
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
### Lambda 関数のの準備
```shell
3-build-function.sh [ハンドラ関数モジュール名]
```
ハンドラを定義したモジュールとutils配下をzipに圧縮します。
モジュール名とデプロイ情報のディレクトリ名を同じにしておく必要があります。
### AWSへのデプロイ
```shell
4-deploy.sh [ハンドラ関数モジュール名]
```
template.ymlによってAWSへのデプロイを行います。template.ymlを配置したディレクトリ（app1やapp2）を指定します。
### Lambda関数の実行
```shell
5-invoke.sh  [ハンドラ関数モジュール名]
```
event.jsonの内容を引数としてLambda関数を実行します。
event.jsonを配置したディレクトリ（func1やfunc2）を指定します。
### リソースの削除
```shell
6-cleanup.sh [ハンドラ関数モジュール名]
```
AWSに登録したリソースを削除します。デプロイ時の引数にてスタックが作成されていますので削除時にも同じ引数を渡します。このコマンドにて最初に作成したS3バケットも削除します。

## ガバレッジ
Pipfileにてインストールしたcoverageを利用します。
```shell
# unittest実行
coverage run --source src -m unittest discover -s tests/ -p "test_*.py"
# レポート出力
coverage report -m
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/func1.py               17      2    88%   29-30
src/func2.py               37      1    97%   60
src/func3.py               21      3    86%   22-23, 39
src/funcXXX.py             44     44     0%   1-73
src/utils/__init__.py       0      0   100%
src/utils/athena.py        45      8    82%   55-56, 61-62, 70-75
src/utils/config.py        10      1    90%   19
src/utils/logger.py        11      0   100%
-----------------------------------------------------
# XMLファイル作成
coverage xml
 ```
vscodeでエディター上で確認するためにはCode Coverage Highlighterを利用します。
shift+cmd+P で`> Code Coverage: Toggle coverage display`を選択します。
## プログラム構造
Lambdaから呼ばれる関数はsrc直下のfunc1,func2...に定義します。各関数で共通利用するモジュールはsrc/utils配下に置き各関数から呼びます。
AWS Lambdaへアップロードするソースは対象のハンドラを定義したモジュールとutils配下をzipファイルに圧縮します。template.ymlのCodeUrlではそのzipファイルを指定します。
### ソースツリー
0-xxxxから5-xxxxはAWS CLIを利用してAWSへのデプロイと実行を行います。
```shell
├── 1-create-bucket.sh    # レイヤの格納先作成
├── 2-build-layer.sh      # Layerビルド
├── 3-build-function.sh   # Functionビルド
├── 4-deploy.sh           # awsへデプロイ
├── 5-invoke.sh           # 実行
├── 6-cleanup.sh          # アップしたリソースの全削除
├── build                 # ビルド、デプロイで作成される
│   ├── bucket-name.txt   # s3に作成したバケット名
│   └── package           # パッケージライブラリ
├── LICENSE               # ライセンスファイル（MIT）
├── Pipfile               # pipenvでinstallされたパッケージ
├── Pipfile.lock          # pipienvでinstallしたパッケージ・バージョン
├── README.md             # このドキュメント
├── conf                  # デプロイ、実行
│   ├── func1             # func1の情報。名前はモジュール名とする
│   │   ├── build         # ビルド時に作成される
│   │   │   └── func.zip  # AWSへアップされるモジュール
│   │   ├── event.json    # Lambda関数実行時の引数
│   │   └── template.yml  # CloudFormationの設定
│   ├── func2
│   │   ├── build
│   │   │   └── func.zip
│   │   ├── event.json
│   │   └── template.yml
│   └── func3
│       ├── build
│       │   └── func.zip
│       ├── event.json
│       └── template.yml
├── package.tar           # Lambda Layerに配置する外部パッケージ
├── requirements.txt      # 標準形式のパッケージ情報（Pipfileから手動で生成）
├── src                   # ソースコード。Lambdaへ登録するディレクトリ
│   ├── func1.py          # 関数１(webAPIの利用)モジュール
│   ├── func2.py          # 関数２(S3csv→pandas)モジュール
│   ├── func3.py          # 関数３(Athena→pandas)モジュール
│   ├── funcXXX.py
│   └── utils
│       ├── __init__.py
│       ├── athenaaccess.py # Athenaアクセス
│       ├── config.ini    # 環境別定数定義
│       ├── config.py     # 定数アクセスモジュール
│       ├── mylogger.py   # ログ設定
│       └── s3util.py     # s3ユーティル
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

Dockerによるパッケージ作成
```shell
cd python_module_builder
docker container run --rm -v ${PWD}/python:/opt/python python_module_builder pandas
```
参考リンク
https://s10i.me/whitenote/post/46

### MFA認証
aws-mfaはこのプロジェクトのPipfileではインストールしていません。実行マシンにインストールしておくことをお勧めします。

参考 https://qiita.com/ogady/items/c17ffe8f7c8e15b15f77

### MFA認証によるCodeCommitへのgitクライアントの接続
とりあえず以下のコマンドでgitに設定を追加すれば接続できそう。
```shell
$ git config --local credential.helper '!aws codecommit credential-helper $@'
$ git config --local credential.UseHttpPath true
```

### 使い方
```shell
aws-mfa --profile [プロファイル名]
```
