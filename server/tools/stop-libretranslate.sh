initialDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
dockerPath=$( cd -- "${initialDir}/../containers" &> /dev/null && pwd )

# Closing Docker services by name
echo "Stopping LibreTranslate container..."
sudo docker compose -f "$dockerPath/libretranslate-compose.yaml" down
if [ $? -eq 0 ]; then
    echo "LibreTranslate stopped successfully."
else
    echo "Failed to stop LibreTranslate docker container. Check logs for details."
fi