from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbimpacta:impacta#2020@dbimpacta.postgresql.dbaas.com.br:5432/dbimpacta"

db = SQLAlchemy(app)


class gabriel7812634876(db.Model):
    ra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    rua = db.Column(db.String(50), unique=True)
    numero = db.Column(db.String(5), unique=True)
    cep = db.Column(db.String(10), unique=True)
    complemento = db.Column(db.String(20), unique=True)

    def __init__(self, nome, email, rua, numero, cep, complemento):
        self.nome = nome
        self.email = email
        self.rua = rua
        self.numero = numero
        self.cep = cep
        self.complemento = complemento


@app.route("/")
def index():
    alunos = gabriel7812634876.query.all()
    return render_template("index.html", alunos=alunos)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        aluno = gabriel7812634876(
            request.form['nome'],
            request.form['email'],
            request.form['rua'],
            request.form['numero'],
            request.form['cep'],
            request.form['complemento'],
        )
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<int:ra>")
def delete(ra):
    aluno = gabriel7812634876.query.get(ra)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/edit/<int:ra>", methods=['GET', 'POST'])
def edit(ra):
    aluno = gabriel7812634876.query.get(ra)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.rua = request.form['rua']
        aluno.numero = request.form['numero']
        aluno.cep = request.form['cep']
        aluno.complemento = request.form['complemento']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', aluno=aluno)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
