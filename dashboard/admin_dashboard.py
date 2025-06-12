from flask import Flask, render_template, request, send_file
import pyodbc
import pandas as pd
from fpdf import FPDF
import io
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_connection():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"UID={os.getenv('SQL_USERNAME')};"
        f"PWD={os.getenv('SQL_PASSWORD')}"
    )

def get_filtered_dataframe(conn, search):
    query = "SELECT * FROM Benutzerdaten"
    if search:
        like_clause = " OR ".join([
            "Vorname LIKE ?",
            "Nachname LIKE ?",
            "Geburtsdatum LIKE ?",
            "Straße LIKE ?",
            "PLZ LIKE ?",
            "Ort LIKE ?",
            "Land LIKE ?",
            "Email LIKE ?",
            "Telefonnummer LIKE ?"
        ])
        query += f" WHERE {like_clause}"
        params = [f"%{search}%"] * 9
        return pd.read_sql(query, conn, params=params)
    else:
        return pd.read_sql(query, conn)

@app.route("/")
def index():
    search = request.args.get("search", "")
    conn = get_connection()
    df = get_filtered_dataframe(conn, search)
    return render_template("dashboard.html", data=df.to_dict(orient="records"))

@app.route("/export/<format>")
def export(format):
    search = request.args.get("search", "")
    conn = get_connection()
    df = get_filtered_dataframe(conn, search)

    if format == "csv":
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="users.csv")

    elif format == "json":
        output = df.to_json(orient="records", force_ascii=False)
        return send_file(io.BytesIO(output.encode()), mimetype="application/json", as_attachment=True, download_name="users.json")

@app.route("/stats/pdf")
def stats_pdf():
    search = request.args.get("search", "")
    conn = get_connection()
    df = get_filtered_dataframe(conn, search)
    stats = df["Land"].value_counts()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Nutzerstatistik nach Land", ln=True)

    for land, count in stats.items():
        pdf.cell(200, 10, f"{land}: {count}", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="statistik.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
