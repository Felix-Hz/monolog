#!/bin/bash
 
# Utils
function divider() { printf '_%.0s' {1..16};  printf '\n\n'; }
function install_uv(){
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

# Execution
echo "⚙️ Installing uv..."
install_uv
divider

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate
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

