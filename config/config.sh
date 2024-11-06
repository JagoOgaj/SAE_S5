#!/bin/bash

#####################
#                   #
#       Config      #
#                   #
#####################

apt-get install git

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <TOKEN> <GITHUB_USER> <GITHUB_EMAIL>"
    exit 1
fi

# Récupérer les arguments passés au script
TOKEN=$1
GITHUB_USER=$2
GITHUB_EMAIL=$3

#rm -rf /content/drive/MyDrive/SAE_S5

mkdir /content/drive/MyDrive/SAE_S5

git clone https://$TOKEN@github.com/JagoOgaj/SAE_S5.git /content/drive/MyDrive/SAE_S5

git config --global user.name "$GITHUB_USER"
git config --global user.email "$GITHUB_EMAIL"

git remote set-url main https://$TOKEN@github.com/JagoOgaj/SAE_S5.git

pip install -r /content/drive/MyDrive/SAE_S5/requirements.txt
