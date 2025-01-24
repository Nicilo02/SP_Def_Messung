import os
import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import openpyxl
import datetime
import seaborn as sns

st.set_page_config(
    page_title="Berechnung Deformationsmessung",
    page_icon="✨",
    layout="centered",  # Optionen: "centered" (Standard), "wide"
    initial_sidebar_state="expanded"  # Optionen: "auto", "expanded", "collapsed"
)

# Einfügen des Logos
col1, col2 = st.columns([1, 3])  # Spalte 1 für Logo, Spalte 2 für andere Inhalte

with col1:
    st.image("https://www.athletes-network.com/wp-content/uploads/2023/06/Emch_Berger_Website.png", width=200)  # Pfad zum Logo anpassen

with col2:
    st.title("Auswertung Deformationsmessung!")
    
tab1, tab2, tab3 = st.tabs(["Import Dateien", "Differenzen Nullmessung", "Differenzen Folgemessung"])


# Temporäre Datei für die Datenbank
DB_PATH = "Defmes_data.db"

# Temporäre Datei für die Differenzen
DIFFERENCES_FILE = "Differenzen.csv"
DIFFERENCES_FILE_FOLGE = 'Differenzen_Folgemess'
LAST_NULL_FILE = "Excelfiles/Nullmessung.csv"

# Funktion zum Einlesen der CSV-Datei
def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data

# Funktion zum Hinzufügen oder Überprüfen der Kopfzeile
def add_header_to_csv(file_path):
    # Die gewünschte Kopfzeile festlegen
    desired_header = ['Punktnummer', 'X', 'Y', 'Z', 'Objektcode']

    # CSV-Datei lesen (nur die erste Zeile einlesen)
    first_row = pd.read_csv(file_path, nrows=1)  # Nur die erste Zeile einlesen

    # Überprüfung, ob die Datei bereits eine Kopfzeile hat
    if list(first_row.columns) == desired_header:
        print("Die Datei enthält bereits die korrekte Kopfzeile.")
        return pd.read_csv(file_path)  # Datei zurückgeben, wenn Kopfzeile korrekt ist
    else:
        print("Die Datei hat eine falsche Kopfzeile oder keine Kopfzeile.")
        
    # Datei ohne Kopfzeile einlesen
    current_data = pd.read_csv(file_path, header=None)

    # Wenn die Spaltenanzahl nicht übereinstimmt, Fehlermeldung ausgeben und Werte ergänzen
    if current_data.shape[1] == len(desired_header) - 1:
        specific_value = input("Welchen Wert sollte der Objektcode haben? ").strip()
        current_data['Objektcode'] = specific_value
    elif current_data.shape[1] != len(desired_header):
        print("Fehler: Die Datei hat eine falsche Anzahl an Spalten. Es können keine Änderungen vorgenommen werden.")
        return None

    # Kopfzeile hinzufügen oder überschreiben
    current_data.columns = desired_header

    # Die neue Datei speichern
    output_file = input("Wie soll die neue Datei heißen? ") or "output_with_new_header.csv"
    current_data.to_csv(output_file, index=False)
    print(f"CSV-Datei mit neuer Kopfzeile wurde unter {output_file} gespeichert.")
    
    return current_data

def create_database():
    """Erstellt eine SQLite-Datenbank, wenn sie nicht existiert."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messungen (
            Punktnummer TEXT,
            X REAL,
            Y REAL,
            Z REAL,
            Objektcode TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def delete_duplicates():
    conn = sqlite3.connect('Defmes_data.db')
    cursor = conn.cursor()

    # SQL-Abfrage zum Löschen von Duplikaten
    cursor.execute('''
        DELETE FROM messungen
        WHERE ROWID NOT IN (
            SELECT MIN(ROWID)
            FROM messungen
            GROUP BY Punktnummer, X, Y, Z, Objektcode
        );
    ''')

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

delete_duplicates()


def save_data_to_db(data):
    """Speichert die Daten der Nullmessung in die SQLite-Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO messungen (Punktnummer, X, Y, Z, Objektcode)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Punktnummer'], row['X'], row['Y'], row['Z'], row['Objektcode']))
    conn.commit()
    conn.close()

