# はじめに
- このファイルでは、アプリを動作させるための環境構築手順を記載する

# 動作環境構築方法
### 前提
- pythonかインストールしていること
- githubのインストール及びログイン済みであること

### 手順
1. projectファイルのインストール
   1. 任意のディレクトリにてKidlog_Projectのレポジトリをcloneする
  ```
  git clone https://github.com/snj184k-ops/kidlog_Project.git
  ```
2. 仮想環境の構築
   1. 1を実行したディレクトリにて仮想環境作成
  ```
   python3 -m venv myvenv
  ```
  2. 仮想環境へのログイン
  ```
   source myvenv/bin/activate
  ```
  3. パッケージのインストール
  ```
   pip install -r kidlog_project/requirements.txt 
  ```
3. ローカルサーバー立ち上げ
   1. kidlog_projectディレクトリに移動
   2. 下記コマンドを実行
  ```
   python manage.py runserver 
  ```
4. webにて以下リンクにアクセス<br>
http://127.0.0.1:8000/accounts/login/
<br>

5. ログイン画面が表示されるため既存登録データを確認する場合は以下内容でログイン<br>
  (以下注意項目でも記載のように新規ユーザーを作成する場合、データがなくアプリの動作確認が難解なため既存ユーザーを用意)
   1. ユーザー：test
   2. パスワード：test
6. child1を選択するとdashboard画面を表示する

#### <注意>
現在はDBも含めてgithubにアップロードしている。<br>
(事前データが入っているとポートフォリオとして確認しやすいため)<br>
本来はmigtateが必要

# ポートフォリオ確認用、事前登録情報
前述した通りポートフォリオ確認用のため、事前にDBへレコードを登録している。
今回はその内容について説明する。
### ユーザー情報
ユーザー情報は以下一件のみ登録している
| id | user  | password  |
| --- | --- | --- |
| 1 | test | test |
後述するデータに関してもtestユーザーに紐づいている
### 子ども情報
子ども情報は以下一件のみ登録している
| id | name | birth_date | user_id |
| --- | --- | --- | --- |
| 1 | child1 | 2024-10-20 | 1 |
### 乳児記録情報
乳児記録情報となる以下テーブルに関して、1年分のデータを格納している
- 身長・体重
- ミルク記録
- うんち記録
- おしっこ記録
- 睡眠記録
- 体温記録
- 食事記録

1年分のデータ保存方法に関しては別途後述する`備考：サンプルデータ登録方法`を参照
### 日記
日記のデータに関して、1年分のデータを格納している
1年分のデータ保存方法に関しては別途後述する`備考：サンプルデータ登録方法`を参照

# 備考：サンプルデータ登録方法
新規ユーザー及び子どもデータを登録の上でサンプルデータが必要な場合にこちらを参照
### 乳児記録登録方法
乳児記録を登録する場合、以下ファイルを実行する
1. baby_data_dummy_script.py
   - 身長・体重以外の記録に関して、1年分のデータをcsv形式でdataフォルダに出力
   - 以下項目を手動で設定
     - child_id
      - start_date(開始日)
      - days(期間)
```
python script/baby_data_dummy_script.py 
```
1. generate_htmt_records.py
   - 身長・体重の記録に関して、1年分のデータをcsv形式でdataフォルダに出力
   - 以下引数を指定する
     - child_id
     - sex(male:男の子, female:女の子)
   - 開始日や期間を変更したい場合は別途ソースコードを修正する
```
python script/generate_htmt_records.py 1 male
```
1. record_import.sh 
   - 各種csvファイルを元にDBへinsertする
```
bash record_import.sh 
```

### 日記記録登録方法
日記の場合はpythonファイルではなく、事前にexcelファイル`data/baby_diary_sample.xlsx`を用意した<br>
(日記の内容がpythonだとある程度固定されてしまうため)

1. 日付を変更したい場合は直接excelファイルを変更する
2. excelファイルのimportスクリプトを実行する
   - 引数
     - 対象excelファイル
     - child_id=x 
```
python manage.py import_diary_excel_script data/baby_diary_sample.xlsx --child_id=1
```