from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Note, User
from app import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)

@main.route("/create", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("❌ Todos los campos son obligatorios.")
            return render_template("note_form.html")

        user = User.query.filter_by(username="David").first()

        note = Note(title=title, content=content, user=user)
        db.session.add(note)
        db.session.commit()

        flash("✅ Nota guardada")
        return redirect(url_for("main.home"))
    return render_template("note_form.html")

@main.route("/edit/<int:note_id>", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))

    return render_template("note_form.html", note=note)

@main.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("🗑️ Nota eliminada con éxito")
    return redirect(url_for("main.home"))

@main.before_app_request
def create_sample_user():
    if not User.query.filter_by(username="David").first():
        user = User(username="David", email="david@example.com")
        db.session.add(user)
        db.session.commit()
