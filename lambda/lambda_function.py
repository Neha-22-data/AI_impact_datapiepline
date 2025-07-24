import boto3
import pandas as pd
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        
        # Get bucket and file name from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
    
        # Read CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))
    
        # Clean: Drop rows with missing values
        df = df.dropna(subset=['Country', 'Industry', 'AI Adoption Rate (%)'])
    
        # Convert and rename columns
        df['ImpactScore'] = df['AI Adoption Rate (%)'].round().astype(int)
        df = df.rename(columns={'Industry': 'ConsumerIndustry'})
    
        # Filter rows with ImpactScore >= 50
        df_filtered = df[df['ImpactScore'] >= 50]
    
        # Transformations
        avg_score = df_filtered.groupby('Country')['ImpactScore'].mean().reset_index()
        count_industry = df_filtered['ConsumerIndustry'].value_counts().reset_index()
        count_industry.columns = ['ConsumerIndustry', 'Count']
        max_score = df_filtered.groupby('ConsumerIndustry')['ImpactScore'].max().reset_index()
    
        # Save cleaned and summary CSVs to memory
        cleaned_csv = df_filtered.to_csv(index=False)
        summary_df = pd.concat([avg_score, count_industry.set_index('ConsumerIndustry'), max_score.set_index('ConsumerIndustry')], axis=1).reset_index()
        summary_csv = summary_df.to_csv(index=False)
    
        # Define output filenames
        cleaned_key = key.replace('.csv', '_cleaned.csv')
        summary_key = key.replace('.csv', '_summary.csv')
    
        # Upload files to S3
        s3.put_object(Bucket=bucket, Key=cleaned_key, Body=cleaned_csv)
        s3.put_object(Bucket=bucket, Key=summary_key, Body=summary_csv)
    
        return {
            'statusCode': 200,
            'body': 'Processing complete and files uploaded.'
        }
    except Exception as e:
        return {
            'statusCode' : 500,
            'body' : f'Error : {str(e)}'
            }
