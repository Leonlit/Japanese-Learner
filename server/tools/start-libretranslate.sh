initialDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
dockerPath=$( cd -- "${initialDir}/../containers" &> /dev/null && pwd )

# Navigate to the LibreTranslate Docker Compose directory and start services in detached mode
echo "Starting LibreTranslate in detached mode..."
sudo docker compose -f "$dockerPath/libretranslate-compose.yaml" up -d
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose."
    exit 1
fi

# Wait for connection
echo "Waiting for LibreTranslate to be ready..."
while [ "$(curl -s -o /dev/null -w '%{http_code}' -X OPTIONS http://localhost:5050/translate)" != "200" ]; do
    echo "LibreTranslate is not ready yet. Retrying in 60 seconds..."
    sleep 60
done
echo "LibreTranslate is up!"
