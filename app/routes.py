from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Note, User
from app import db

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
def home():
    # notes = Note.query.all()
    if "user_id" not in session:
        flash("Debe iniciar sesión")
        return redirect(url_for("main.login"))
    notes = Note.query.filter_by(user_id=session["user_id"]).all()
    return render_template("home.html", notes=notes)

@main.route("/create", methods=["GET", "POST"])
@login_required
def create_note():
    if "user_id" not in session:
        flash("Debe iniciar sesión para crear notas")
        return redirect(url_for('main.login'))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("❌ Todos los campos son obligatorios.")
            return render_template("note_form.html")

        user_id = session["user_id"]
        note = Note(title=title, content=content, user_id=user_id)

        db.session.add(note)
        db.session.commit()

        flash("✅ Nota guardada")
        return redirect(url_for("main.home"))
    return render_template("note_form.html")

@main.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
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
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("🗑️ Nota eliminada con éxito")
    return redirect(url_for("main.home"))

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method== "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if not username or not email:
            flash("❌ Todos los campos son obligatorios")
            return render_template("register.html")
        
        if User.query.filter_by(username=username).first():
            flash("❌ El usuario ya eiste")
            return render_template("register.html")
        
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()

        flash("✅ Registro exitoso, se puede iniciar sesión")
        return redirect(url_for("main.login"))
    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username", "").strip()

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("❌ Usuario no encontrado")
            return render_template("login.html")
        
        session["user_id"] = user.id
        session["username"] = user.username
        flash(f"✅ Bienvenido, {user.username}")
        return redirect(url_for("main.home"))
    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión")
    return redirect(url_for("main.login"))

#Esto es solo para validar los usuarios es una test
# @main.before_app_request
# def create_sample_user():
#     if not User.query.filter_by(username="David").first():
#         user = User(username="David", email="david@example.com")
#         db.session.add(user)
#         db.session.commit()
