- https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html
- https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
- https://docs.python.org/3/reference/compound_stmts.html#the-if-statement

``myLambdaTest`` using ``python 3.13``

### DIY
```python
# The Lambda handler is the first function that executes in your code.
def lambda_handler(event, context):
    
    # context – to provide runtime information to your handler.
    # event – to pass in event data to the handler.
    
    # When you invoke your Lambda function you can determine :
    # The content and structure of the event. 
    # The event structure varies by service.
    # 
    # "event" parameter has the following structure of name/value pairs:
    # {
    #     "emoji_type": number,
    #     "message": "string"
    # }
        
    emoji_type = event["emoji_type"]
    message = event["message"]

    print(emoji_type)
    print(message)
    
    custom_message = None
    feeling = None

    if emoji_type == 0:
        #custom_message = "Message for code 0: " + message
        feeling = "positive"

    elif emoji_type == 1:
        #custom_message = "Message for code 1: " + message
        feeling = "neutral"

    else:
        #custom_message = "Message for all other codes: " + message
        feeling = "negative"
        
    # Optionally, the handler can return a value.
    # In this lab we use synchronous execution, so we need to create a response
    response = {
        "message": message,
        #"custom_message": custom_message,
        "feeling": feeling,
    }
    
    return response
```

#### Test :
```json
{
	"emoji_type": 0,
	"message": "I love the park"
}
```

