import boto3
import inspect


class DymDao:
    def __init__(self, *args, **kwargs):
        self.db = boto3.resource('dynamodb', *args, **kwargs)
        self.client = boto3.client('dynamodb', *args, **kwargs)

    def table(self, table_name):
        return WrapTable(self, table_name)


class WrapTable:
    def __init__(self, dao, table_name):
        self.dao = dao
        self.table_name = table_name

        self.table = self.dao.db.Table(table_name)
        self.ddl = self.dao.client.describe_table(TableName=table_name)

        self.key = self.__get_key_name()
        self.__register_method()

    def __register_method(self):
        methods = inspect.getmembers(self.table, inspect.ismethod)
        for name, func in methods:
            setattr(self, name, self.__intercept(func))

    def __get_key_name(self):
        key_schema = self.ddl['Table']['KeySchema']

        hash_name = next((r['AttributeName'] for r in key_schema if r['KeyType'] == "HASH"), None)
        range_name = next((r['AttributeName'] for r in key_schema if r['KeyType'] == "RANGE"), None)
        return hash_name, range_name

    @staticmethod
    def __intercept(method):
        def _m(*args, **kwargs):
            ret = method(*args, **kwargs)
            return WrapTable.pick_out_item(ret)
        return _m

    @staticmethod
    def pick_out_item(obj):
        if type(obj) == dict:
            if 'Item' in obj:
                return obj['Item']
            if 'Items' in obj:
                items = []
                for row in obj['Items']:
                    items.append(row['Item'] if type(row) == dict and 'Item' in row else row)
                return items
        return obj

    def find(self, hash_value, range_value=None, asc=True, option=None):
        hash_name, range_name = self.key
        opt = option if option is not None else {}

        if range_value is not None:
            key_param = {hash_name: hash_value, range_name: range_value}
            ret = self.table.get_item(Key=key_param, **opt)
            ret = self.pick_out_item(ret)

            return [ret] if ret is not None else []
        else:
            query_params = {
                "TableName": self.table_name,
                "KeyConditionExpression": "#a = :val",
                "ExpressionAttributeValues": {":val": hash_value},
                "ExpressionAttributeNames": {"#a": hash_name},
                "ScanIndexForward": asc,
            }
            query_params.update(opt)

            ret = self.table.query(**query_params)
            return self.pick_out_item(ret)
