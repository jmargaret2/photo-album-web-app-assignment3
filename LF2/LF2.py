import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

lexClient = boto3.client("lexv2-runtime")

opensearch_client = OpenSearch(
    hosts=[{"host": "search-cloud-hw3-rjqzgwzppqcyrcgsmqdqftq3qq.aos.us-east-1.on.aws"}],
    http_auth=(
        "admin",
        "Admin@12",
    ),  # dummy variables now, replace with actual values later
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


def lambda_handler(event, context):
    print(event)

    print(f"context: {context}")
    user_id = event["userId"]
    
    session_id = event["sessionId"]

    query = event["currentIntent"]["slots"]["keyword"]

    print(f"query: {query}")

    response = lexClient.recognize_text(
        botId="DG5VY8N0AZ",
        botAliasId="TSTALIASID",
        localeId="en_US",
        sessionId=session_id,
        text=query,
    )
    print(f"response {response}")

    keywords = response["sessionState"]["intent"]["slots"]["keyword"]["value"]["originalValue"]

    if keywords:
        print(keywords)

        print("starting to search OpenSearch")
        response = opensearch_client.search(
            index="photos", body={"query": {"match": {"field": query}}}
        )

        return {"message": "Searched OpenSearch"}

    else:
        # return empty array of results
        response = []
        return {"message": "Search contained no keywords"}
