#!/usr/bin/env bash

# Avvia l'app Gestione Pagamenti con Streamlit

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Avvio Gestione Pagamenti..."
./lancia_app.sh

