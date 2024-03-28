import json
import boto3

lex = boto3.client("lex-runtime")
opensearch_client = boto3.client("opensearch")


def lambda_handler(event, context):
    query = event["query"]

    # Disambiguate query using Amazon Lex
    lex_response = lex.post_text(
        botName="PhotoAlbumBot", botAlias="$LATEST", userId="Mar", inputText=query
    )

    keywords = []
    if "slots" in lex_response:
        keywords = lex_response["slots"].values

    # Search OpenSearch only if keywords were returned from Amazon Lex
    if keywords:
        opensearch_response = opensearch_client.search(
            index="photos",
            body={"query": {"multi_match": {"query": keywords, "fields": ["labels"]}}},
        )

        return {"statusCode": 200, "body": json.dumps(opensearch_response)}

    # If no keywords were returned, return an empty response
    else:
        return {"statusCode": 200, "body": json.dumps("No results found.")}
