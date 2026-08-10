from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError

from app.models import Usuario

CATEGORIAS = [
    ("vinilo", "Vinilo"),
    ("cd", "CD"),
    ("merch", "Merch"),
    ("amplificador", "Amplificador"),
    ("cable", "Cable"),
    ("speaker", "Speaker"),
    ("receiver", "Receiver"),
    ("otro", "Otro"),
]


class RegistroForm(FlaskForm):
    nombre_usuario = StringField(
        "Nombre de usuario", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden.")],
    )
    submit = SubmitField("Crear cuenta")

    def validate_nombre_usuario(self, field):
        if Usuario.query.filter_by(nombre_usuario=field.data).first():
            raise ValidationError("Ese nombre de usuario ya está en uso.")

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError("Ese email ya está registrado.")


class LoginForm(FlaskForm):
    nombre_usuario = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    categoria = SelectField("Categoría", choices=CATEGORIAS, validators=[DataRequired()])
    descripcion = TextAreaField("Descripción")
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Guardar")
