import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit-App
st.title("Liniendiagramme der Abweichungen")

# Datei-Upload
uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type=["csv"])
if uploaded_file is not None:
    # CSV-Datei einlesen
    df = pd.read_csv(uploaded_file)

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
    ax_x.axhline(0, color="black", linestyle="--", linewidth=0.8)

    # Punktnummern hinzufügen
    for x, y_x, point_num in zip(x_labels, y_values_x, point_numbers):
        ax_x.annotate(
            str(point_num),
            (x, y_x),
            textcoords="offset points",
            xytext=(5, 10),
            ha="center",
            rotation=90,
            fontsize=9,
            color="darkred",
        )

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
    ax_y.axhline(0, color="black", linestyle="--", linewidth=0.8)

    # Punktnummern hinzufügen
    for x, y_y, point_num in zip(x_labels, y_values_y, point_numbers):
        ax_y.annotate(
            str(point_num),
            (x, y_y),
            textcoords="offset points",
            xytext=(5, 10),
            ha="center",
            rotation=90,
            fontsize=9,
            color="darkblue",
        )

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
    ax_z.axhline(0, color="black", linestyle="--", linewidth=0.8)

    # Punktnummern hinzufügen
    for x, y_z, point_num in zip(x_labels, y_values_z, point_numbers):
        ax_z.annotate(
            str(point_num),
            (x, y_z),
            textcoords="offset points",
            xytext=(5, 10),
            ha="center",
            rotation=90,
            fontsize=9,
            color="darkblue",
        )

    ax_z.set_title("Liniendiagramm der Abweichungen: Y_diff")
    ax_z.set_xlabel("Kategorie" if category_col else "Index")
    ax_z.set_ylabel("Abweichung")
    ax_z.tick_params(axis='x', rotation=45)
    ax_z.legend()

    st.pyplot(fig_z)
    
    
    
else:
    st.info("Bitte lade eine CSV-Datei hoch, um die Diagramme zu sehen.")






