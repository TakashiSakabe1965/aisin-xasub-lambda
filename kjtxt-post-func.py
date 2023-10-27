#
#       title  kjtxt 工場変換サブルーチン kjtxt-post-func
#       create 2023/9/12
#       author Takashi Sakabe  
#
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('kjtxt-translate-tb')

#  リクエストパラメーターskj,jkjでレコードを追加する

def post_kjtxt(Hheaders,requestJSON):

#   dynamoDB 　テーブル重複判定

    dynamoDBResponse = table.get_item(
        Key={
             'skj': requestJSON['skj']
        }
    )

    if "Item" in dynamoDBResponse:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': Hheaders,
            'body': json.dumps("record already exists")
        }

#  dynamoDB テーブル追加

    dynamoDBResponse = table.put_item(Item={'skj': requestJSON['skj'], 'jkj': requestJSON['jkj']})

#  dynamoDB テーブル追加　処理判定

    if dynamoDBResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': Hheaders,
            'body': json.dumps("record add successful")
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
    return post_kjtxt(event['headers'],requestJSON)
    
