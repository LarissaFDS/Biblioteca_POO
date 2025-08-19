import sys
from biblioteca import Biblioteca
from menu import menu_principal
from acervo_padrao import *

if __name__ == "__main__":
    biblioteca = Biblioteca()
    
    for tipo, titulo, autor, editora, genero, total_exemplares, extra1, extra2 in item_padrao:
        biblioteca.cadastrar_item(
            titulo, autor, editora, genero, total_exemplares,
            tipo=tipo, isbn=extra1, edicao=extra1, formato=extra1, link_download=extra2
        )

    for nome, descricao, data, local in eventos_padrao:
        biblioteca.agendar_evento(nome, descricao, data, local)
    
    for nome, endereco, email in membros_padrao:
        biblioteca.cadastrar_membro(nome, endereco, email)

    print("✔ Carga de dados concluída com sucesso!")
    print("\nBem-vindo ao sistema de biblioteca!")
    menu_principal(biblioteca)