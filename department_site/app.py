from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Replace with your full Aiven Service URI (with revealed password)
DATABASE_URL = "PASTE_YOUR_AIVEN_SERVICE_URI_HERE"

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO department (dept_id, dept_name, hod, hod_email) VALUES (%s, %s, %s, %s)",
            (
                request.form["dept_id"],
                request.form["dept_name"],
                request.form["hod"],
                request.form["hod_email"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM department ORDER BY dept_id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)