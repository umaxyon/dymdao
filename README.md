# DymDao

AWS のDynamoDBの記述を簡単にして、気軽に使えるようにするboto3のラッパーライブラリ。

## Features

* 既存のboto3のメソッドがそのまま利用できます。ただし、レスポンスから「Item」「Items」を取り出し、結果だけを返却します。
* 「findメソッド」が追加されます。findメソッドは、get_item と query の代替として、より簡単な記述法を提供します。



## Install

```shell
pip install git+https://github.com/umaxyon/dymdao.git
```

## Usage

```python
from dymdao.dymdao import DymDao

dao = DymDao()
tbl = dao.table('tbl_hogehoge')  # HASH、RANGE両方定義された複合テーブル、または単一キーテーブル


# boto3 の Tableに定義されているメソッドが全てそのまま使える
dat = tbl.get_item(Key={'mykey': '3238', 'row': '2021/02/03'})

# ただし、「dat["Item"]」とか「dat["Items"]」とか書く必要はなく、Itemから取り出された結果が返却される
print(dat)

# findメソッド
# HASH、RANGE 両指定 で1件取得
dat = tbl.find('3238', "2021/02/03")

# 結果は常にリストで返却される。データが存在しない場合も、Noneではなく、空リストが返却される。
print(len(dat))

# HASH のみ指定。複合テーブルの場合、パーティションのデータが昇順で取得される。
# 単一キーテーブルの場合、1件取得される。
dat = tbl.find('3238')

# query(降順)
dat = tbl.find('3238', asc=False)

# queryの別のオプションも指定可能
dat = tbl.find('3238', option={"Limit": 2})

# Listで戻ってくる
print(dat[0])
```

## 認証情報、オプションの指定

DymDao は boto3 の上位ラッパーであり、AWS接続の資格情報検索については boto3 のメカニズムをそのまま継承します。 

具体的には以下の優先順に従います。

1. クライアント生成時のパラメータ、Configオブジェクト
2. 環境変数
3. ~/.aws/config ファイル

詳細は boto3 のドキュメントを参照してください。
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

DymDao の生成時に指定した認証情報、その他パラメータは、そのまま boto3 の resource、client の生成に引き継がれます。

```python
dao = DymDao(
    aws_access_key_id="your_access_key_id",
    aws_secret_access_key="your_secret_access_key",
    region_name="your_region"
)
```