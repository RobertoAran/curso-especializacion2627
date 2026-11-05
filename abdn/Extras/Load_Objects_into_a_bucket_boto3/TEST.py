import boto3
from InquirerPy import inquirer


def start_questions_list():
    answer = inquirer.select(
        message="What would you like to do?",
        choices=[
            'List Buckets',
            'List data from a bucket',
            #'Create Bucket',
            #'Copy Object to Bucket',
            'Exit'
        ]
    ).execute()
    return answer

def start_question_select_def_case(answer):
    print(answer)
    match answer:
        case "List Buckets":
            buckets = aws_list_buckets()
            buckets_viewer(buckets)
        case "List data from a bucket":
            buckets = aws_list_buckets()
            aws_list_objects_from_bucket(buckets)
        case 'Exit':
            print("See ya")
            exit(0)
    

def aws_list_buckets():
    s3_client = boto3.client('s3')

    array_buckets = []
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        bucket_arn = f"arn:aws:s3:::{bucket_name}"
        array_buckets.append({'Name': bucket_name, 'ARN': bucket_arn})
    return array_buckets

def buckets_viewer(buckets):
    for bucket in buckets:
        print("Name of bucket: " + bucket.get('Name'))

def aws_list_objects_from_bucket(buckets):
    bucket_names = [bucket.get('Name') for bucket in buckets]
    selected_bucket = inquirer.select(
        message="Select a bucket to list its objects:",
        choices=bucket_names
    ).execute()

    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=selected_bucket)

    if 'Contents' in response:
        print(f"Objects in bucket '{selected_bucket}':")
        for obj in response['Contents']:
            print(f" - {obj['Key']}")
    else:
        print(f"No objects found in bucket '{selected_bucket}'.")


if __name__ == "__main__":
    start_question_select_def_case(start_questions_list())