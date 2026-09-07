import mysql.connector


def conectar():
    banco = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aluno",
        database="delivery"
    )

    return banco