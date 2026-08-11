from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app import db
from app.models import Producto
from app.forms import ProductoForm

productos_bp = Blueprint("productos", __name__)


def _obtener_producto_propio(producto_id):
    """Obtiene un producto y aborta con 403 si no pertenece al usuario en sesión."""
    producto = db.get_or_404(Producto, producto_id)
    if producto.usuario_id != current_user.id:
        abort(403)
    return producto


@productos_bp.route("/productos")
@login_required
def lista():
    productos = (
        Producto.query.filter_by(usuario_id=current_user.id)
        .order_by(Producto.fecha_creacion.desc())
        .all()
    )
    return render_template("productos/lista.html", productos=productos)


@productos_bp.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            usuario_id=current_user.id,
        )
        db.session.add(producto)
        db.session.commit()
        flash("Producto creado.", "success")
        return redirect(url_for("productos.lista"))

    return render_template("productos/formulario.html", form=form, titulo="Nuevo producto")


@productos_bp.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def editar(producto_id):
    producto = _obtener_producto_propio(producto_id)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        form.populate_obj(producto)
        db.session.commit()
        flash("Producto actualizado.", "success")
        return redirect(url_for("productos.lista"))

    return render_template("productos/formulario.html", form=form, titulo="Editar producto")


@productos_bp.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@login_required
def eliminar(producto_id):
    producto = _obtener_producto_propio(producto_id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado.", "success")
    return redirect(url_for("productos.lista"))
