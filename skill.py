##############################
# Builders
##############################

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def statement_builder(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

##############################
# Intent Definitions
##############################

def intent_router(event, context):
    intent = event['request']['intent']['name']

    # custom intent
    if intent == "CryptoPriceIntent":
        return price_intent(event, context)

    # required intents
    if intent == "AMAZON.CancelIntent":
        return statement_builder("Cancel intent", "This is a cancellation")

    if intent == "AMAZON.HelpIntent":
        return statement_builder("Cancel intent", "This was cancelled")

    if intent == "AMAZON.StopIntent":
        return statement_builder("Stop intent", "You was stopped")

def price_intent(event, context):
    slots = event['request']['intent']['slots']
    token = slots['cryptocurrency'].get('value', None)

    try:
        price = get_price()
    except KeyError as ke:
        return statement_builder("Price intent", "invalid currency")
    except Exception as e:
        return statement_builder("Price intent", "something went wrong")

    return statement_builder("Price intent", "The price of {0} is ${1}".format(token, price))

##############################
# Lambda Handler
##############################

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return statement_builder("Welcome to Crypto Price", "Welcome to crypto price! You can start by asking me for a crypto token's value")

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
