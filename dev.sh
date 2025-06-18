# UV version to install
UV_VERSION="0.6.9"

# exit previous venv if any
if command -v deactivate &> /dev/null; then
  echo "exit current virtual env"
  deactivate
fi

# install uv
#
if ! command -v uv &> /dev/null
then
   curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh
fi

echo "installing dependencies..."
uv sync



# enter virtualenv
source $(pwd)/.venv/bin/activate

# install pre-commit
pre-commit install
