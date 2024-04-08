import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

lexClient = boto3.client("lexv2-runtime")
opensearch_client = boto3.client("opensearch")


def lambda_handler(event, context):
    print(event)
    print("context")
    print(context)
    query = event["query"]

    # Disambiguate query using Amazon Lex
    # lex_response = lexClient.post_text(
    #     botName="PhotoAlbumBot", botAlias="$LATEST", userId="Mar", inputText=query
    # )
    
    response = lexClient.recognize_text(
                botId = "DG5VY8N0AZ",
                botAliasId = "TSTALIASID",
                localeId = "en_US",
                sessionId = "test",
                text = query,
            )
    print(response)
    keywords = []
    # if "slots" in lex_response:
    #     keywords = lex_response["slots"].values

    # # Search OpenSearch only if keywords were returned from Amazon Lex
    # if keywords:
    #     opensearch_response = opensearch_client.search(
    #         index="photos",
    #         body={"query": {"multi_match": {"query": keywords, "fields": ["labels"]}}},
    #     )

    #     return {"statusCode": 200, "body": json.dumps(opensearch_response)}

    # # If no keywords were returned, return an empty response
    # else:
    #     return {"statusCode": 200, "body": json.dumps("No results found.")}
