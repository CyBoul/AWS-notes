# The Lambda handler is the first function that executes in your code.
def lambda_handler(event, context):
    
    # context – to provide runtime information to your handler.
    # event – to pass in event data to the handler.
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
        feeling = "positive"

    elif emoji_type == 1:
        feeling = "neutral"

    else:
        feeling = "negative"
        
    # Optionally, the handler can return a value.
    # Synchronous execution == we need to create a response
    response = {
        "message": message,
        "feeling": feeling,
    }
    
    return response


''' Test with :
{
	"emoji_type": 0,
	"message": "I love the park"
}


