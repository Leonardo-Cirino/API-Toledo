from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Cliente(BaseModel):
    nome: str
    data_chegada: Optional[str] = None
    atendido: Optional[bool] = None
    tipo_atendimento: str
    posicao: Optional[int] = None

fila = []

@app.get("/")
def pag_inicial():
    return "API Totem fila de atendimento"

@app.get("/fila")
def fila_espera():
    return [cliente for cliente in fila if not cliente.atendido]

@app.get("/fila/completa")
def fila_completa():
    return fila

@app.get("/fila/{id}")
def cliente_ID(id: int):
    try:
        return fila[id-1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

@app.post("/fila")
def adiciona_cliente(cliente: Cliente):
    if len(cliente.nome) > 20:
        raise HTTPException(status_code=400, detail="Nome deve ter no máximo 20 caracteres")
    if cliente.tipo_atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="Tipo de atendimento inválido")
    cliente.data_chegada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cliente.atendido = False
    cliente.posicao = len(fila) + 1
    fila.append(cliente)
    return {"mensagem": "Cliente adicionado à fila"}

@app.put("/fila")
def atualizar_fila():
    for i, cliente in enumerate(fila):
        if cliente.atendido:
            continue
        if i == 0:
            cliente.atendido = True
        else:
            cliente.posicao -= 1
    return {"mensagem": "Fila atualizada"}

@app.delete("/fila/{id}")
def remover_cliente(id: int):
    try:
        del fila[id-1]
        for i, cliente in enumerate(fila):
            cliente.posicao = i+1
        return {"mensagem": "Cliente removido da fila"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")