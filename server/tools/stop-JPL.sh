currentDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
${currentDir}/stop-python-server.sh && ${currentDir}/stop-libretranslate.sh