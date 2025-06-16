currentDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
${currentDir}/start-python-server.sh && ${currentDir}/start-libretranslate.sh