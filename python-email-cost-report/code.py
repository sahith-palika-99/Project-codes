import json
import boto3
import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    billing_client = boto3.client('ce')
    # getting dates (yyyy-MM-dd) and converting to string 
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1) 
    str_today = str(today) 
    str_yesterday = str(yesterday)
    # connecting to cost explorer to get daily aws usage 
    response = billing_client.get_cost_and_usage( 
       TimePeriod={ 
         'Start': str_yesterday, 
         'End': str_today }, 
       Granularity='DAILY', 
       Metrics=[ 'UnblendedCost',] 
    )
    
    cost = response["ResultsByTime"][0]['Total']['UnblendedCost']['Amount']
    cost='$'+str(cost)
    message = 'Cost of AWS training account for yesterday was' 
    
    # create an SES client
    ses_client = boto3.client('ses', region_name='us-east-1')
    
    # create the HTML and CSS code for the email
    html = """
        <html>
          <head>
            <style>
              body {{
                font-family: Arial, sans-serif;
                background-color: black;
                color: white;
              }}
              h2 {{
                color: white;
                font-size: 25px;
                text-align: center;
          
              }}
              h1 {{
                color: #333333;
                font-size: 40px;
                text-align: center;
                background-color: yellow;
              }}
              p {{
                color: white;
                font-size: 30px;
                line-height: 1.5;
                margin-bottom: 20px;
                text-align: center;
              }}
            </style>
          </head>
          <body>
            <p> Training Account report for the day {} </p>
            <h2> {}  </h2>
            <h1><strong> <em>{}</em></strong> </h1>
          </body>
        </html>
        """.format(str_yesterday,message,cost)

    # create the message
    message = {
        'Subject': {'Data': 'AWS training account cost report'},
        'Body': {'Html': {'Data': html}}
    }
    
    response = ses_client.send_email(
        Source='sahithpalika@cloudangles.com',
        Destination={'ToAddresses': ['jayasree.gundasu@cloudangles.com', 'sahithpalika@cloudangles.com']},
        Message=message
    )
    
    if today.weekday() == 1:
        week = today - datetime.timedelta(days = 7) 
        str_week = str(week)
        # connecting to cost explorer to get daily aws usage 
        response = billing_client.get_cost_and_usage( 
           TimePeriod={ 
             'Start': str_week, 
             'End': str_today }, 
           Granularity='MONTHLY', 
           Metrics=[ 'UnblendedCost',] 
        )
        
        cost = response["ResultsByTime"][0]['Total']['UnblendedCost']['Amount']
        cost='$'+str(cost)
        message = 'Cost of AWS training account for the week was' 
        
        # create an SES client
        ses_client = boto3.client('ses', region_name='us-east-1')
        
        # create the HTML and CSS code for the email
        html = """
            <html>
              <head>
                <style>
                  body {{
                    font-family: Arial, sans-serif;
                    color: white;
                    background-color: black;
                  }}
                  h2 {{
                    color: white;
                    font-size: 25px;
                    text-align: center;
                  }}
                  h1 {{
                    color: #333333;
                    font-size: 40px;
                    text-align: center;
                    background-color: yellow;
                  }}
                  p {{
                    color: white;
                    font-size: 30px;
                    line-height: 1.5;
                    margin-bottom: 20px;
                    text-align: center;
                  }}
                </style>
              </head>
              <body>
                <p> Training Account report for the week {} to {} </p>
                <h2> {} </h2>
                <h1> <strong> <em> {} </em></strong> </h1>
              </body>
            </html>
            """.format(str_week,str_today,message,cost)
    
        # create the message
        message = {
            'Subject': {'Data': 'AWS training account cost report'},
            'Body': {'Html': {'Data': html}}
        }
        
        response = ses_client.send_email(
            Source='sahithpalika@cloudangles.com',
            Destination={'ToAddresses': ['jayasree.gundasu@cloudangles.com', 'sahithpalika@cloudangles.com']},
            Message=message
        )
