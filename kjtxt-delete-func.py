#
#       title  kjtxt 工場変換サブルーチン kjtxt-delete-func
#       create 2023/9/12
#       author Takashi Sakabe
#
import boto3
import json
import time
 
dynamodb = boto3.resource('dynamodb')
tableName = 'kjtxt-translate-tb'
table    = dynamodb.Table(tableName)
params    = {
    'TableName' : tableName,
    'KeySchema' : [
        {'AttributeName': 'skj','KeyType' : 'HASH'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'skj','AttributeType': 'S'}
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5 
    }
}

#リクエストパラメータでskjが指定される場合、該当skjのレコードを削除する

def delete_kjtxt(Hheaders,skj):

# dynamodb テーブル存在判定

    dynamoDBResponse = table.get_item(
        Key={
             'skj': skj
        }
    )
    
    if "Item" not in dynamoDBResponse:
            return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("Record not found")
            }
# dynamodb 該当テーブルの削除

    dynamoDBResponse = table.delete_item(
        Key={
            'skj': skj
        }
    )

    if dynamoDBResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps("")
        }
    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("DynamoDB error")
        }

#リクエストパラメータでskjが指定されない場合、全レコード削除する　 

def delete_kjtxts(Hheaders):

# dynamodb 全テーブル読み込み

    dynamoDBResponse = table.scan()
    items = dynamoDBResponse.get('Items', [])

    while 'LastEvaluatedKey' in dynamoDBResponse:
        dynamoDBResponse = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(dynamoDBResponse.get('Items', []))

# dynamodb 一件づつテーブル削除

    for item in items:
        table.delete_item(Key={'skj': item['skj']})

    if dynamoDBResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps("Delete succesfull")
        }
    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("DynamoDB error")
        }

#   Lambda Handler event and context 受信リクエスト 
	        
def lambda_handler(event, context):

    query_params = event.get('queryStringParameters')

#   リクエストパラメーターが指定されているか？

    if query_params == None:
        return delete_kjtxts(event['headers'])
    else:
        return delete_kjtxt(event['headers'],event['queryStringParameters']['skj'])
