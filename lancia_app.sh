#!/usr/bin/env bash

# Script di lancio per l'app Gestione Pagamenti in locale

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Cartella di lavoro: $SCRIPT_DIR"
echo "Avvio Streamlit con python3..."

python3 -m streamlit run pagamenti.py