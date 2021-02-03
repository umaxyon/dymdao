# DymDao

AWS のDynamoDBの記述を簡単にして、気軽に使えるようにするboto3のラッパーライブラリ。

## Features

* 「get_item」と「query」を使い分けなくて良くなる「find」メソッドが追加される。
* 常に結果がListで戻ってくる
* キー名を指定する必要が無くなる
* 既存のboto3のメソッドはそのまま利用できる

## Usage

```python
from src.dymdao import DymDao

dao = DymDao()
tbl = dao.table('tbl_hogehoge')  # HASH、RANGE両方定義された複合テーブル

# HASH、RANGE 両指定(get_item実行)
dat = tbl.find('3238', range_value="2021/02/03")

# HASH のみ指定(query実行)
dat = tbl.find('3238')

# query(降順)
dat = tbl.find('3238', asc=False)

# 別のオプションも指定可能
dat = tbl.find('3238', option={"Limit": 2})

# Listで戻ってくる
print(dat[0])

# 既存のメソッドもそのまま使える
dat = tbl.get_item(Key={'mykey': '3238', 'row': '2021/02/03'})

# 「dat["Item"]」とか「dat["Items"]」とか書かなくていい
print(dat)
```