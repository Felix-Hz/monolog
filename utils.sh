#!/bin/bash

function divider  { printf '_%.0s' {1..16};  printf '\n\n'; }

function install_uv {
    if ! which uv > /dev/null; then
        if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
            echo "✅ uv is now installed"
        elif [ "$(uname)" == "Windows" ]; then
            powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
            echo "✅ uv is now installed"
        else
            echo "⚠️ Unsupported operating system"
            exit 1
        fi
    else
        echo "✅ uv is already installed"
    fi
}

function activate_or_create_venv {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        uv venv .venv
        source .venv/bin/activate
        echo "✅ Virtual environment created and activated"
    fi
}

function validate_py_version {
    local VERSION="$(python --version | awk '{print $2}' | cut -d'.' -f1-2)"
    if (( $(echo "$VERSION >= 3.12" | bc -l) )); then
        echo "✅ Supported"
    else
        echo "⚠️ Unsupported"
        exit 1
    fi
}

function install_dependencies {
    uv sync
    echo "✅ Environment up to date"
}

function make_and_migrate {
    python manage.py makemigrations
    python manage.py migrate
    echo "✅ Database up to date"
}

function spin_server_up {
    python manage.py runserver
    echo "✅ Server started"
}

function monofetch {
    echo " _ __  ___   ___  _ __   ___ | | ___   __ _"
    echo "| '_ \` _ \ / _ \| '_ \ / _ \| |/ _ \ / _\` |"
    echo "| | | | | | (_) | | | | (_) | | (_) | (_| |"
    echo "|_| |_| |_|\___/|_| |_|\___/|_|\___/ \__, |"
    echo "                                      |___/"
}
