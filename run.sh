#!/bin/bash

# Utils
function divider  { printf '_%.0s' {1..16};  printf '\n\n'; }
function install_uv {
    if ! which uv > /dev/null; then
        if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
        elif [ "$(uname)" == "Windows" ]; then
            powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        else
            echo "⚠️ Unsupported operating system"
            exit 1
        fi
    else
        echo "✅ uv is already installed"
    fi
}
function validate_py_version {
    local VERSION="$(python --version | awk '{print $2}' | cut -d'.' -f1-2)"
    if (( $(echo "$VERSION >= 3.12" | bc -l) )); then
        echo "✅ Supported"
    else
        echo "⚠️ Unsupported"
    fi
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Execution
echo "⚙️ Installing uv..."
install_uv
divider

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate
divider

echo "⚙️ Validating Python version..."
validate_py_version
divider

echo "⚙️ Installing dependencies..."
uv sync
divider

echo "⚙️ Checking for outstanding migrations..."
python manage.py makemigrations
python manage.py migrate
divider

echo "⚙️ Running server..."
python manage.py runserver
divider

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
