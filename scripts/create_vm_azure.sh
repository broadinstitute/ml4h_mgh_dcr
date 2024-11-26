#!/bin/bash
set -e

trap 'echo -e "\033[0;31m \nAn error occurred. Please clean up any Azure resources that might have been created up to the point of failure before rerunning the script. \033[0m"; exit 1' ERR

##### VM settings ##########
LOCATION="eastus2"
ADMIN_USERNAME="azureuser"
VM_SIZE="Standard_D4S_V3"
OS_DISK_GB="50"
# Image details
IMAGE_PUBLISHER="canonical" 
IMAGE_OFFER="ubuntu-24_04-lts"
IMAGE_SKU="server"
IMAGE_VERSION="latest"
############################

# Construct the image
IMAGE="$IMAGE_PUBLISHER:$IMAGE_OFFER:$IMAGE_SKU:$IMAGE_VERSION"

# Check if RESOURCE_GROUP and VM_NAME are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 RESOURCE_GROUP VM_NAME"
    exit 1
fi

# Check that VM_NAME is less than 20 characters. We impose that for readability reasons, as well as because the keyvault name is derived from VM name and must be less than 24 characters.
if [ ${#VM_NAME} -ge 21 ]; then
    echo "Error: VM_NAME length must be less or equal than 20 characters."
    exit 1
fi

RESOURCE_GROUP=$1
VM_NAME=$2

read -sp "Enter VM admin password: " ADMIN_PASSWORD
echo

read -sp "Repeat password: " ADMIN_PASSWORD_CONFIRM
echo

# Check if passwords match
if [ "$ADMIN_PASSWORD" != "$ADMIN_PASSWORD_CONFIRM" ]; then
    echo "Error: Passwords do not match."
    exit 1
fi

# Construct the key vault name - note that key vault name must be globally unique, between 3-24 alphanumeric characters, and begin with a letter, end with a letter or digit, and not contain consecutive hyphens
KEY_VAULT_NAME=$(echo $VM_NAME | tr -cd '[:alnum:]')"-kv"

echo "Getting subnet ID..."
SUBNET_ID=$(az network vnet subnet show \
  --resource-group mgh-echocardiography-research-ai-e2-rg \
  --vnet-name mgh-echocardiography-research-ai-e2-vnet \
  --name default \
  --query id --output tsv)

# Create the VM
echo "Creating VM..."
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --image $IMAGE \
  --size $VM_SIZE \
  --os-disk-size-gb $OS_DISK_GB \
  --admin-username $ADMIN_USERNAME \
  --admin-password $ADMIN_PASSWORD \
  --subnet $SUBNET_ID \
  --location $LOCATION \
  --public-ip-address ""

echo "Creating keyvault..."
az keyvault create --name $KEY_VAULT_NAME --resource-group $RESOURCE_GROUP --location $LOCATION --enabled-for-disk-encryption

echo "Encrypting VM..."
az vm encryption enable -g $RESOURCE_GROUP --name ${VM_NAME} --disk-encryption-keyvault $KEY_VAULT_NAME

# Output the VM details
echo "VM '$VM_NAME' created in resource group '$RESOURCE_GROUP' with admin username '$ADMIN_USERNAME'."
