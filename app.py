from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'Esto-es-una-clave-secreta-david'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        print(f"✅ Título: {title}, Contenido: {content}")
        return redirect(url_for("home"))
    return render_template("note_form.html")

if __name__ == '__main__':
    app.run(debug=True)