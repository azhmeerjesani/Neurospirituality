import os
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from Neurospirituality.HiddenKeys import backblaze_keys

# Backblaze credentials
application_keys = backblaze_keys()
B2_BUCKET_NAME = application_keys[0]  # Replace with your bucket name
B2_APPLICATION_KEY_ID = application_keys[1]  # Replace with your Key ID
B2_APPLICATION_KEY = application_keys[2]  # Replace with your Application Key


def connect_to_backblaze():
    """Authenticates and connects to Backblaze B2."""
    info = InMemoryAccountInfo()  # Stores auth data in memory
    b2_api = B2Api(info)
    b2_api.authorize_account("production", B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY)
    return b2_api


def upload_directory_to_b2(local_directory, b2_bucket_name):
    """Uploads all files from a local directory to a Backblaze B2 bucket, preserving the structure."""
    b2_api = connect_to_backblaze()
    bucket = b2_api.get_bucket_by_name(b2_bucket_name)

    for root, _, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_directory)  # Preserve folder structure
            b2_file_path = relative_path.replace("\\", "/")  # Ensure forward slashes for B2 compatibility

            print(f"Uploading {local_file_path} to B2 as {b2_file_path}...")

            # Upload and overwrite if the file exists
            bucket.upload_local_file(
                local_file=local_file_path,
                file_name=b2_file_path
            )

    print("Upload complete.")


# Example usage
local_directory = r"C:\Users\azhme\OneDrive - Clear Creek ISD\Coding\Websites\Neurospirituality\templates"  # Change to your directory path
upload_directory_to_b2(local_directory, B2_BUCKET_NAME)
