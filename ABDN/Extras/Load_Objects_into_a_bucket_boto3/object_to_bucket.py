import Boto3

bucketName = "bucket-name"
s3_client = boto3.client('s3')

bucket_copy_spot=""
filet_to_copy = ""

def bucket_name_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except Exception as e:
        print(f"Bucket {bucket_name} does not exist or you do not have access: {e}")
        return False

def create_bucket(bucket_name):
    try:
        response = s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
        return response['Location']
    except Exception as e:
        print(f"Error creating bucket {bucket_name}: {e}")
        return None

if __name__ == "__main__":
    bucket_name = bucketName

    bucket_arn = bucket_name_exists(bucket_name)
    if bucket_arn:
        copy_object_to_bucket(bucket_arn, filet_to_copy, bucket_copy_spot)
    else:
        bucket_arn = create_bucket(bucket_name)
        copy_object_to_bucket(bucket_arn, filet_to_copy, bucket_copy_spot)

    
    