#!/bin/bash

if [[ $# != 1 ]] 
then
    echo "Usage: sign <clientname>"
    exit 1
fi

echo "Generating Public Private key pair for Tenant"
# read -p $'Enter the tenant name\n' name
# To generate a public/private key:
name=$1
openssl genrsa -out private_$name.pem 4096
openssl rsa -in private_$name.pem -pubout -out public_$name.pem

# privatekey=$2
# echo "Signing the public key of the tenant"
# sleep 1
# openssl dgst -sha256 -sign /home/ubuntu/encryption-project/CA_Private.pem -out sign_bin public_$name.pem # Binary signed file
# openssl base64 -in sign_bin -out sign_base64 # base 64 encoded signed file
