from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import Usuario
from app.forms import RegistroForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("productos.lista"))

    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(nombre_usuario=form.nombre_usuario.data, email=form.email.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash("Cuenta creada correctamente. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/registro.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("productos.lista"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nombre_usuario=form.nombre_usuario.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("productos.lista"))
        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("auth.login"))
