import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

lexClient = boto3.client("lexv2-runtime")
host = 'search-cloud-hw3-rjqzgwzppqcyrcgsmqdqftq3qq.aos.us-east-1.on.aws' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1'
service = 'aos'
auth = ('admin', 'Admin@12') 
opensearch_client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )


def getKeyWords(lexResponse):
    keywords = []
    interpretations = lexResponse['interpretations']
    for i in interpretations:
        if i['intent']['name'] == "SearchIntent":
            # print(i)
            for j in i['intent']['slots'].values():
                if j:
                    a = j['value']['interpretedValue']
                    if a:
                        keywords.append(a)
    return keywords
                
    

def queryElasticSearch(keywords):
    joined = "-".join(keywords)
    query = {
        "query": {
            "multi_match": {
            "query": joined,
            "fields": ["labels"]
            }
        }
    }

    response = opensearch_client.search(
        body = query,
        index = 'photos'
    )
    return response['hits']['hits']

def convertToURLS(objects):
    urls = set()
    for i in objects:
        url = "https://" + i["_source"]['bucket'] + ".s3.us-east-1.amazonaws.com/" + i["_source"]['objectKey']
        urls.add(url)
    
    return urls
        

def lambda_handler(event, context):
    query = event['query']

    response = lexClient.recognize_text(
        botId="DG5VY8N0AZ",
        botAliasId="TSTALIASID",
        localeId="en_US",
        sessionId="test",
        text=query,
    )
    keywords = getKeyWords(response)
    
    totalHits = queryElasticSearch(keywords)
    if(len(totalHits)) > 0:
        urls = convertToURLS(totalHits)
        return {"results": True, "urls": list(urls)}
        
    else:
        return {"message": "No Results Found", "results": False}
