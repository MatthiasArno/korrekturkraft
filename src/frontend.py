import streamlit as st

def main():
    st.title("Korrektur-HMI")
    
    # R-1: Textfeld für Korrekturanweisung
    st.header("Korrekturanweisung")
    korrekturanweisung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen
        max_chars=80*50,  # Max. 80x50 Zeichen
        placeholder="Geben Sie hier Ihre Korrekturanweisung ein..."
    )
    
    # R-2: Textfeld für Arbeitsanweisung
    st.header("Arbeitsanweisung")
    arbeitsanweisung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen
        max_chars=80*50,  # Max. 80x50 Zeichen
        placeholder="Geben Sie hier Ihre Arbeitsanweisung ein..."
    )
    
    # R-3 & R-4: File Picker und Upload-Button
    st.header("Datei-Upload")
    uploaded_files = st.file_uploader(
        label="Dateien auswählen",
        type=None,  # Alle Dateitypen erlauben
        accept_multiple_files=True
    )
    
    # Anzeige der hochgeladenen Dateien
    if uploaded_files:
        st.write(f"{len(uploaded_files)} Datei(en) hochgeladen:")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size} Bytes)")
    
    # R-5: Textfeld für Bewertung
    st.header("Bewertung")
    bewertung = st.text_area(
        label="",
        height=300,  # Ungefähr 50 Zeilen
        max_chars=80*50,  # Max. 80x50 Zeichen
        placeholder="Hier erscheint die Bewertung..."
    )
    
    # Buttons in einer Zeile anordnen
    col1, col2, col3 = st.columns(3)
    
    # R-6: Button "Korrektur starten"
    with col1:
        if st.button("Korrektur starten", type="primary"):
            # Hier kommt die Logik für die Korrektur
            st.session_state.bewertung = "Beispiel-Bewertung nach der Korrektur..."
            st.experimental_rerun()
    
    # R-7: Download-Button für Bewertung
    with col2:
        if bewertung:
            st.download_button(
                label="Bewertung herunterladen",
                data=bewertung,
                file_name="bewertung.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    # Session State für persistente Daten initialisieren
    if 'bewertung' not in st.session_state:
        st.session_state.bewertung = ""
        
    main()