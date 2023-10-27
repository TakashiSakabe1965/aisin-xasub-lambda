#
#       title  kjtxt 工場変換サブルーチン kjtxt-put-func
#       create 2023/9/12
#       author Takashi Sakabe  
#
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('kjtxt-translate-tb')

# リクエストパラメーターsjkでjjkを更新する 
 
def put_kjtxt(Hheaders,requestJSON):

# dynamadb テーブル重複判定
    dynamoDBResponse = table.get_item(
        Key={
                 'skj': requestJSON['skj']
        }
    )

    if "Item" not in dynamoDBResponse:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("record not found")
        }

#  dynamoｄb テーブルの更新処理

    dynamoDBResponse = table.update_item(
        Key={
            'skj': requestJSON['skj']
        },
        UpdateExpression="set #jkj = :newjkj",
        ExpressionAttributeNames= {
            '#jkj' : 'jkj'
        },
        ExpressionAttributeValues={
            ':newjkj': requestJSON['jkj']
        }
    )

#  dynamodb テーブル更新処理判定 

    if dynamoDBResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps("record update successful")
        }
    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("dynamodb error")
        }

#   Lambda Handler event and context 受信リクエスト 
	
def lambda_handler(event, context):
    print(event)
    requestJSON = json.loads(event['body'])  
    return put_kjtxt(event['headers'],requestJSON)
#    print(event)
#    return put_kjtxt(event['headers'],event['body'])
