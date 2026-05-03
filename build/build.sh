#!/bin/bash
#  This build script is used to build the UnCover python modules as an executable
#  one Widnows.
#
# This is done to help find the wheel file for the current OS
# Currently only macos and linux are supported for the bash script
# windows is handled by the batch script
#
OS=$(uname -s)
ARCH=$(uname -m)
if [ "$OS" == "Darwin" ]
then
   OS=macosx
else
   OS=linux
fi


unzip() # parameter is name of file to unzip
{
echo "**** Unzipping $1 with Python***"   

python -c "import zipfile

# Open the ZIP file for reading
with zipfile.ZipFile('"$1"', 'r') as zipf:
    # Extract all files to a directory
    zipf.extractall('.')
"
}

echo -e "\nStarting build\n"

BASENAME=$(basename "${PWD}"  | tr '[:upper:]' '[:lower:]')
BASEDIR=${PWD}
if [ "$BASENAME" == "build" ]; then
   BASEDIR=$(dirname "${PWD}")
elif [ "$BASENAME" != "weathertrak" ]; then
   echo must be in unarchive base directory or build directory
   exit
fi

PYTHON=python3.13
PROJECT=WeatherTrak
PYINSTALLER=pyinstaller
DIST=${BASEDIR}/dist
WORK=${BASEDIR}/work
SRC=${BASEDIR}/$PROJECT
VERSION=1.0   

echo -e "\nRebuilding the virtual environment.\n"

#if [ -n "${VIRTUAL_ENV}" ]; then
#   VE=${VIRTUAL_ENV}
#   deactivate
#fi
rm -rf "${BASEDIR}/.venv"
"${PYTHON}" -m venv "${BASEDIR}/.venv"
source "${BASEDIR}/.venv/bin/activate"
"${PYTHON}" -m pip install --upgrade pip
"${PYTHON}" -m pip install -r "${BASEDIR}/requirements.txt"

echo -e "\nCleaning up the dist folder\n"

#
#  Clean up the distribution directories
#
rm -rf "$DIST"
rm -f "$DIST"

echo -e "\nRebuilding dist folder up the dist folder\n"

#
#  Make distribution directory structure and copy relevant sample files
#
mkdir "$DIST"
#cp -rp "${BASEDIR}/LICENSE" "$DIST/LICENSE"
#cp -rp "${BASEDIR}/README.md" "$DIST/README.md"
#cp -rp "${BASEDIR}/CreateCustomExports.md" "$DIST/CreateCustomExports.md"
#cp -rp "${BASEDIR}/unarchive.ini.sample" "$DIST/unarchive.ini.sample"
#cp -rp "${BASEDIR}/plugins" "$DIST/plugins"
#cp -rp "${BASEDIR}/tests/arch_test.AF" "$DIST/arch_test.AF"
#cp -rp "${BASEDIR}/samples" "$DIST/samples"
cp -rp "${SRC}/weather.sh" "$DIST/weather.sh"
cp -rp "${SRC}/getweather.py" "$DIST/getweather.py"

cd "$SRC" || exit

#VERSION=$(python base/UAVersion.py)

#echo -e "\nBuild command line executable\n"

#$PYINSTALLER --onefile --name WeatherApp ${SRC} weathertrak

pip list

deactivate

#if [ -n "${VE}" ]; then
#   source "${VE}/"bin/activate"
#fi