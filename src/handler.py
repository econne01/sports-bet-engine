import boto3

def write_odds_handler(event, context):
    bucket_name = 'sports-bet'
    file_name = 'todays_odds.csv'
    s3_path = file_name

    # First read current file
    s3Client = boto3.client("s3")
    orig_file = s3Client.get_object(Bucket=bucket_name, Key=s3_path)
    data = str(orig_file['Body'].read())
    for row in data.split('\n'):
        print(row)

    # Then write today's odds to file
    string = "TODAYS ODDS PLACEHOLDER TEXT"
    encoded_string = (data + '\n' + string).encode("utf-8")

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)

if __name__ == '__main__':
    write_odds_handler('', '')
