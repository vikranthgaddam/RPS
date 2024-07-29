import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from flask import current_app


# Load AWS credentials from environment variables
def get_aws_client():
    aws_access_key_id = current_app.config['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = current_app.config['AWS_SECRET_ACCESS_KEY']
    aws_region = current_app.config['AWS_REGION']
    print("This is aws secret",aws_secret_access_key)
    print("This is aws region",aws_region)

    return boto3.resource('dynamodb',
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

def send_data_to_aws(rounds, ip_address):
    """
    Send game data to AWS DynamoDB using batch write.
    
    :param rounds: List of GameRound objects
    :param ip_address: IP address of the player
    :return: True if successful, False otherwise
    """
    table_name = 'Game_Round'
    dynamodb=get_aws_client()
    table = dynamodb.Table(table_name)
    game_id = str(uuid.uuid4())  # Generate a unique game ID

    try:
        with table.batch_writer() as batch:
            for round in rounds:
                item = {
                    'game_id': game_id,
                    'round_id': str(uuid.uuid4()),  # Unique identifier for each round
                    'timestamp': round.timestamp.isoformat(),
                    'player_choice': round.player_choice,
                    'ai_choice': round.ai_choice,
                    'winner': round.winner,
                    'model_used': round.model_used,
                    'ip_address': ip_address
                }
                batch.put_item(Item=item)
        
        print(f"Successfully sent {len(rounds)} rounds to DynamoDB for game {game_id}")
        return True, game_id

    except ClientError as e:
        print(f"Error sending data to DynamoDB: {e.response['Error']['Message']}")
        return False, None
