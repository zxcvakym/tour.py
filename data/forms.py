from flask_wtf import FlaskForm
import wtforms


class SignUpForm(FlaskForm):
    username = wtforms.StringField("Введіть логін", validators=[wtforms.validators.DataRequired()])
    email = wtforms.EmailField("Введіть свою електронну пошту", validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.DataRequired(), wtforms.validators.length(8)])
    submit = wtforms.SubmitField("Зареєструватись")


class LoginForm(FlaskForm):
    username = wtforms.StringField("Введіть логін або електронну адресу", validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField("Увійти")