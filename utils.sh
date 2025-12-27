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

  function spin_services_up {
      echo "🚀 Starting Redis..."
      docker start redis 2>/dev/null || docker run -d -p 6379:6379 --name redis redis

      echo "🚀 Starting Celery worker..."
      celery -A project worker --loglevel=info &
      CELERY_PID=$!

      echo "🚀 Starting Django server..."
      python manage.py runserver &
      DJANGO_PID=$!

      # Trap to kill background processes on exit
      trap "kill $CELERY_PID $DJANGO_PID 2>/dev/null; docker stop redis" EXIT

      echo "✅ All services started"
      echo "   Django server: http://127.0.0.1:8000"
      echo "   Celery worker is running in background"
      echo "   Redis server is running in background"
      echo "   Press Ctrl+C to stop all services"

      # Wait for processes
      wait
  }

function monofetch {
    echo " _ __  ___   ___  _ __   ___ | | ___   __ _"
    echo "| '_ \` _ \ / _ \| '_ \ / _ \| |/ _ \ / _\` |"
    echo "| | | | | | (_) | | | | (_) | | (_) | (_| |"
    echo "|_| |_| |_|\___/|_| |_|\___/|_|\___/ \__, |"
    echo "                                      |___/"
}
