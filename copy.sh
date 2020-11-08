# run: . copy.sh
# if permission denied, run chmod +x copy.sh

# validate input
extension=${1:($(echo -n ${1} | wc -m) - 4):$(echo -n ${1} | wc -m)}
# https://stackoverflow.com/questions/22179405/bash-script-error-unary-operator-expected
if [ "${1}" == "" ] || [ "${2}" == "" ]; then
  echo Usage: ". copy.sh <name-of-zip> <destination-dir-name>"
  kill -INT $$
elif [ "${extension}" != ".zip" ]; then
  echo Error: must input .zip file
  kill -INT $$
elif [ "${2}" != "fa20" ] && [ "${2}" != "fa20-csm" ]; then
  echo Error: destination directory must be "fa20" or "fa20-csm"
  kill -INT $$
fi

OK_DIR=`pwd`

src="${OK_DIR}/zips/${1}"

REPO_DIR=${WEBSITE_DIR}

dest="${REPO_DIR}assets/${2}"

cp -a ${src} ${dest}

echo Copied!