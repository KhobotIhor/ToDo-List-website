from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SECRET_KEY'] = 'SECRET KEY'


db = SQLAlchemy(model_class=Base)

db.init_app(app)


class ActionForm(FlaskForm):
    action = StringField('Enter the action', validators=[validators.DataRequired()])
    submit = SubmitField('Add')


class Action(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    action: Mapped[str] = mapped_column(db.String(250), nullable=False)


# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ActionForm()
    if request.method == 'GET':
        result = db.session.execute(db.select(Action).order_by(Action.id))
        all_actions = result.scalars()
        return render_template('index.html', form=form, actions=all_actions)
    if form.validate_on_submit():
        new_action = Action(
            action=request.form.get('action')
        )
        db.session.add(new_action)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete/<int:action_id>')
def delete(action_id):
    action = db.get_or_404(Action, action_id)
    if action:
        db.session.delete(action)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
