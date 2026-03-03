"""
Software Gestione Pagamenti - App Streamlit
Avvia con: streamlit run pagamenti.py
"""
from pathlib import Path
import hashlib
import json
from datetime import date, datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestione Pagamenti", layout="wide")

# Stile globale: colori tenui e pulsantini più carini
st.markdown("""
<style>
    /* Metriche in card con colori pastello */
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f7fa 100%);
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 4px solid #5b9bd5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    /* Pulsanti più morbidi */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        border: 1px solid #c5d9e8;
        background: linear-gradient(180deg, #f8fcff 0%, #e8f2f8 100%);
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #e8f2f8 0%, #d0e4f2 100%);
        border-color: #5b9bd5;
        box-shadow: 0 2px 6px rgba(91,155,213,0.2);
    }
    /* Box report totale */
    .report-totale-box {
        background: linear-gradient(145deg, #f5f9fc 0%, #eef5fa 100%);
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #d4e5f0;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .report-totale-title {
        color: #2c5f7a;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    /* Tabella con righe alternate tenui */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    /* Sidebar più pulita */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fbfd 0%, #f0f5f9 100%);
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent
USERS_FILE = BASE_DIR / "utenti.json"
PAYMENTS_FILE = BASE_DIR / "pagamenti_dati.json"


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


def load_payments():
    if not PAYMENTS_FILE.exists():
        return {"medici": {}, "email_medici": {}, "telefono_medici": {}}
    try:
        with PAYMENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"medici": {}, "email_medici": {}, "telefono_medici": {}}
    if "medici" not in data or not isinstance(data["medici"], dict):
        data["medici"] = {}
    if "email_medici" not in data or not isinstance(data["email_medici"], dict):
        data["email_medici"] = {}
    if "telefono_medici" not in data or not isinstance(
        data["telefono_medici"], dict
    ):
        data["telefono_medici"] = {}
    return data


def save_payments(data):
    with PAYMENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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


def show_payments_area():
    st.subheader("Gestione provvigioni medici")

    data = load_payments()
    medici = data.get("medici", {})
    email_medici = data.get("email_medici", {})
    telefono_medici = data.get("telefono_medici", {})
    nomi_medici = sorted(medici.keys())

    st.markdown("#### Seleziona o crea medico")
    col1, col2 = st.columns([2, 1])

    with col1:
        medico_selezionato = st.selectbox(
            "Medico esistente",
            options=["- Seleziona medico -"] + nomi_medici
            if nomi_medici
            else ["- Nessun medico presente -"],
            index=0,
            key="medico_selezionato",
        )
        if medico_selezionato.startswith("-"):
            medico_corrente = None
        else:
            medico_corrente = medico_selezionato

    with col2:
        nuovo_medico = st.text_input("Nuovo medico", key="nuovo_medico")
        nuova_email = st.text_input("Email medico", key="nuova_email")
        nuovo_cell = st.text_input("Cellulare medico", key="nuovo_cell")
        if st.button("Aggiungi medico"):
            if not nuovo_medico:
                st.warning("Inserisci il nome del nuovo medico.")
            elif nuovo_medico in medici:
                st.warning("Questo medico esiste già.")
            else:
                medici[nuovo_medico] = []
                data["medici"] = medici
                if nuova_email:
                    email_medici[nuovo_medico] = nuova_email.strip()
                    data["email_medici"] = email_medici
                if nuovo_cell:
                    telefono_medici[nuovo_medico] = nuovo_cell.strip()
                    data["telefono_medici"] = telefono_medici
                save_payments(data)
                st.success(f"Medico '{nuovo_medico}' aggiunto.")
                st.rerun()

    if not medico_corrente:
        st.info("Seleziona un medico esistente o creane uno nuovo per iniziare.")
        return

    # Gestione email del medico selezionato
    st.markdown("---")
    st.markdown("#### Dati medico")
    email_corrente = email_medici.get(medico_corrente, "")
    cell_corrente = telefono_medici.get(medico_corrente, "")
    col_mail1, col_mail2, col_mail3 = st.columns([3, 3, 1])
    with col_mail1:
        nuova_email_medico = st.text_input(
            f"Email di {medico_corrente}",
            value=email_corrente,
            key="email_medico_corrente",
        )
    with col_mail2:
        nuovo_cell_medico = st.text_input(
            f"Cellulare di {medico_corrente}",
            value=cell_corrente,
            key="cell_medico_corrente",
        )
    with col_mail3:
        if st.button("Salva contatti", key="salva_contatti_medico"):
            email_medici[medico_corrente] = nuova_email_medico.strip()
            telefono_medici[medico_corrente] = nuovo_cell_medico.strip()
            data["email_medici"] = email_medici
            data["telefono_medici"] = telefono_medici
            save_payments(data)
            st.success("Contatti del medico aggiornati.")

    st.markdown("---")
    st.markdown("#### Aggiungi vendita (stile tabella Excel)")

    mese_corrente = date.today().strftime("%Y-%m")

    vendita_in_modifica = st.session_state.get("edit_values")

    # Valori di default per il form (nuova vendita o modifica)
    if vendita_in_modifica:
        try:
            data_default = datetime.strptime(
                vendita_in_modifica.get("data", date.today().strftime("%d/%m/%y")),
                "%d/%m/%y",
            ).date()
        except Exception:
            data_default = date.today()
        mese_default = vendita_in_modifica.get("mese", mese_corrente)
        cliente_default = vendita_in_modifica.get("cliente") or vendita_in_modifica.get(
            "paziente", ""
        )
        valore_default = float(vendita_in_modifica.get("valore", 0.0))
        perc_default = float(vendita_in_modifica.get("percentuale", 25.0))
        testo_bottone = "Salva modifica"
    else:
        data_default = date.today()
        mese_default = mese_corrente
        cliente_default = ""
        valore_default = 0.0
        perc_default = 25.0
        testo_bottone = "Aggiungi riga in tabella"

    with st.form(key="form_vendita", clear_on_submit=True):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            data_vendita = st.date_input("Data", value=data_default)
        with col_d2:
            mese_riferimento = st.text_input(
                "Mese di riferimento (YYYY-MM)", value=mese_default
            )

        cliente = st.text_input("Cliente (nome e cognome)", value=cliente_default)
        valore = st.number_input(
            "Prezzo di vendita (€)",
            min_value=0.0,
            step=10.0,
            format="%.2f",
            value=valore_default,
        )
        percentuale = st.number_input(
            "Percentuale provvigione (%)",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            value=perc_default,
        )

        conferma = st.form_submit_button(testo_bottone)

        if conferma:
            if not cliente:
                st.warning("Inserisci il nome del cliente.")
            elif not mese_riferimento:
                st.warning("Inserisci il mese di riferimento.")
            else:
                commissione = valore * percentuale / 100.0
                vendite_medico = medici.get(medico_corrente, [])
                vendite_medico.append(
                    {
                        "data": data_vendita.strftime("%d/%m/%y"),
                        "cliente": cliente,
                        "paziente": cliente,
                        "valore": float(valore),
                        "percentuale": float(percentuale),
                        "commissione": float(commissione),
                        "mese": mese_riferimento,
                        "pagato": False,
                        "archiviato": False,
                    }
                )
                medici[medico_corrente] = vendite_medico
                data["medici"] = medici
                save_payments(data)
                st.session_state["edit_values"] = None
                if vendita_in_modifica:
                    st.success("Modifica salvata correttamente.")
                else:
                    st.success("Riga aggiunta correttamente alla tabella.")
                st.rerun()

    st.markdown("---")
    st.markdown("#### Report per medico e mese")

    vendite_medico = medici.get(medico_corrente, [])
    if not vendite_medico:
        st.info("Non ci sono vendite registrate per questo medico.")
        return

    mesi_disponibili = sorted({v["mese"] for v in vendite_medico})
    mese_default = date.today().strftime("%Y-%m")
    if mese_default in mesi_disponibili:
        idx_default = mesi_disponibili.index(mese_default)
    else:
        idx_default = len(mesi_disponibili) - 1

    mese_selezionato = st.selectbox(
        "Mese di riferimento",
        options=mesi_disponibili,
        index=idx_default,
        key="mese_report",
    )

    vendite_mese_attive = [
        v
        for v in vendite_medico
        if v.get("mese") == mese_selezionato and not v.get("archiviato", False)
    ]

    if not vendite_mese_attive:
        st.info("Nessuna vendita attiva per il mese selezionato (forse è già archiviato).")
    else:
        # Calcolo righe e totali per logica e per export CSV
        righe = []
        for v in vendite_mese_attive:
            righe.append(
                {
                    "data": v.get("data", ""),
                    "cliente": v.get("cliente") or v.get("paziente", ""),
                    "referente": medico_corrente,
                    "prezzo di vendita (€)": v.get("valore", 0.0),
                    "% provvigione": v.get("percentuale", 0.0),
                    "provvigione (€)": v.get("commissione", 0.0),
                }
            )

        df = pd.DataFrame(righe)
        totale_valore = df["prezzo di vendita (€)"].sum()
        totale_commissioni = df["provvigione (€)"].sum()

        riga_totale = {
            "data": "",
            "cliente": "TOTALE",
            "referente": "",
            "prezzo di vendita (€)": totale_valore,
            "% provvigione": "",
            "provvigione (€)": totale_commissioni,
        }
        df_con_totale = pd.concat([df, pd.DataFrame([riga_totale])], ignore_index=True)

        # Tabella stile Excel con pulsanti per riga (righe alternate colorate)
        st.markdown("##### Vendite del mese")
        header_cols = st.columns([1.5, 3, 2, 2, 2, 2, 2])
        intestazioni = [
            "Data",
            "Cliente",
            "Referente",
            "Prezzo vendita (€)",
            "% provvigione",
            "Provvigione (€)",
            "Azioni",
        ]
        for col, testo in zip(header_cols, intestazioni):
            col.markdown(f"**{testo}**")

        indici_righe = [
            i
            for i, v in enumerate(vendite_medico)
            if v.get("mese") == mese_selezionato and not v.get("archiviato", False)
        ]

        for riga_visibile, idx in enumerate(indici_righe):
            v = vendite_medico[idx]
            bg_color = "#ffffff" if riga_visibile % 2 == 0 else "#f5f7ff"

            def cell(texto: str):
                return f"<div style='background-color:{bg_color}; padding:4px 6px; border-radius:3px;'>{texto}</div>"

            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 3, 2, 2, 2, 2, 2])
            with c1:
                st.markdown(cell(v.get("data", "")), unsafe_allow_html=True)
            with c2:
                st.markdown(
                    cell(v.get("cliente") or v.get("paziente", "")),
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(cell(medico_corrente), unsafe_allow_html=True)
            with c4:
                st.markdown(
                    cell(f"{v.get('valore', 0.0):.2f} €"), unsafe_allow_html=True
                )
            with c5:
                st.markdown(
                    cell(f"{v.get('percentuale', 0.0):.0f} %"), unsafe_allow_html=True
                )
            with c6:
                st.markdown(
                    cell(f"{v.get('commissione', 0.0):.2f} €"),
                    unsafe_allow_html=True,
                )
            with c7:
                col_elim, col_mod = st.columns(2)
                with col_elim:
                    if st.button(
                        "🗑️ Elimina",
                        key=f"del_{medico_corrente}_{mese_selezionato}_{idx}",
                    ):
                        vendite_medico.pop(idx)
                        medici[medico_corrente] = vendite_medico
                        data["medici"] = medici
                        save_payments(data)
                        st.success("Vendita eliminata.")
                        st.rerun()
                with col_mod:
                    if st.button(
                        "✏️ Modifica",
                        key=f"edit_{medico_corrente}_{mese_selezionato}_{idx}",
                    ):
                        st.session_state["edit_values"] = v
                        # Rimuovo subito la vecchia riga; verrà reinserita aggiornata dal form
                        vendite_medico.pop(idx)
                        medici[medico_corrente] = vendite_medico
                        data["medici"] = medici
                        save_payments(data)
                        st.info("Ora modifica i valori nel form sopra e conferma.")
                        st.rerun()

        # Riga totale riassuntiva
        st.markdown("---")
        c_tot1, c_tot2, c_tot3 = st.columns([4, 2, 2])
        with c_tot1:
            st.markdown("**TOTALE**")
        with c_tot2:
            st.markdown(f"**Vendite: {totale_valore:,.2f} €**")
        with c_tot3:
            st.markdown(f"**Provvigioni: {totale_commissioni:,.2f} €**")

        # Dati di saldo per il mese
        st.markdown("##### Dati di pagamento del mese")
        col_mp1, col_mp2 = st.columns(2)
        with col_mp1:
            metodo_pagamento = st.selectbox(
                "Metodo di pagamento",
                options=[
                    "Bonifico bancario",
                    "Contanti",
                    "Assegno",
                    "Altro",
                ],
                key="metodo_pagamento",
            )
        with col_mp2:
            nota_pagamento = st.text_input(
                "Nota pagamento (es. numero CRO, banca, ecc.)",
                key="nota_pagamento",
            )

        csv = df_con_totale.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Scarica report CSV per il medico",
            data=csv,
            file_name=f"report_{medico_corrente}_{mese_selezionato}.csv",
            mime="text/csv",
        )

        if st.button(
            "Segna questo mese come pagato e archivia",
            key="archivia_mese",
            use_container_width=True,
        ):
            for v in vendite_medico:
                if v.get("mese") == mese_selezionato:
                    v["archiviato"] = True
                    v["pagato"] = True
                    v["data_pagamento"] = date.today().isoformat()
                    v["metodo_pagamento"] = metodo_pagamento
                    v["nota_pagamento"] = nota_pagamento
            medici[medico_corrente] = vendite_medico
            data["medici"] = medici
            save_payments(data)
            st.success(
                f"Mese {mese_selezionato} archiviato per {medico_corrente}. "
                "Per il mese successivo potrai inserire nuove vendite con il nuovo mese di riferimento."
            )
            st.rerun()


def show_storico_area():
    """Visualizza i mesi archiviati (pagati) per ogni medico."""
    st.subheader("Storico pagamenti archiviati")

    data = load_payments()
    medici = data.get("medici", {})
    email_medici = data.get("email_medici", {})
    telefono_medici = data.get("telefono_medici", {})
    nomi_medici = sorted(medici.keys())

    if not nomi_medici:
        st.info("Nessun medico presente. Aggiungi medici e archivia dei mesi dalla sezione Pagamenti.")
        return

    medico_selezionato = st.selectbox(
        "Seleziona il medico",
        options=nomi_medici,
        key="storico_medico",
    )
    vendite_medico = medici.get(medico_selezionato, [])
    email_medico = email_medici.get(medico_selezionato, "")
    cell_medico = telefono_medici.get(medico_selezionato, "")
    vendite_archiviate = [v for v in vendite_medico if v.get("archiviato")]

    if not vendite_archiviate:
        st.info(
            f"Nessun mese archiviato per **{medico_selezionato}**. "
            "I mesi compaiono qui dopo aver cliccato «Segna questo mese come pagato e archivia»."
        )
        return

    mesi_archiviati = sorted(
        {v["mese"] for v in vendite_archiviate},
        reverse=True,
    )
    mese_storico = st.selectbox(
        "Mese da visualizzare",
        options=mesi_archiviati,
        key="storico_mese",
    )

    righe_mese = [
        v
        for v in vendite_archiviate
        if v.get("mese") == mese_storico
    ]
    if not righe_mese:
        st.warning("Nessun dato per questo mese.")
        return

    # Data pagamento se presente
    data_pag = righe_mese[0].get("data_pagamento")
    metodo_pag = righe_mese[0].get("metodo_pagamento", "")
    nota_pag = righe_mese[0].get("nota_pagamento", "")

    info_line = []
    if data_pag:
        # Normalizza il formato data in GG/MM/AAAA
        try:
            dt_pag = datetime.fromisoformat(data_pag)
            data_pag_formattata = dt_pag.strftime("%d/%m/%Y")
        except Exception:
            # Se non è ISO, la mostriamo così com'è
            data_pag_formattata = data_pag
        info_line.append(f"pagato il **{data_pag_formattata}**")
    if metodo_pag:
        info_line.append(f"con **{metodo_pag}**")
    if nota_pag:
        info_line.append(f"(**{nota_pag}**)")

    if email_medico or cell_medico:
        contatti = []
        if email_medico:
            contatti.append(f"Email: `{email_medico}`")
        if cell_medico:
            contatti.append(f"Cellulare: `{cell_medico}`")
        st.markdown(" – ".join(contatti))

    if info_line:
        st.caption(" - ".join(info_line))

    # Tabella storico (stesso stile, solo lettura)
    st.markdown("##### Dettaglio vendite archiviate")
    header_cols = st.columns([1.5, 3, 2, 2, 2, 2])
    for col, testo in zip(
        header_cols,
        ["Data", "Cliente", "Referente", "Prezzo vendita (€)", "% provvigione", "Provvigione (€)"],
    ):
        col.markdown(f"**{testo}**")

    totale_valore = 0.0
    totale_commissioni = 0.0
    for riga_visibile, v in enumerate(righe_mese):
        bg_color = "#ffffff" if riga_visibile % 2 == 0 else "#f5f7ff"
        totale_valore += v.get("valore", 0.0)
        totale_commissioni += v.get("commissione", 0.0)

        def cell(texto: str):
            return f"<div style='background-color:{bg_color}; padding:4px 6px; border-radius:3px;'>{texto}</div>"

        c1, c2, c3, c4, c5, c6 = st.columns([1.5, 3, 2, 2, 2, 2])
        with c1:
            st.markdown(cell(v.get("data", "")), unsafe_allow_html=True)
        with c2:
            st.markdown(
                cell(v.get("cliente") or v.get("paziente", "")),
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(cell(medico_selezionato), unsafe_allow_html=True)
        with c4:
            st.markdown(
                cell(f"{v.get('valore', 0.0):.2f} €"), unsafe_allow_html=True
            )
        with c5:
            st.markdown(
                cell(f"{v.get('percentuale', 0.0):.0f} %"), unsafe_allow_html=True
            )
        with c6:
            st.markdown(
                cell(f"{v.get('commissione', 0.0):.2f} €"),
                unsafe_allow_html=True,
            )

    st.markdown("---")
    c_tot1, c_tot2, c_tot3 = st.columns([4, 2, 2])
    with c_tot1:
        st.markdown("**TOTALE**")
    with c_tot2:
        st.markdown(f"**Vendite: {totale_valore:,.2f} €**")
    with c_tot3:
        st.markdown(f"**Provvigioni: {totale_commissioni:,.2f} €**")

    # Export CSV dello storico
    df_storico = pd.DataFrame(
        [
            {
                "data": v.get("data", ""),
                "cliente": v.get("cliente") or v.get("paziente", ""),
                "referente": medico_selezionato,
                "prezzo (€)": v.get("valore", 0.0),
                "%": v.get("percentuale", 0.0),
                "provvigione (€)": v.get("commissione", 0.0),
            }
            for v in righe_mese
        ]
    )
    csv = df_storico.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Scarica report CSV (storico)",
        data=csv,
        file_name=f"storico_{medico_selezionato}_{mese_storico}.csv",
        mime="text/csv",
        key="download_storico",
    )


def show_statistiche_area():
    """Statistiche annuali per singolo medico (numero prescrizioni e valore generato)."""
    st.subheader("Statistiche annuali per medico")

    data = load_payments()
    medici = data.get("medici", {})
    email_medici = data.get("email_medici", {})
    telefono_medici = data.get("telefono_medici", {})
    nomi_medici = sorted(medici.keys())

    if not nomi_medici:
        st.info("Nessun medico presente. Aggiungi medici dalla sezione Pagamenti.")
        return

    col_m1, col_m2 = st.columns([2, 3])
    with col_m1:
        medico_sel = st.selectbox(
            "Seleziona il medico",
            options=nomi_medici,
            key="stat_medico",
        )

    email = email_medici.get(medico_sel, "")
    cell = telefono_medici.get(medico_sel, "")
    with col_m2:
        contatti = []
        if email:
            contatti.append(f"Email: `{email}`")
        if cell:
            contatti.append(f"Cellulare: `{cell}`")
        if contatti:
            st.markdown(" – ".join(contatti))

    vendite_medico = medici.get(medico_sel, [])
    if not vendite_medico:
        st.info("Nessuna prescrizione registrata per questo medico.")
        return

    # Anni disponibili basati sul campo 'mese' (YYYY-MM)
    anni_disponibili = sorted(
        {
            v.get("mese", "")[:4]
            for v in vendite_medico
            if isinstance(v.get("mese"), str) and len(v.get("mese")) >= 4
        }
    )
    if not anni_disponibili:
        st.info("Non sono presenti informazioni di anno nelle vendite.")
        return

    anno_corrente = str(date.today().year)
    if anno_corrente in anni_disponibili:
        idx_default = anni_disponibili.index(anno_corrente)
    else:
        idx_default = len(anni_disponibili) - 1

    anno_sel = st.selectbox(
        "Anno di riferimento",
        options=anni_disponibili,
        index=idx_default,
        key="stat_anno",
    )

    vendite_anno = [
        v for v in vendite_medico if str(v.get("mese", ""))[:4] == anno_sel
    ]
    if not vendite_anno:
        st.info(f"Nessuna prescrizione registrata per l'anno {anno_sel}.")
        return

    num_prescrizioni = len(vendite_anno)
    totale_valore = sum(v.get("valore", 0.0) for v in vendite_anno)
    totale_commissioni = sum(v.get("commissione", 0.0) for v in vendite_anno)

    st.markdown("---")
    c_stat1, c_stat2, c_stat3 = st.columns(3)
    with c_stat1:
        st.metric("Numero prescrizioni", f"{num_prescrizioni}")
    with c_stat2:
        st.metric("Valore totale vendite", f"{totale_valore:,.2f} €")
    with c_stat3:
        st.metric("Provvigioni totali", f"{totale_commissioni:,.2f} €")

    # Dettaglio per mese dell'anno (utile per bonus)
    st.markdown("##### Dettaglio per mese nell'anno selezionato")
    per_mese = {}
    for v in vendite_anno:
        mese = v.get("mese", "")
        if mese not in per_mese:
            per_mese[mese] = {"n": 0, "valore": 0.0, "commissioni": 0.0}
        per_mese[mese]["n"] += 1
        per_mese[mese]["valore"] += v.get("valore", 0.0)
        per_mese[mese]["commissioni"] += v.get("commissione", 0.0)

    rows = []
    for mese, dati in sorted(per_mese.items()):
        rows.append(
            {
                "mese": mese,
                "numero prescrizioni": dati["n"],
                "valore vendite (€)": round(dati["valore"], 2),
                "provvigioni (€)": round(dati["commissioni"], 2),
            }
        )
    df_mesi = pd.DataFrame(rows)
    st.dataframe(df_mesi, use_container_width=True)

    csv_stat = df_mesi.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Scarica report annuale (CSV)",
        data=csv_stat,
        file_name=f"statistiche_{medico_sel}_{anno_sel}.csv",
        mime="text/csv",
        key="download_statistiche",
    )


def _nome_mese(anno_mese):
    """Da YYYY-MM restituisce 'mese anno' (es. marzo 2026)."""
    if not anno_mese or len(anno_mese) < 7:
        return anno_mese
    try:
        y, m = anno_mese[:4], int(anno_mese[5:7])
        mesi = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
                "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
        return f"{mesi[m]} {y}"
    except Exception:
        return anno_mese


def show_report_totale_area():
    """Report totale di tutti i medici su un solo foglio: per mese o per anno."""
    st.subheader("Report totale – Tutti i medici")

    data = load_payments()
    medici = data.get("medici", {})

    if not medici:
        st.info("Nessun medico presente. Aggiungi medici dalla sezione Pagamenti.")
        return

    # Raccogli tutti i mesi/anni presenti
    tutti_mesi = set()
    for vendite in medici.values():
        for v in vendite:
            m = v.get("mese", "")
            if isinstance(m, str) and len(m) >= 7:
                tutti_mesi.add(m)
    mesi_ordinati = sorted(tutti_mesi, reverse=True)

    tutti_anni = sorted({m[:4] for m in tutti_mesi}) if tutti_mesi else []
    anno_corrente = str(date.today().year)
    idx_anno = len(tutti_anni) - 1
    if anno_corrente in tutti_anni:
        idx_anno = tutti_anni.index(anno_corrente)

    # Scelta periodo: mese o anno
    col_tipo, col_val = st.columns([1, 2])
    with col_tipo:
        tipo_periodo = st.radio(
            "Periodo",
            options=["Per mese", "Per anno"],
            horizontal=True,
            key="report_totale_tipo",
        )
    with col_val:
        if tipo_periodo == "Per mese":
            if not mesi_ordinati:
                st.warning("Nessun dato per nessun mese.")
                return
            periodo_sel = st.selectbox(
                "Seleziona il mese",
                options=mesi_ordinati,
                key="report_totale_mese",
            )
            etichetta_periodo = _nome_mese(periodo_sel)
            filtro = lambda v: v.get("mese") == periodo_sel
        else:
            if not tutti_anni:
                st.warning("Nessun dato per nessun anno.")
                return
            periodo_sel = st.selectbox(
                "Seleziona l'anno",
                options=tutti_anni,
                index=idx_anno,
                key="report_totale_anno",
            )
            etichetta_periodo = str(periodo_sel)
            filtro = lambda v: str(v.get("mese", ""))[:4] == str(periodo_sel)

    # Calcola per ogni medico
    righe = []
    for nome, vendite in medici.items():
        vendite_periodo = [v for v in vendite if filtro(v)]
        if not vendite_periodo:
            continue
        n = len(vendite_periodo)
        valore = sum(v.get("valore", 0.0) for v in vendite_periodo)
        provv = sum(v.get("commissione", 0.0) for v in vendite_periodo)
        righe.append({
            "Medico": nome,
            "Prescrizioni": n,
            "Valore vendite (€)": round(valore, 2),
            "Provvigioni (€)": round(provv, 2),
        })

    if not righe:
        st.info(f"Nessuna prescrizione nel periodo selezionato ({etichetta_periodo}).")
        return

    num_medici = len(righe)
    tot_prescrizioni = sum(r["Prescrizioni"] for r in righe)
    tot_valore = sum(r["Valore vendite (€)"] for r in righe)
    tot_provv = sum(r["Provvigioni (€)"] for r in righe)

    # Riepilogo in evidenza
    if tipo_periodo == "Per mese":
        testo_periodo = f"nel **mese di {etichetta_periodo}**"
    else:
        testo_periodo = f"nell'**anno {etichetta_periodo}**"

    st.markdown(
        f'<div class="report-totale-box">'
        f'<div class="report-totale-title">Riepilogo globale</div>'
        f'<p><strong>{num_medici}</strong> medici in totale {testo_periodo} hanno sviluppato '
        f'<strong>{tot_prescrizioni}</strong> prescrizioni, per un valore vendite di '
        f'<strong>{tot_valore:,.2f} €</strong> e provvigioni totali <strong>{tot_provv:,.2f} €</strong>.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Metriche in card
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Medici attivi", f"{num_medici}")
    with c2:
        st.metric("Prescrizioni totali", f"{tot_prescrizioni}")
    with c3:
        st.metric("Valore vendite", f"{tot_valore:,.2f} €")
    with c4:
        st.metric("Provvigioni totali", f"{tot_provv:,.2f} €")

    # Mini grafico prescrizioni per medico
    df_grafico = pd.DataFrame(righe).set_index("Medico")[["Prescrizioni"]]
    st.bar_chart(df_grafico, height=280)

    # Tabella tutti i medici (un solo foglio)
    st.markdown("##### Dettaglio per medico")
    df_totale = pd.DataFrame(righe)
    st.dataframe(
        df_totale.style.background_gradient(
            subset=["Prescrizioni", "Valore vendite (€)", "Provvigioni (€)"],
            cmap="Blues",
            axis=0,
        ).format({"Valore vendite (€)": "{:,.2f}", "Provvigioni (€)": "{:,.2f}"}),
        use_container_width=True,
    )

    csv_totale = df_totale.to_csv(index=False).encode("utf-8")
    suffisso = periodo_sel.replace("-", "_")
    st.download_button(
        "Scarica report totale (CSV)",
        data=csv_totale,
        file_name=f"report_totale_{suffisso}.csv",
        mime="text/csv",
        key="download_report_totale",
    )


def show_main_app():
    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "utente")

    st.title("Gestione Pagamenti")
    st.write(f"Benvenuto, **{username}**. Ruolo: **{role}**.")

    if role == "admin":
        area = st.sidebar.radio(
            "Area",
            ["Pagamenti", "Storico", "Statistiche", "Report totale", "Amministrazione utenti"],
        )
    else:
        area = st.sidebar.radio(
            "Area", ["Pagamenti", "Storico", "Statistiche", "Report totale"]
        )

    if area == "Amministrazione utenti" and role == "admin":
        show_admin_area()
    elif area == "Storico":
        show_storico_area()
    elif area == "Statistiche":
        show_statistiche_area()
    elif area == "Report totale":
        show_report_totale_area()
    else:
        show_payments_area()

    st.markdown("---")
    if st.button("Esci"):
        st.session_state.clear()
        st.rerun()


def main():
    ensure_admin_user()

    # Login automatico durante lo sviluppo: si entra sempre come admin
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.session_state["logged_in"] = True
        st.session_state["username"] = "admin"
        st.session_state["role"] = "admin"

    show_main_app()


if __name__ == "__main__":
    main()
