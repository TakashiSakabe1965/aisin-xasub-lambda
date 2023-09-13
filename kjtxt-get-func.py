#
#       title  kjtxt 工場変換サブルーチン kjtxt-get-func
#       create 2023/9/12
#       author Takashi Sakabe
#   
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('kjtxt-translate-tb')

#リクエストパラメータでIDが指定される場合、該当IDのユーザ情報を取得して返す

def get_kjtxt(Hheaders,skj):

# dynamodb テーブル読み込み

    dynamoDBResponse = table.get_item(
        Key={
             'skj': skj
        }
    )

    if "Item" in dynamoDBResponse:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps(dynamoDBResponse['Item'])
        }
    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("record not found")
        }

#リクエストパラメータでIDが指定されない場合、全ユーザ情報を取得して返す

def get_kjtxts(Hheaders):

#  dynamodb 全テーブル読み込み

    dynamoDBResponse = table.scan()
    if not dynamoDBResponse['Items']:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("record not found")
        }
    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps(dynamoDBResponse['Items'])
        }       

#   Lambda Handler event and context 受信リクエスト

def lambda_handler(event, context):
#    print(event['queryStringParameters']['skj'])
    query_params = event.get('queryStringParameters')

#   リクエストパラメーターが指定されているか？

    if query_params == None:
        return get_kjtxts(event['headers'])
    else:
        return get_kjtxt(event['headers'],event['queryStringParameters']['skj'])