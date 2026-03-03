"""
Software Gestione Pagamenti - App Streamlit
Avvia con: streamlit run pagamenti.py
"""
from pathlib import Path
import hashlib
import json

import streamlit as st

st.set_page_config(page_title="Gestione Pagamenti", layout="wide")

BASE_DIR = Path(__file__).parent
USERS_FILE = BASE_DIR / "utenti.json"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users():
    if not USERS_FILE.exists():
        return []
    try:
        with USERS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def ensure_admin_user():
    """Crea un utente admin di default se il file è vuoto o mancante."""
    users = load_users()
    if not any(u.get("role") == "admin" for u in users):
        users.append(
            {
                "username": "admin",
                "password_hash": hash_password("admin123"),
                "role": "admin",
            }
        )
        save_users(users)


def authenticate(username: str, password: str):
    users = load_users()
    pwd_hash = hash_password(password)
    for user in users:
        if user["username"] == username and user["password_hash"] == pwd_hash:
            return user
    return None


def show_login():
    st.title("Accesso Gestione Pagamenti")
    st.write("Inserisci le tue credenziali.")

    username = st.text_input("Utente")
    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
        user = authenticate(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["role"] = user["role"]
            st.success(f"Accesso effettuato come {user['username']} ({user['role']}).")
            st.rerun()
        else:
            st.error("Utente o password non corretti.")


def show_admin_area():
    st.subheader("Area amministratore - Gestione utenti")

    users = load_users()
    if users:
        st.write("Utenti esistenti:")
        st.table(
            [
                {
                    "username": u["username"],
                    "ruolo": u["role"],
                }
                for u in users
            ]
        )
    else:
        st.info("Nessun utente presente.")

    st.markdown("---")
    st.write("Crea un nuovo utente:")

    new_username = st.text_input("Nuovo utente", key="new_username")
    new_password = st.text_input("Password nuovo utente", type="password", key="new_password")
    new_role = st.selectbox("Ruolo", ["utente", "admin"])

    if st.button("Crea utente"):
        if not new_username or not new_password:
            st.error("Compila sia utente che password.")
        else:
            if any(u["username"] == new_username for u in users):
                st.error("Nome utente già esistente.")
            else:
                users.append(
                    {
                        "username": new_username,
                        "password_hash": hash_password(new_password),
                        "role": new_role,
                    }
                )
                save_users(users)
                st.success(f"Utente '{new_username}' creato con ruolo '{new_role}'.")
                st.rerun()


def show_main_app():
    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "utente")

    st.title("Gestione Pagamenti")
    st.write(f"Benvenuto, **{username}**. Ruolo: **{role}**.")

    if role == "admin":
        area = st.sidebar.radio("Area", ["Pagamenti", "Amministrazione utenti"])
    else:
        area = "Pagamenti"

    if area == "Amministrazione utenti" and role == "admin":
        show_admin_area()
    else:
        st.subheader("Area pagamenti")
        st.write("Qui in futuro aggiungeremo tutte le funzioni di gestione pagamenti.")
        if st.button("Esempio: mostra messaggio"):
            st.success("Funziona! (area protetta dopo login)")

    st.markdown("---")
    if st.button("Esci"):
        st.session_state.clear()
        st.rerun()


def main():
    ensure_admin_user()

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        show_login()
    else:
        show_main_app()


if __name__ == "__main__":
    main()
