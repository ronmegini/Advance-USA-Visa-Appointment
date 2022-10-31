from selenium.webdriver.chrome.options import Options
import boto3
from botocore.exceptions import ClientError


def set_chrome_options() -> None:
    """
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    print("--- set_chrome_options ---")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def get_secret(secret_name, key):
    """
    Get secret content from aws Secret Manager

    :secret_name: (str) secret name
    :key: (str) specify the key that you want to get his value

    :return:
    :secret: (str) key's secret value
    """
        
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    value = secret[key]
    
    return value