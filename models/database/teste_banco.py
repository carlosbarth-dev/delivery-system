from database.conexao import conectar

banco = conectar()

if banco.is_connected():
    print("Conectado ao MySQL!")

banco.close()