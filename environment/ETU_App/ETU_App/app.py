
from flask import Flask, render_template, request
import key_config as keys
import boto3 
import logging
from botocore.exceptions import ClientError
import dynamoDB_create_table as dynamodb_ct

app = Flask(__name__)


dynamodb = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    #dynamodb_ct.create_table()
    #return 'Table Created'
    return render_template('index.html')

@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form["name"]
        reg_num = request.form["reg_num"]
        email = request.form["email"]
        password = request.form["password"]
        degree = request.form["degree"]
        contact = request.form["contact"]
        intro = request.form["intro"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]
        
        table = dynamodb.Table('ETU_Students')
        
        table.put_item(
                Item={
        'name': name,
        'reg_num' : reg_num,
        'email' : email,
        'password' : password,
        'degree' : degree,
        'contact' : contact,
        'intro' : intro,
        'cgpa' : cgpa,
        'skills' : skills
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login.html',msg = msg)
    return render_template('index.html')
    
@app.route('/login')
def login():    
    return render_template('login.html')


@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('ETU_Students')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        reg_num = items[0]['reg_num']
        email = items[0]['email']
        password = items[0]['password']
        degree = items[0]['degree']
        contact = items[0]['contact']
        intro = items[0]['intro']
        cgpa = items[0]['cgpa']
        skills = items[0]['skills']
        if password == items[0]['password']:
            
            return render_template("home.html",name = name, reg_num=reg_num, email=email, password=password, degree=degree, contact=contact, intro=intro, cgpa=cgpa, skills=skills)
    return render_template("login.html")
    
@app.route('/home')
def home():
    return render_template('home.html')
    
    
@app.route('/update', methods=['POST'])
def update_table():

    data = request.form
    reg_num=data.get('email')
    
    response= dynamodb_ct.update(reg_num,data,dynamodb)
    

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    } 
    

@app.route('/upload', methods=['POST'])
def create_bucket(etu_students, region=None):
    
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=etu_students)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=etu_students,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Upload the file to S3
        try:
            s3.upload_fileobj(file, etu-bucket, file.filename)
        except NoCredentialsError:
            return 'AWS Credentials not available.'

        # Get the public access URL of the uploaded file
        url = f'https://{etu-bucekt}.s3.{aws_region}.amazonaws.com/{file.filename}'

        # Store the URL in DynamoDB
        reg_num = 'reg_num'  # You should replace this with the actual username
        dynamo.tables['ETU_Students'].put_item(Item={'reg_num': reg_num, 'profile_picture_url': url})

        return 'Upload successful!'






@app.route('/profile/<reg_num>', methods=['GET'])
def get_info(reg_num):
    response = dynamodb_ct.get_info(reg_num,dynamodb)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        items = response['Items']
        name = items[0]['name']
        reg_num = items[0]['reg_num']
        email = items[0]['email']
        password = items[0]['password']
        degree = items[0]['degree']
        contact = items[0]['contact']
        intro = items[0]['intro']
        cgpa = items[0]['cgpa']
        skills = items[0]['skills']
        if password == items[0]['password']:
            return render_template("profile.html",name = name, reg_num=reg_num, email=email, password=password, degree=degree, contact=contact, intro=intro, cgpa=cgpa, skills=skills)
    return render_template("login.html")

   




if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
