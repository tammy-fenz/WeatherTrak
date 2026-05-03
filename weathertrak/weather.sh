echo "=============== $(hostname) starting at $(date)"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
rm -rf "${DIR}/.venv"
python -m venv "${DIR}/.venv"
source "${DIR}/.venv/bin/activate"
python -m pip install --upgrade pip
pip install requests
python "$DIR"/getweather.py
echo "=============== finished at $(date)"