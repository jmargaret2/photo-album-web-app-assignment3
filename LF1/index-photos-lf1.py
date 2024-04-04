import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

s3 = boto3.client("s3")
opensearch_client = OpenSearch(
    hosts=[{"host": "https://search-cloud-hw3-rjqzgwzppqcyrcgsmqdqftq3qq.aos.us-east-1.on.aws"}],  # dummy value, replace with actual one later
    http_auth=(
        "admin",
        "Admin@12",
    ),  # dummy variables now, replace with actual values later
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

rekognition = boto3.client("rekognition")


def lambda_handler(event, context):
    # Get S3 object from event
    print(event)
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(bucket, key)

    # Detect labels using Rekognition
    response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}, MaxLabels=10
    )
    print(response)
    
    # Get S3 metadata
    s3_object = s3.head_object(Bucket=bucket, Key=key)
    custom_labels = s3_object.get("Metadata", {}).get("customLabels", [])
    if not custom_labels:
        custom_labels = []
    else:
        custom_labels = json.loads(custom_labels)

    # Append Rekognition labels
    for label in response["Labels"]:
        custom_labels.append(label["Name"])
    print(custom_labels)
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


print("hii")
a = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2024-04-04T02:44:51.012Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AROA3FLDXQ2HL5XE4YLJC:BackplaneAssumeRoleSession'}, 'requestParameters': {'sourceIPAddress': '44.210.65.185'}, 'responseElements': {'x-amz-request-id': '6E1BXBVT6T1Y596Z', 'x-amz-id-2': 'PUddi071LjZAPLbmzYe/H6XIdEvQIG8sz4RAuTJxQeZbhjtkUQW2Db616vKt5+C0ZuhOknMyCVn/P1Ui153jLzGTxyGqDqxV'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '895b18b0-67c1-4657-8baa-280d5d7e8642', 'bucket': {'name': 'ccbigdata-assignment3-b2', 'ownerIdentity': {'principalId': 'A14NYF1MZS6C3Y'}, 'arn': 'arn:aws:s3:::ccbigdata-assignment3-b2'}, 'object': {'key': 'images/test.jpg', 'size': 406004, 'eTag': '874a2510f4bd2d1438acc69c1ce94432', 'sequencer': '00660E1422DDD61613'}}}]}
lambda_handler(a, [])