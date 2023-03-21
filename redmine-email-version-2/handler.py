from redminelib import Redmine
import boto3
import urllib3
import json
import html2text

def lambda_handler(event, context):
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    #get_last_modified='4t5rm5guuobhjasr4ij9l9e6usbasnitqj8k6v81'
    s3 = boto3.client('s3')
    
    objs = s3.list_objects(Bucket='redmine-email-integration')['Contents']
    length = len(objs)-1
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][length]
    #last_added = '0menrubhvc77smqdhve290h6cm23qvpgk3knmh81'
    print(last_added)
    
    file_content = s3.get_object( Bucket='redmine-email-integration', Key=last_added)["Body"].read()
    content = file_content.decode('UTF-8')
    
    content_array = content.split("\n")

    lengt = len(content_array)


    #Finding the start line number of the description
    for lines in range(len(content_array)):
        word_one = "text/plain;"
        if word_one in content_array[lines]:
            lowercount = lines            
    print(lowercount)
    
    #Finding the end line number of the description       
    for lines in range(len(content_array)):
        word_two="text/html"
        if word_two in content_array[lines]:
            uppercount=lines  
        else:
            uppercount=len(content_array)
    print(uppercount)
            
      
    # parsing the description according to the line numbers
    print('Description : \n')
    body_1 = ' '
    for i in range(lowercount+1,uppercount-1):
        body_1=body_1+content_array[i]
    #print(body_1,'\n')
    
    #removing the html language
    body_1=html2text.html2text(body_1)
    print(body_1)
    
        
    # Findig the sender_domain  
    for lines in content_array:
        line_array = lines.split(" ")
        if line_array[0] == "Return-Path:":
            at=lines.split('@')
            if at[-1]=='bizcloudexperts.com>\r':
                sender_domain = 2
            else:
                sender_domain= 1
            print(sender_domain)
    
           
    #Finding the sender
    for lines in content_array:
        line_array = lines.split("\n")
        word="From:"
        for i in range(len(line_array)):
            if word in line_array[i]:
                sender=line_array[i]
            break
    print(sender)
    c=0
    for i in sender:
        c=c+1
        if i=='<':
            index=c
            to_address=sender[index:len(sender)-2]
        else:
            index=sender
            to_address=sender
    print(index)
    print(to_address)
    
              
    #Finding the subject of the mail
    for lines in content_array:
        line_array = lines.split(" ")
        if line_array[0] == "Subject:":
            subject=' '
            for i in range(1,len(line_array)):
                subject=subject+line_array[i]+' '
    print(subject[1:])
    #print(subject[1:].startswith("Re:"))
    
            
    #addidng sender to description 
    body=body_1+"\n"+sender
            
            
    #Default Priority
    default_priority = 5
    
    redmine = Redmine('https://agiledev.bizcloudexperts.com', key='key')
    user = redmine.auth()
    
    if subject[1:].startswith("Re:"):
        print('in')
        subject_1 = subject[5:]
        print(subject_1)
        try:
            print("Updating already existing ticket, subject Re:")
            ticket_details=list(redmine.issue.search(subject_1, project_id=72, open_issues=True))
            print(ticket_details)
            print(len(ticket_details))
            ticket_details[0]=str(ticket_details[0])
            print(str(ticket_details[0]))
            ticket=ticket_details[0].split("#")
            print(ticket)
            ticket_number = ticket[1][0:5]
            print(ticket_number)
            redmine.issue.update(ticket_number, description=body)
        except:
            print('new ticket with Re:')
            new_ticket=redmine.issue.create(
            project_id=72,
            subject=subject_1,
            description=body,
            priority_id=default_priority,
            custom_fields=[{'id':1,'value':2}] )
            ticket_id = new_ticket.id 
            ticket_id=str(ticket_id)
            
            ticket_id = new_ticket.id            #ticket_id

            ticket_id=str(ticket_id)
            
            #sending alerts to slack-channel
            message = 'A ticket is created with the #' + ticket_id + ' number. Link: https://agiledev.bizcloudexperts.com/issues/' + ticket_id
            http = urllib3.PoolManager()
            url ="slack_url"
            msg = {
            "channel": "#bizcloud-support",
            "username": "WEBHOOK_USERNAME",
            "text": message
            }
            encoded_msg = json.dumps(msg).encode('utf-8')
            resp = http.request('POST',url, body=encoded_msg)
        
    else:
        try:
            print("updating already existing new ticket")
            ticket_details=list(redmine.issue.search(subject, project_id=72, open_issues=True))
            ticket_details[0]=str(ticket_details[0])
            print(str(ticket_details[0]))
            ticket=ticket_details[0].split("#")
            print(ticket)
            ticket_number = ticket[1][0:5]
            print(ticket_number)
            redmine.issue.update(ticket_number, description=body)
        except:
            print("new ticket")
            new_ticket=redmine.issue.create(
                project_id=72,
                subject=subject,
                description=body,
                priority_id=default_priority,
                custom_fields=[{'id':1,'value':2}] )
                
            ticket_id = new_ticket.id 
            ticket_id=str(ticket_id)
            
            
            #sending alerts to slack-channel
            message = 'A ticket is created with the #' + ticket_id + ' number. Link: https://agiledev.bizcloudexperts.com/issues/' + ticket_id
            http = urllib3.PoolManager()
            url ="slack_url"
            msg = {
            "channel": "#bizcloud-support",
            "username": "WEBHOOK_USERNAME",
            "text": message
            }
            encoded_msg = json.dumps(msg).encode('utf-8')
            resp = http.request('POST',url, body=encoded_msg)
            
            

