# Software Gestione Pagamenti

## Uso da Dropbox (più computer)

Puoi mettere **tutta la cartella del progetto** in Dropbox e usarla da qualsiasi PC.

- **Cosa sincronizza Dropbox:** `pagamenti.py`, `requirements.txt`, README e (in futuro) i file di dati (es. CSV, database) se li mettiamo dentro la cartella del progetto.
- **Su ogni computer:** devi avere Python installato. Poi apri la cartella (da Dropbox), crei un ambiente virtuale **sul quel PC** e installi le dipendenze (vedi sotto). Non usare il `venv` creato su un altro computer.
- **Consiglio:** nelle impostazioni di Dropbox (Selective Sync / Sincronizzazione selettiva) escludi la cartella `venv` da questa progetto, così non si sincronizzano centinaia di file inutili. Il file `.dropboxignore` elenca cosa conviene non sincronizzare.

---

## Esecuzione su un ambiente web gratuito

Puoi far girare l’app su internet e aprirla da qualsiasi dispositivo senza installare nulla. Opzione consigliata: **Streamlit Community Cloud** (gratuito).

1. **Crea un repository su GitHub** con il contenuto di questa cartella (almeno `pagamenti.py` e `requirements.txt`).
2. Vai su **[share.streamlit.io](https://share.streamlit.io)**, accedi con GitHub e clicca **“New app”**.
3. Scegli il repository e il branch; in **“Main file path”** inserisci: `pagamenti.py`.
4. Clicca **“Deploy”**. Dopo qualche minuto avrai un link tipo `https://tuoprogetto.streamlit.app` per usare l’app dal browser.

**Alternative gratuite:** [Hugging Face Spaces](https://huggingface.co/spaces) (supporta Streamlit), [Render](https://render.com), [Railway](https://railway.app) (piani free con limiti).

Se in futuro l’app salverà dati (file, database), in ambiente web andranno usati servizi cloud (es. database online o storage) invece di file solo sul PC.

---

## Avvio (in locale)

1. Entra nella cartella (percorso può cambiare se è in Dropbox):
   ```bash
   cd "percorso/Software Gestione Pagamenti"
   ```

2. Crea e attiva un ambiente virtuale (da fare su ogni computer):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # su Windows: venv\Scripts\activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Avvia l'app:
   ```bash
   streamlit run pagamenti.py
   ```

L'app si aprirà nel browser (di solito http://localhost:8501).
