import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

s3 = boto3.client("s3")
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
    custom_labels = s3_object.get("Metadata", {}).get("customlabels", "")
    custom_labels = custom_labels.split(",")
    # Append Rekognition labels
    for label in response["Labels"]:
        custom_labels.append(label["Name"])
        
    print(custom_labels)
    # Store in ElasticSearch
    host = 'search-cloud-hw3-rjqzgwzppqcyrcgsmqdqftq3qq.aos.us-east-1.on.aws' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
    auth = ('admin', 'Admin@123') 

    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )
    
    response = client.index(
            index = 'photos',
            body = {
                "objectKey": key,
                "bucket": bucket,
                "createdTimestamp": s3_object["LastModified"],
                "labels": custom_labels,
                },
        )
    
    print(response)