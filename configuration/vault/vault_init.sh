#!/bin/bash

VAULT_ADDR="http://0.0.0.0:8200"

echo "Initialisation de Vault..."
init_output=$(docker exec transcendence-vault-1 vault operator init)
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'initialisation de Vault"
    exit 1
fi

# If vault is already initialized init_output will get the actual status
echo "Extraction des clés de déverrouillage et du jeton d'accès root..."
unseal_key_1=$(echo "$init_output" | awk '/Unseal Key 1/ {print $4}')
unseal_key_2=$(echo "$init_output" | awk '/Unseal Key 2/ {print $4}')
unseal_key_3=$(echo "$init_output" | awk '/Unseal Key 3/ {print $4}')

echo "Déverrouillage de Vault avec la clé $unseal_key_1..."
docker exec transcendence-vault-1 vault operator unseal $unseal_key_1
if [ $? -ne 0 ]; then
    echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_1"
    exit 1
fi

echo "Déverrouillage de Vault avec la clé $unseal_key_2..."
docker exec transcendence-vault-1 vault operator unseal $unseal_key_2
if [ $? -ne 0 ]; then
    echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_2"
    exit 1
fi

echo "Déverrouillage de Vault avec la clé $unseal_key_3..."
docker exec transcendence-vault-1 vault operator unseal $unseal_key_3
if [ $? -ne 0 ]; then
    echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_3"
    exit 1
fi

root_token=$(echo "$init_output" | awk '/Initial Root Token/ {print $4}')
echo "Connexion à Vault avec le jeton d'accès root..."
docker exec transcendence-vault-1 vault login $root_token
if [ $? -ne 0 ]; then
    echo "Erreur lors de la connexion à Vault"
    exit 1
fi

export VAULT_TOKEN=$root_token
echo "Root Token: $root_token"

# Activation du Secret Engine KV si nécessaire
echo "Vérification du Secret Engine KV..."
kv_enabled=$(docker exec transcendence-vault-1 vault secrets list | grep -E "^kv/")
if [ -z "$kv_enabled" ]; then
    echo "Activation du Secret Engine KV version 2..."
    docker exec transcendence-vault-1 vault secrets enable -version=2 kv
    if [ $? -ne 0 ]; then
        echo "Erreur lors de l'activation du Secret Engine KV"
        exit 1
    fi
else
    echo "Le Secret Engine KV est déjà activé."
fi

RELATIVE_PATH="../../.env.dev"

ENV_FILE=$(realpath "$(dirname "$0")/$RELATIVE_PATH")

echo "Vérification de l'existence du fichier .env..."
if [ ! -f "$ENV_FILE" ]; then
    echo "Le fichier .env n'existe pas à l'emplacement spécifié."
    exit 1
fi

echo "Lecture et enregistrement des secrets du fichier .env dans Vault..."
while IFS='=' read -r key value; do
    if [[ "$key" == \#* || "$key" == "" ]]; then
        continue
    fi

    key=$(echo $key | xargs)
    value=$(echo $value | xargs)

    echo "Enregistrement du secret pour la clé $key..."
    response=$(curl --silent --header "X-Vault-Token: $VAULT_TOKEN" \
                    --request POST \
                    --data "{\"data\": {\"$key\": \"$value\"}}" \
                    $VAULT_ADDR/v1/kv/data/myapp/$key)

    echo "Réponse de Vault pour la clé $key: $response"

    echo $response | grep "errors" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Erreur lors de l'enregistrement du secret pour la clé $key"
    fi
done < "$ENV_FILE"

echo "Tous les secrets ont été enregistrés avec succès."