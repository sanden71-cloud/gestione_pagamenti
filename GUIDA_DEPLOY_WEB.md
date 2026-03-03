# Guida passo passo: mettere l’app sul web (gratis)

Segui i passi in ordine. Un passo alla volta.

---

## PARTE 1 – Mettere il progetto su GitHub

L’app deve stare su GitHub prima di poterla pubblicare su Streamlit. Se non hai mai usato GitHub, segui così.

### Passo 1.1 – Account GitHub
- Vai su **https://github.com**
- Se non hai un account: clicca **Sign up** e creane uno (email + password).
- Se ce l’hai già: fai **Sign in**.

### Passo 1.2 – Creare un “repository” (la cartella del progetto su GitHub)
- Dopo il login, in alto a destra clicca sul **+** e scegli **New repository**.
- **Repository name:** scrivi un nome, ad esempio: `gestione-pagamenti` (tutto attaccato, minuscolo).
- Lascia **Public**.
- **Non** spuntare “Add a README” (il README ce l’hai già nel progetto).
- Clicca **Create repository**.

### Passo 1.3 – Caricare i file del progetto
Dopo “Create repository” vedrai una pagina con istruzioni. Ignora i comandi Git per ora e usa il metodo con **drag & drop**:

- Sulla pagina del repository cerca la scritta **“uploading an existing file”** (carica un file esistente) e cliccaci.
- Oppure trascina i file direttamente nella finestra del browser.

Carica **questi 3 file** dalla cartella “Software Gestione Pagamenti”:
1. **pagamenti.py**
2. **requirements.txt**
3. **README.md** (opzionale ma utile)

- Trascinali nella zona di upload (o clicca e scegli i file).
- In basso scrivi un messaggio tipo: `Primo caricamento`.
- Clicca **Commit changes**.

Ora il tuo progetto è su GitHub. L’indirizzo sarà tipo:  
`https://github.com/TUO-USERNAME/gestione-pagamenti`  
(dove TUO-USERNAME è il tuo nome utente GitHub).

---

## PARTE 2 – Pubblicare l’app su Streamlit

### Passo 2.1 – Aprire Streamlit Cloud
- Vai su **https://share.streamlit.io**
- Clicca **Sign up** o **Sign in** e accedi **con il tuo account GitHub** (così Streamlit vede i tuoi repository).

### Passo 2.2 – Avviare un nuovo deploy
- Clicca **“New app”** (o “Deploy an app” / “Deploy”).

### Passo 2.3 – Compilare il form (un campo alla volta)

**Campo 1 – Repository**
- Dove chiede il repository scrivi: **TUO-USERNAME/gestione-pagamenti**
  - Esempio: se il tuo utente è `mariorossi`, scrivi: `mariorossi/gestione-pagamenti`
- Oppure clicca “Paste GitHub URL” e incolla:  
  `https://github.com/TUO-USERNAME/gestione-pagamenti`

**Campo 2 – Branch**
- Lascia **master** (o, se GitHub ti ha creato il repo con branch **main**, scrivi **main**).

**Campo 3 – Main file path**
- Cancella quello che c’è (`streamlit_app.py`) e scrivi **solo**:  
  **pagamenti.py**

**Campo 4 – App URL**
- Lascia vuoto.

### Passo 2.4 – Deploy
- Clicca il pulsante blu **Deploy**.

### Passo 2.5 – Attendere
- Comparirà “Building…” / “Deploying…”. Aspetta 2–5 minuti.
- Quando finisce vedrai un link tipo: `https://gestione-pagamenti-xxxx.streamlit.app`
- Clicca sul link: si aprirà la tua app nel browser. Da quel momento puoi usarla da qualsiasi dispositivo.

---

## Riepilogo veloce

| Dove | Cosa fare |
|------|-----------|
| github.com | Creare account → New repository → caricare pagamenti.py, requirements.txt, README |
| share.streamlit.io | Accedi con GitHub → New app → Repository: username/nome-repo → Main file: **pagamenti.py** → Deploy |

Se un passo non ti riesce, scrivi **a quale passo sei** (es. “Passo 1.2”) e cosa vedi sullo schermo, così possiamo correggere solo quello.
