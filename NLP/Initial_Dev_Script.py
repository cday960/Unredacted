import json
from decouple import config
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, CategoriesOptions, ConceptsOptions, KeywordsOptions


API_KEY = config('NLP_API_KEY')
API_URL = config('NLP_API_URL')
SAMPLE_TEXT_TO_ANALYZE = ''

with open('NLP/SAMPLE_TEXT.txt','r') as file:
    text = " ".join(line.rstrip() for line in file)
    SAMPLE_TEXT_TO_ANALYZE = text
    
authenticator = IAMAuthenticator(API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(API_URL)

response = natural_language_understanding.analyze(
    text=SAMPLE_TEXT_TO_ANALYZE,
    features=Features(entities=EntitiesOptions(sentiment=True,limit=30), categories=CategoriesOptions(limit=10), concepts=ConceptsOptions(limit=10), keywords=KeywordsOptions(limit=20))).get_result()

print(json.dumps(response, indent=2))