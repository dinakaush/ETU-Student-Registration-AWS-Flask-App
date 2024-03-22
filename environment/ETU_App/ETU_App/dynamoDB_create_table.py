import boto3

import key_config as keys



dynamodb_client = boto3.client(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
s3 = boto3.client(
    's3', 
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)



def create_table():
   table = dynamodb_resource.create_table(
       TableName = 'ETU_Students', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'email',
               'KeyType'      : 'HASH' #RANGE = sort key, HASH = partition key
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'email', # Name of the attribute
               'AttributeType': 'S'   # N = Number (B= Binary, S = String)
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table
   
def update(email, data:dict, resource):
    #
    ETU_Students= resource.Table('ETU_Students')
    response = ETU_Students.update_item(
        #
        Key = {
           'email': email
        },
        AttributeUpdates={
            
            'name': {
               'Value'  : data['name'],
               'Action' : 'PUT' 
            },
            'reg_num': {
               'Value'  : data['reg_num'],
               'Action' : 'PUT'
            },
            'password': {
               'Value'  : data['password'],
               'Action' : 'PUT' 
            },
            'degree': {
               'Value'  : data['degree'],
               'Action' : 'PUT'
            },
            'contact': {
               'Value'  : data['contact'],
               'Action' : 'PUT' 
            },
            'intro': {
               'Value'  : data['intro'],
               'Action' : 'PUT'
            },
            'cgpa': {
               'Value'  : data['cgpa'],
               'Action' : 'PUT'
            },
            'skills': {
               'Value'  : data['skills'],
               'Action' : 'PUT'
            }
        },
        
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    
    return response

def get_info(reg_num,resource):
    #
    
    ETU_Students=resource.Table('ETU_Students')
    response = ETU_Students.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('reg_num').eq(reg_num)
    )
    return response