def calculate_differences(data_new, output_path):
    """Berechnet die Differenzen zwischen der Nullmessung und den neuen Daten."""
    conn = sqlite3.connect(DB_PATH)
    nullmessung = pd.read_sql_query("SELECT * FROM messungen", conn)

    # Verbinden der Daten
    merged_data = pd.merge(nullmessung, data_new, on='Punktnummer', suffixes=('_Null', '_New'))

    # Differenzen berechnen
    merged_data['X_diff'] = merged_data['X_New'] - merged_data['X_Null']
    merged_data['Y_diff'] = merged_data['Y_New'] - merged_data['Y_Null']
    merged_data['Z_diff'] = merged_data['Z_New'] - merged_data['Z_Null']

    # Auf 3 Dezimalstellen runden
    merged_data = merged_data.round({'X_diff': 3, 'Y_diff': 3, 'Z_diff': 3})
    
    # Prüfen, ob ein Punkt ignoriert werden soll
    if ignored_point:
        # Filter für den Punkt
        ignored_row = merged_data[merged_data['Punktnummer'] == ignored_point]
        # Wenn der Punkt existiert, markieren
        if not ignored_row.empty:
            ignored_entry = pd.DataFrame({
                'Punktnummer': [ignored_point],
                'X_diff': ['nicht Gemessen'],
                'Y_diff': ['nicht Gemessen'],
                'Z_diff': ['nicht Gemessen']
            })
            # Entferne den Punkt aus der Berechnung
            merged_data = merged_data[merged_data['Punktnummer'] != ignored_point]
            # Füge die markierte Zeile hinzu
            result = pd.concat([merged_data[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']], ignored_entry])
        else:
            # Falls der Punkt nicht in der Nullmessung ist, einfach weitermachen
            result = merged_data[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']]
    else:
        # Keine Punkte ignorieren
        result = merged_data[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']]

    # Differenzen speichern
    result.to_csv(output_path, index=False)

    conn.close()
    return result

def calculate_differences_folgemessung (data_folge, output_path_folg):
    """Berechnet die Differenzen zwischen den Folgemessungen."""
    conn = sqlite3.connect(DB_PATH)
    folgemessung = pd.read_sql_query(f'SELECT * FROM {new_table_name}', conn)
    
    #Verbindung der Daten
    merged_data_2 = pd.merge(folgemessung, data_folge, on='Punktnummer', suffixes=('_Null', '_New'))
    
    # Differenzen berechnen
    merged_data_2['X_diff'] = merged_data_2['X_New'] - merged_data_2['X_Null']
    merged_data_2['Y_diff'] = merged_data_2['Y_New'] - merged_data_2['Y_Null']
    merged_data_2['Z_diff'] = merged_data_2['Z_New'] - merged_data_2['Z_Null']
    
    # Auf 3 Dezimalstellen runden
    merged_data_2 = merged_data_2.round({'X_diff': 3, 'Y_diff': 3, 'Z_diff': 3})
    
    
    result_2 = merged_data_2[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']]
    result_2.to_csv(output_path_folg, index=False)
    
    conn.close()
    return result_2

# --- Streamlit Interface ---
# Schritt 1: Hochladen der Nullmessung
with tab1:
    st.header("Schritt 1: Nullmessung hochladen")

    use_last_null_file = st.checkbox("Zuletzt hochgeladene Nullmessung verwenden")

    if use_last_null_file:
        if os.path.exists(LAST_NULL_FILE):
            null_data = add_header_to_csv(LAST_NULL_FILE)
            if null_data is not None:
                st.success("Zuletzt hochgeladene Nullmessung wurde verwendet.")
        else:
            st.error("Es wurde noch keine Nullmessung hochgeladen.")
            null_data = None
    else:
        uploaded_null_file = st.file_uploader("Laden Sie die Nullmessung als CSV-Datei hoch", type="csv", key= 'file_uploader_1')
        if uploaded_null_file is not None:
            with open("temp_uploaded_null_file.csv", "wb") as f:
                f.write(uploaded_null_file.getbuffer())
            null_data = add_header_to_csv("temp_uploaded_null_file.csv")
            if null_data is not None:
                null_data.to_csv(LAST_NULL_FILE, index=False)  # Speichern als zuletzt hochgeladene Datei
                st.success("Nullmessung wurde erfolgreich hochgeladen.")
        else:
            null_data = None

# Punkt hinzufügen, falls gewünscht
    if null_data is not None:
        add_point = st.checkbox("Möchten Sie einen weiteren Punkt zur Nullmessung hinzufügen?")
        if add_point:
            punktnummer = st.text_input("Punktnummer") 
            x_coord = st.number_input("X-Koordinate", format="%.3f",min_value = 2400000, max_value = 2900000)
            y_coord = st.number_input("Y-Koordinate", format="%.3f",min_value = 1000000, max_value= 1300000)
            z_coord = st.number_input("Z-Koordinate", format="%.3f")
            objektcode = st.text_input("Objektcode")

            if st.button("Punkt hinzufügen"):
                new_row = pd.DataFrame([{
                    'Punktnummer': punktnummer,
                    'X': x_coord,
                    'Y': y_coord,
                    'Z': z_coord,
                    'Objektcode': objektcode
                }])
                null_data = pd.concat([null_data, new_row], ignore_index=True)
                null_data.to_csv(LAST_NULL_FILE, index=False)
                st.success("Der neue Punkt wurde zur Nullmessung hinzugefügt.")

    # Nullmessung speichern und in Datenbank einfügen
        create_database()
        save_data_to_db(null_data)
        delete_duplicates()
        st.write("Aktuelle Nullmessung:")
        st.dataframe(null_data)
    
    # Schritt 2.1: Hochladen der neuen Messung
    st.header("Schritt 2.1: Neue Messung hochladen")
    uploaded_new_file = st.file_uploader("Laden Sie die neue Messung als CSV-Datei hoch", type="csv", key='file_uploader_2')

    if uploaded_new_file is not None:
        try:
            # Neue Messung einlesen
            with open("temp_uploaded_new_file.csv", "wb") as f:
                f.write(uploaded_new_file.getbuffer())

            # Kopfzeile der neuen Messung überprüfen oder hinzufügen
            new_data = add_header_to_csv("temp_uploaded_new_file.csv")

            if new_data is not None:
                # Neue Messung überprüfen
                st.write("Vorschau der neuen Messung:")
                st.dataframe(new_data)
            
                ignored_point_checkbox = st.checkbox('Einen Punkt von der Differenzberechnung ausschließen')
                ignored_point = None
                if ignored_point_checkbox:
                    ignored_point = st.text_input("Geben Sie den Punkt ein, der ignoriert werden soll:")
            
                conn = sqlite3.connect(DB_PATH)

                # Generiere einen eindeutigen Tabellennamen basierend auf dem aktuellen Zeitstempel
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_table_name = f"NeueMessung_{timestamp}"

                # Speichern der neuen Messung in der Datenbank
                new_data.to_sql(new_table_name, conn, if_exists="fail", index=False)
                st.success(f"Die neue Messung wurde erfolgreich in der Tabelle '{new_table_name}' gespeichert.")

                # Differenzen berechnen
                differences = calculate_differences(new_data, DIFFERENCES_FILE_FOLGE)

                # Differenzen anzeigen
                st.write("Berechnete Differenzen:")
                st.dataframe(differences)

                # Differenzen als Download bereitstellen
                st.download_button(
                    label="Differenzen herunterladen",
                    data=open(DIFFERENCES_FILE_FOLGE, "rb").read(),
                    file_name="Differenzen.csv",
                    mime="text/csv",
                    key= 'download_button_1'
                )

                st.success("Differenzen wurden erfolgreich berechnet und gespeichert.")
            else:
                st.error("Die neue Messung konnte aufgrund einer fehlerhaften Kopfzeile nicht verarbeitet werden.")
        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der neuen Messung: {e}")
    else:
        st.info("Bitte laden Sie eine neue Messung hoch, um die Differenzen zu berechnen.")
    
    # Schritt 2.2: Hochladen der neuen Messung
    st.header("Schritt 2: Neue Messung hochladen")
    uploaded_new_folg_1 = st.file_uploader("Laden Sie die neue Messung als CSV-Datei hoch", type="csv")

    if uploaded_new_folg_1 is not None:
        try:
         # Neue Messung einlesen
            with open("temp_uploaded_new_file.csv", "wb") as f:
             f.write(uploaded_new_folg_1.getbuffer())

            # Kopfzeile der neuen Messung überprüfen oder hinzufügen
            new_data_folg = add_header_to_csv("temp_uploaded_new_file.csv")

            if new_data_folg is not None:
                # Neue Messung überprüfen
                st.write("Vorschau der neuen Messung:")
                st.dataframe(new_data)

                # Differenzen berechnen
                differences = calculate_differences_folgemessung(new_data_folg, DIFFERENCES_FILE)

                # Differenzen anzeigen
                st.write("Berechnete Differenzen:")
                st.dataframe(differences)

                # Differenzen als Download bereitstellen
                st.download_button(
                    label="Differenzen herunterladen",
                    data=open(DIFFERENCES_FILE, "rb").read(),
                    file_name="Differenzen.csv",
                    mime="text/csv",
                    key= 'download_button_2'
                )

                st.success("Differenzen wurden erfolgreich berechnet und gespeichert.")
            else:
                st.error("Die neue Messung konnte aufgrund einer fehlerhaften Kopfzeile nicht verarbeitet werden.")
        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der neuen Messung: {e}")
    else:
        st.info("Bitte laden Sie eine neue Messung hoch, um die Differenzen zu berechnen.")

# --- Schritt 3: Diagramme erstellen ---
uploaded_diff_file = DIFFERENCES_FILE
uploaded_folg_diff = DIFFERENCES_FILE_FOLGE

with tab2:
    st.header("Schritt 3: Liniendiagramme der Abweichungen")

    if uploaded_diff_file is not None:
        # CSV-Datei einlesen
        df = pd.read_csv(uploaded_diff_file)

        # Überblick über die Daten
        st.write("Daten aus der hochgeladenen CSV-Datei:")
        st.dataframe(df.head())

        # Benutzer-Eingaben für Spaltennamen
        category_col = st.text_input("Gib den Namen der Kategorie-Spalte ein (leer lassen für Index):")
        point_number_col = 'Punktnummer'
        deviation_x_col = 'X_diff'
        deviation_y_col = 'Y_diff'
        deviation_z_col = 'Z_diff'

        # Daten für Diagramme vorbereiten
        x_labels = df[category_col] if category_col in df.columns else df.index
        y_values_x = df[deviation_x_col]
        y_values_y = df[deviation_y_col]
        y_values_z = df[deviation_z_col]
        point_numbers = df[point_number_col]

    # --- Diagramm 1: X_diff ---
        st.subheader("Liniendiagramm der Abweichungen: X_diff")
        fig_x, ax_x = plt.subplots(figsize=(10, 6))
        ax_x.plot(x_labels, y_values_x, marker=".", linestyle="-", color="Orange", label="X_diff (Abweichung)")
        ax_x.axhline(0, color="black", linestyle="--", linewidth=1.0)
        for x, y_x, point_num in zip(x_labels, y_values_x, point_numbers):
            ax_x.annotate(str(point_num), (x, y_x), textcoords="offset points", xytext=(5, 10), ha="center",
                        rotation=90, fontsize=9, color="darkred")
        ax_x.set_title("Liniendiagramm der Abweichungen: X_diff")
        ax_x.set_xlabel("Kategorie" if category_col else "Index")
        ax_x.set_ylabel("Abweichung")
        ax_x.tick_params(axis='x', rotation=45)
        ax_x.legend()
        st.pyplot(fig_x)

    # --- Diagramm 2: Y_diff ---
        st.subheader("Liniendiagramm der Abweichungen: Y_diff")
        fig_y, ax_y = plt.subplots(figsize=(10, 6))
        ax_y.plot(x_labels, y_values_y, marker=".", linestyle="-", color="Blue", label="Y_diff (Abweichung)")
        ax_y.axhline(0, color="black", linestyle="--", linewidth=0.5)
        for x, y_y, point_num in zip(x_labels, y_values_y, point_numbers):
            ax_y.annotate(str(point_num), (x, y_y), textcoords="offset points", xytext=(5, 10), ha="right",
                          rotation=90, fontsize=9, color="darkblue")
        ax_y.set_title("Liniendiagramm der Abweichungen: Y_diff")
        ax_y.set_xlabel("Kategorie" if category_col else "Index")
        ax_y.set_ylabel("Abweichung")
        ax_y.tick_params(axis='x', rotation=45)
        ax_y.legend()
        st.pyplot(fig_y)

    # --- Diagramm 3: Z_diff ---
        st.subheader("Liniendiagramm der Abweichungen: Höhendifferenz")
        fig_z, ax_z = plt.subplots(figsize=(10, 6))
        ax_z.plot(x_labels, y_values_z, marker=".", linestyle="-", color="Green", label="Z_diff (Abweichung)")
        ax_z.axhline(0, color="black", linestyle="--", linewidth=0.5)
        for x, y_z, point_num in zip(x_labels, y_values_z, point_numbers):
            ax_z.annotate(str(point_num), (x, y_z), textcoords="offset points", xytext=(5, 10), ha="right",
                          rotation=90, fontsize=9, color="darkblue")
        ax_z.set_title("Liniendiagramm der Abweichungen: Z_diff")
        ax_z.set_xlabel("Kategorie" if category_col else "Index")
        ax_z.set_ylabel("Abweichung")
        ax_z.tick_params(axis='x', rotation=45)
        ax_z.legend()
        st.pyplot(fig_z)
    else:
        st.info("Bitte laden Sie die Differenzen-Datei hoch, um die Diagramme zu sehen.")

with tab3:
    st.header("Schritt 4: Liniendiagramme der Abweichungen")
    
    if uploaded_folg_diff is not None:
        # CSV-Datei einlesen
        df = pd.read_csv(uploaded_folg_diff)

        # Überblick über die Daten
        st.write("Daten aus der hochgeladenen CSV-Datei:")
        st.dataframe(df.head())

        # Benutzer-Eingaben für Spaltennamen
        category_col = st.text_input("Gib den Namen der Kategorie-Spalte ein (leer lassen für Index):", key= 'upload_2')
        point_number_col = 'Punktnummer'
        deviation_x_col = 'X_diff'
        deviation_y_col = 'Y_diff'
        deviation_z_col = 'Z_diff'

        # Daten für Diagramme vorbereiten
        x_labels = df[category_col] if category_col in df.columns else df.index
        y_values_x = df[deviation_x_col]
        y_values_y = df[deviation_y_col]
        y_values_z = df[deviation_z_col]
        point_numbers = df[point_number_col]

    # --- Diagramm 1: X_diff ---
        st.subheader("Liniendiagramm der Abweichungen: X_diff")
        fig_x, ax_x = plt.subplots(figsize=(10, 6))
        ax_x.plot(x_labels, y_values_x, marker=".", linestyle="-", color="Orange", label="X_diff (Abweichung)")
        ax_x.axhline(0, color="black", linestyle="--", linewidth=1.0)
        for x, y_x, point_num in zip(x_labels, y_values_x, point_numbers):
            ax_x.annotate(str(point_num), (x, y_x), textcoords="offset points", xytext=(5, 10), ha="center",
                        rotation=90, fontsize=9, color="darkred")
        ax_x.set_title("Liniendiagramm der Abweichungen: X_diff")
        ax_x.set_xlabel("Kategorie" if category_col else "Index")
        ax_x.set_ylabel("Abweichung")
        ax_x.tick_params(axis='x', rotation=45)
        ax_x.legend()
        st.pyplot(fig_x)

    # --- Diagramm 2: Y_diff ---
        st.subheader("Liniendiagramm der Abweichungen: Y_diff")
        fig_y, ax_y = plt.subplots(figsize=(10, 6))
        ax_y.plot(x_labels, y_values_y, marker=".", linestyle="-", color="Blue", label="Y_diff (Abweichung)")
        ax_y.axhline(0, color="black", linestyle="--", linewidth=0.5)
        for x, y_y, point_num in zip(x_labels, y_values_y, point_numbers):
            ax_y.annotate(str(point_num), (x, y_y), textcoords="offset points", xytext=(5, 10), ha="right",
                          rotation=90, fontsize=9, color="darkblue")
        ax_y.set_title("Liniendiagramm der Abweichungen: Y_diff")
        ax_y.set_xlabel("Kategorie" if category_col else "Index")
        ax_y.set_ylabel("Abweichung")
        ax_y.tick_params(axis='x', rotation=45)
        ax_y.legend()
        st.pyplot(fig_y)

    # --- Diagramm 3: Z_diff ---
        st.subheader("Liniendiagramm der Abweichungen: Höhendifferenz")
        fig_z, ax_z = plt.subplots(figsize=(10, 6))
        ax_z.plot(x_labels, y_values_z, marker=".", linestyle="-", color="Green", label="Z_diff (Abweichung)")
        ax_z.axhline(0, color="black", linestyle="--", linewidth=0.5)
        for x, y_z, point_num in zip(x_labels, y_values_z, point_numbers):
            ax_z.annotate(str(point_num), (x, y_z), textcoords="offset points", xytext=(5, 10), ha="right",
                          rotation=90, fontsize=9, color="darkblue")
        ax_z.set_title("Liniendiagramm der Abweichungen: Z_diff")
        ax_z.set_xlabel("Kategorie" if category_col else "Index")
        ax_z.set_ylabel("Abweichung")
        ax_z.tick_params(axis='x', rotation=45)
        ax_z.legend()
        st.pyplot(fig_z)
    else:
        st.info("Bitte laden Sie die Differenzen-Datei hoch, um die Diagramme zu sehen.")
