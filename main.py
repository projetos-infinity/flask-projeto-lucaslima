from flask import Flask, render_template, redirect, request
import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import String, Integer


engine = sqlalchemy.create_engine('sqlite:///fake.db', echo = True)

Base = declarative_base()

class Treino(Base):
    __tablename__ = 'treinamento'
    id = Column(Integer, primary_key = True)
    exercicio = Column(String(100))
    equipamento = Column(String(100))
    series = Column(String(100))
    reps = Column(String(100))
    peso = Column(String(100))
Base.metadata.create_all(engine)

def criar_treino_sql(treino: Treino):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(treino)
    session.commit()

def apagar_treino_sql(id_):
    Session = sessionmaker(bind=engine)
    session = Session()
    treino_del = session.query(Treino).filter_by(id=id_).first()
    session.delete(treino_del)
    session.commit()

def buscar_treinos_sql():
    Session = sessionmaker(bind=engine)
    session = Session()
    treinos = session.query(Treino).all()
    return treinos


app = Flask(__name__)
@app.route('/')
def index():
    treinos = buscar_treinos_sql()
    return render_template('index.html', treinos=treinos)

@app.route('/newtraining')
def new_training():
    return render_template('newTraining.html')

@app.route('/criar_treino', methods=['POST'])
def criar_treino():
    print(request.form)
    treino = Treino(
    exercicio=request.form['exe-type'],
    equipamento=request.form['exe-equip'],
    series=request.form['v1'],
    reps=request.form['v2'],
    peso=request.form['v3']
    )
    criar_treino_sql(treino)
    return redirect('/')

@app.route('/delete_treino', methods=['POST'])
def delete_treino():
    apagar_treino_sql(request.form['id'])
    return redirect('/')

app.run(host='0.0.0.0', debug=True, port=81)
