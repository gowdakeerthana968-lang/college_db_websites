from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Replace with the EXACT SAME Aiven Service URI (with revealed password)
DATABASE_URL = "PASTE_YOUR_AIVEN_SERVICE_URI_HERE"

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute(
            """INSERT INTO student (usn, name, branch, age, ph_no, email, semester, section, dept_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                request.form["usn"],
                request.form["name"],
                request.form["branch"],
                request.form["age"],
                request.form["ph_no"],
                request.form["email"],
                request.form["semester"],
                request.form["section"],
                request.form["dept_id"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM student ORDER BY usn;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)