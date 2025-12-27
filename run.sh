#!/bin/bash

source utils.sh

monofetch

echo "⚙️ Installing uv..."
install_uv
divider

echo "⚙️ Activating virtual environment..."
activate_or_create_venv
divider

echo "⚙️ Validating Python version..."
validate_py_version
divider

echo "⚙️ Installing dependencies..."
install_dependencies
divider

echo "⚙️ Checking for outstanding migrations..."
make_and_migrate
divider

echo "⚙️ Running services..."
spin_services_up "$1"
divider
