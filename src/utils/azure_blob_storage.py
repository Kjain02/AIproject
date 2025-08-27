from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
import os, sys
sys.path.append(os.path.abspath(os.path.join('../..')))

from src.azure_credentials import *
from azure.storage.blob import BlobClient

# Set up your Azure Storage details
STORAGE_ACCOUNT_NAME = AZURE_STORAGE_ACCOUNT_NAME
CONTAINER_NAME = AZURE_STORAGE_CONTAINER_NAME
SAS_TOKEN = AZURE_STORAGE_SAS_TOKEN

# Create the BlobServiceClient
blob_service_client = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/?{SAS_TOKEN}"
)

# Reference to the container client
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def download_blob_from_uri(uri, download_file_path):
    """
    Downloads a blob from Azure Blob Storage using its URI to a local file.
    :param uri: Full URI of the blob (including SAS token).
    :param download_file_path: Path to save the downloaded file.
    """
    try:
        # Create a BlobClient from the URI
        blob_client = BlobClient.from_blob_url(blob_url=uri)

        # Download the blob's content and write it to a local file
        with open(download_file_path, "wb") as file:
            file.write(blob_client.download_blob().readall())
            print(f"Blob downloaded successfully to '{download_file_path}'")
            return 1
    except ResourceNotFoundError:
        print(f"Blob not found at the provided URI.")
        return 0
    except Exception as e:
        print(f"Error downloading blob: {e}")
        return 0

def upload_file_to_container(file_path,main_name):
    """
    Uploads a file to the Azure Blob Storage container.
    :param file_path: Path to the file to upload.
    """
    # Ensure the container exists
    try:
        if not container_client.exists():
            container_client.create_container()

        # Blob name should be the file name
        blob_name = f"{main_name}/{os.path.basename(file_path)}"
        # Upload file to Blob Storage
        with open(file_path, "rb") as data:
            print(f"Uploading {file_path} as {blob_name}")
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)

        # return the link to the file
        file_addr = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{main_name}/{os.path.basename(file_path)}"
        print(f"File uploaded to '{file_addr}'")
        return file_addr
        
    except:
        print(f"Error uploading file")
        return 0

def list_all_files_in_container():
    """
    Lists all blobs in the Azure Blob Storage container.
    """
    try:
        print(f"Files in container '{CONTAINER_NAME}':")
        for blob in container_client.list_blobs():
            print(f" - {blob.name}")
    except Exception as e:
        print(f"Error listing blobs: {e}")


def upload_folder_to_container(folder_path,main_name):
    """
    Uploads all files in a folder to the Azure Blob Storage container.
    :param folder_path: Path to the folder containing files to upload.
    """
    # Ensure the container exists
    if not container_client.exists():
        container_client.create_container()

    # Walk through the directory
    # main_name = "ChromaVectorStore"
    print(f"Uploading files to blob storage")
    folder_name = os.path.basename(folder_path)
    for root, dirs, files in os.walk(folder_path):
    
        for file in files:
            file_path = os.path.join(root, file)
            # Blob name should be relative path to the file
            blob_name = os.path.relpath(file_path, folder_path)
            blob_name = f"{main_name}/{folder_name}/{blob_name}"
            # Upload file to Blob Storage
            with open(file_path, "rb") as data:
                print(f"Uploading {file_path} as {blob_name}")
                container_client.upload_blob(name=blob_name, data=data, overwrite=True)

    # return the link to the folder
    folder_addr = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{main_name}/{folder_name}"
    print(f"Files uploaded to '{folder_addr}'")

    return folder_addr

# if __name__ == "__main__":
    # Example Usage

    # Upload a file
    # uri = "https://docparserblob.blob.core.windows.net/docparsercontainer/user_2rJIC7WzAGwwJE5dQ2qPwxvpT4G/pdf/HCLTECH__1736334719874_fbcb1d00-5668-4586-ae04-311e8cf4ea3c.pdf?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-11-16T22:57:46Z&st=2024-11-17T14:57:46Z&spr=https&sig=MDyePBPP%2BmWIPfVIAz65f1FQ9ycsoAZ9S%2FU71SBF88s%3D"

    # download_blob_from_uri(uri, "../rag/data/test.pdf")

    # List all files in the container
    # list_all_files_in_container()
    # upload_folder_to_container("../rag/data/test1_chromavectorstore")

    # list_all_files_in_container()
