from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'Esto-es-una-clave-secreta-david'

db_path = os.path.join(os.path.dirname(__file__), 'notes.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)

@app.route("/create", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if not title or not content:
            flash("❌ Todos los campos son obligatorios.")
            return render_template("note_form.html")
        
        #Guardar en una base de datos
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()

        flash("✅ Nota enviada correctamente")
        return redirect(url_for("home"))
    
    return render_template("note_form.html")

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    note =Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("🚮 Nota eliminada con éxito")
    return redirect(url_for("home"))

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("❌ Todos los campos son obligatorios.")
            return render_template("note_form.html", note=note)
        
        note.title = title
        note.content = content
        db.session.commit()
        flash("✅ Nota actualizada correctamente.")
        return redirect(url_for("home"))
    
    return render_template("note_form.html", note=note)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"
    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)