# run: . deploy.sh
# if permission denied, run chmod +x deploy.sh

# validate input

extension=${1:($(echo -n ${1} | wc -m) - 4):$(echo -n ${1} | wc -m)}
# https://stackoverflow.com/questions/22179405/bash-script-error-unary-operator-expected
if [ "${1}" == "" ] || [ "${2}" == "" ]; then
  echo Usage: ". deploy.sh <name-of-zip> <destination-dir-name>"
  kill -INT $$
elif [ "${extension}" != ".zip" ]; then
  echo Error: must input .zip file
  kill -INT $$
elif [ "${2}" != "fa20" ] && [ "${2}" != "fa20-csm" ]; then
  echo Error: destination directory must be "fa20" or "fa20-csm"
  kill -INT $$
fi

PROMPT="Do you really want to copy and push ${1}? (y/n): "
echo "${PROMPT}"
read RESPONSE
RESPONSE=$(echo "${RESPONSE}" | tr '[:upper:]' '[:lower:]')
while [ "${RESPONSE}" != "y" ] && [ "${RESPONSE}" != "n" ]
do
  echo "${PROMPT}"
  read RESPONSE
  RESPONSE=$(echo "${RESPONSE}" | tr '[:upper:]' '[:lower:]')
done

if [ "${RESPONSE}" == "n" ]; then
  echo Exiting
  kill -INT $$
fi

OK_DIR=`pwd`

src="${OK_DIR}/zips/${1}"

REPO_DIR=${WEBSITE_DIR}

dest="${REPO_DIR}assets/${2}"

cp -a ${src} ${dest}

GIT=`which git`
cd ${REPO_DIR}

${GIT} add assets/${2}/${1}
${GIT} commit -m "release ${1}"
${GIT} push ${WEBSITE_PUSH}

cd ${OK_DIR}