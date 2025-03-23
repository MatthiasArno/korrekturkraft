import streamlit as st
import uuid
from datetime import datetime
import correction
from templates.template import templates


data=[]

def get_session_id():
    """Erzeugt oder lädt eine eindeutige Sitzungs-ID"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def main():
    # Eindeutige Sitzungs-ID und Zeitstempel
    session_id = get_session_id()
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.title("Korrektur-HMI")
    with st.expander("Sitzungsinfo", expanded=False):
        st.write(f"Sitzungs-ID: {session_id}")
        st.write(f"Gestartet: {st.session_state.start_time}")
        if st.button("Neue Sitzung starten"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    


     # Dropdown für Vorlagen
    st.header("Vorlagen")
    selected_template = st.selectbox(
        "Vorlage auswählen",
        options=list(templates.keys()),
        key="selected_template"
    )
    
    # Anwenden-Button für die Vorlage
    if st.button("Vorlage anwenden"):
        if selected_template != "Auswählen...":
            st.session_state.korrekturanweisung = templates[selected_template]["korrektur"]
            st.session_state.arbeitsanweisung = templates[selected_template]["arbeitsanweisung"]
            st.session_state.file_data["template"] = templates[selected_template]["template"]
            st.rerun()
    

    # R-1: Textfeld für Korrekturanweisung
    st.header("Korrekturanweisung")
    korrekturanweisung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen
        max_chars=80*50,  # Max. 80x50 Zeichen
        placeholder="Bitte hier die Korrekturanweisung hinterlegen", # correction.system_context,
        key="korrekturanweisung"  # Key zum Speichern im Session State
    )
    
    # R-2: Textfeld für Arbeitsanweisung
    st.header("Arbeitsanweisung")
    arbeitsanweisung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen
        max_chars=80*50,  # Max. 80x50 Zeichen
        placeholder="Bitte hier die Aufgabenbeschreibung hinterlegen", # correction.task_context,
        key="arbeitsanweisung"  # Key zum Speichern im Session State
    )
        
    # R-3 & R-4: File Picker und Upload-Button
    st.header("Datei-Upload")
    uploaded_files = st.file_uploader(
        label="Dateien auswählen. Aktuell nur .txt Format.",
        type=None,  # Alle Dateitypen erlauben
        accept_multiple_files=True,
        key="uploaded_files"  # Key zum Speichern im Session State
    )

    st.header("Template-Upload")
    uploaded_template = st.file_uploader(
        label="Datei auswählen. Aktuell nur .html Format.",
        type="html",
        accept_multiple_files=False,
        key="uploaded_template"  # Key zum Speichern im Session State
    )

    if "upload" not in st.session_state.file_data:
        st.session_state.file_data["upload"]=dict()
    if "text" not in st.session_state.file_data:
        st.session_state.file_data["text"]=dict()
    if "template" not in st.session_state.file_data:
        st.session_state.file_data["template"]=None


    if uploaded_template:     
        file=uploaded_template      
        st.session_state.file_data["template"]=file.read().decode("utf-8")
        # Dateizeiger zurücksetzen für weitere Operationen        
        # Zeige Dateiinformationen an
    
    # Verarbeite und speichere hochgeladene Dateien
    if uploaded_files:
        st.write(f"{len(uploaded_files)} Datei(en) hochgeladen:")       
        # Speichere Dateiinhalte im Session State
        for file in uploaded_files:
            # Nur speichern, wenn noch nicht im Session State
            if file.name not in st.session_state.file_data:
                file_bytes = file.read()
                st.session_state.file_data["upload"][file.name] = {
                    'content': file_bytes,
                    'size': file.size,
                    'type': file.type,
                    'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                # Dateizeiger zurücksetzen für weitere Operationen
                file.seek(0)
            
            # Zeige Dateiinformationen an
            st.write(f"- {file.name} ({file.size} Bytes)")
            
    # Anzeige gespeicherter Dateien aus früheren Uploads
    stored_files = [f for f in st.session_state.file_data["upload"].keys() 
                    if f not in [getattr(file, 'name', '') for file in uploaded_files or []]]
    if stored_files:
        st.write("Gespeicherte Dateien aus früheren Uploads:")
        for filename in stored_files:
            fileinfo = st.session_state.file_data["upload"][filename]
            st.write(f"- {filename} ({fileinfo['size']} Bytes)")
            if st.button(f"Entfernen: {filename}", key=f"remove_{filename}"):
                del st.session_state.file_data["upload"][filename]
                st.experimental_rerun()

    for filename in st.session_state.file_data["upload"]:      
        if filename.endswith(".txt"):
            if not filename in st.session_state.file_data["text"]:
                st.session_state.file_data["text"][filename]= st.session_state.file_data["upload"][filename]["content"]              
       

    # R-5: Textfeld für Bewertung
    st.header("Bewertung")
    bewertung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen      
        max_chars=160*50,  # Max. 80x50 Zeichen
        placeholder="Hier erscheint die Bewertung...",
        value=st.session_state.bewertung,
        key="bewertung_input"
    )

    if st.session_state.bewertung:
        st.markdown(st.session_state.bewertung, unsafe_allow_html=True)

    # Buttons in einer Zeile anordnen
    col1, col2, col3 = st.columns(3)
    
    # R-6: Button "Korrektur starten"
    with col1:
        if st.button("Korrektur starten", type="primary"):
            # Hier kommt die Logik für die Korrektur
            # Beispielimplementierung für die Simulation einer Korrektur
            if st.session_state.korrekturanweisung and st.session_state.arbeitsanweisung:
                # Verarbeite die Eingaben und erstelle eine Bewertung
                num_files = len(st.session_state.file_data)
                st.session_state.bewertung = correction.run_correction(
                        st.session_state.file_data["template"],
                        dict([(key, value["content"].decode("utf-8")) for key, value in st.session_state.file_data["upload"].items()]),
                        st.session_state.korrekturanweisung,
                        st.session_state.arbeitsanweisung
                )
                st.rerun()
            else:
                st.error("Bitte fülle Korrekturanweisung und Arbeitsanweisung aus.")
    
    # R-5: Download-Button für Bewertung
    with col2:
        if st.session_state.bewertung:
            st.download_button(
                label="Bewertung herunterladen",
                data=st.session_state.bewertung,
                file_name=f"bewertung_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
    
    # Sitzungsverwaltung
    with col3:
        if st.button("Sitzung zurücksetzen"):
            # Bestimmte Schlüssel behalten (optional)
            keys_to_keep = ["session_id", "start_time"]
            
            # Alle anderen Schlüssel löschen
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            
            # Initialisiere Hauptwerte neu
            st.session_state.bewertung = ""
            st.session_state.file_data = {}
            st.session_state.korrekturanweisung = ""
            st.session_state.arbeitsanweisung = ""
            
            st.experimental_rerun()

if __name__ == "__main__":
    # Session State für persistente Daten initialisieren
    if 'bewertung' not in st.session_state:
        st.session_state.bewertung = ""
    
    # Initialisiere Datenspeicherung für Uploads
    if 'file_data' not in st.session_state:
        st.session_state.file_data = {}
    
    # Initialisiere Eingabefelder
    if 'korrekturanweisung' not in st.session_state:
        st.session_state.korrekturanweisung = ""
    if 'arbeitsanweisung' not in st.session_state:
        st.session_state.arbeitsanweisung = ""
        
    main()