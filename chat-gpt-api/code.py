import json
import openai

def lambda_handler(event, context):

    body = event["body"]
    
    #sampl = json.dumps(body)
    body = json.loads(body)
    print(body)
    
    #model= "davinci"-powerfull
    #model='curie' - fast
    #input= "What day of the week is it?"
    #instruction= "what is docker"
    
    openai.api_key = "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"
    
    completion = openai.Completion.create(
        engine=body['model'],
        prompt=body['instruction'],
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    a=completion.choices[0].text.split('\n')
    print(a)

    return {
        'statusCode': 200,
        'body':a[2] +a[4] +a[6]
    }
    
