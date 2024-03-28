import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

s3 = boto3.client("s3")
opensearch_client = OpenSearch(
    hosts=[{"host": "opensearch-host"}],  # dummy value, replace with actual one later
    http_auth=(
        "es_user",
        "pass",
    ),  # dummy variables now, replace with actual values later
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

rekognition = boto3.client("rekognition")


def lambda_handler(event, context):
    # Get S3 object from event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(bucket, key)

    # Detect labels using Rekognition
    response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}, MaxLabels=10
    )

    # Get S3 metadata
    s3_object = s3.head_object(Bucket=bucket, Key=key)
    custom_labels = s3_object.get("Metadata", {}).get("customLabels")
    if not custom_labels:
        custom_labels = []
    else:
        custom_labels = json.loads(custom_labels)

    # Append Rekognition labels
    for label in response["Labels"]:
        custom_labels.append(label["Name"])

    # Store in ElasticSearch
    opensearch_client.index(
        index="photos",
        body={
            "objectKey": key,
            "bucket": bucket,
            "createdTimestamp": s3_object["LastModified"],
            "labels": custom_labels,
        },
    )

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
