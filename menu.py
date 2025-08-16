import sys
import time
import os
from classes import Ebook

SENHA_ADMIN = "admin123"

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

#------------------------------- MENU PRINCIPAL ------------------------------------------
def menu_principal(biblioteca):
    while True:
        time.sleep(2)
        limpar_tela()
        print("---- Sistema de gerenciamento da biblioteca ----")
        print("1. Entrar como administrador")
        print("2. Entrar como membro")
        print("3. Cadastrar novo membro")
        print("4. Sair do sistema")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            senha = input("Digite a senha de administrador: ")
            if senha == SENHA_ADMIN:
                print("\n✔ Login de administrador bem-sucedido!")
                time.sleep(1)
                menu_administrador(biblioteca)
            else:
                print("❗️ Senha incorreta.")
                time.sleep(1.5)
                
        elif escolha == '2':
            email = input("Digite seu e-mail para login: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if membro:
                print(f"\n✔ Login bem-sucedido! Bem-vindo(a), {membro.nome}.")
                time.sleep(1)
                menu_membro(biblioteca, membro)
            else:
                print("❗️ Membro não encontrado com este e-mail.")
                time.sleep(1.5)
                
        elif escolha == '3':
            menu_cadastrar_membro(biblioteca)
        elif escolha == '4':
            print("Saindo do sistema...")
            time.sleep(1)
            print("Até logo!")
            sys.exit(0)
        else:
            print("❗️ Opção inválida.")
            time.sleep(1.5)
            
#------------------------------------------------- MENU e SUBMENU ADMINISTRADOR --------------------------------------------------
def menu_administrador(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 👑 Menu do administrador ---")
        print(f"Data atual do sistema: {biblioteca.get_data_atual().strftime('%d/%m/%Y')}")
        print("1. Gerenciar acervo")
        print("2. Gerenciar membros")
        print("3. Gerenciar eventos")
        print("4. Avançar o tempo no sistema")
        print("5. Ver relatório de uso")
        print("6. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_itens(biblioteca)
        elif escolha == '2':
            menu_gerenciar_membros(biblioteca)
        elif escolha == '3':
            menu_gerenciar_eventos(biblioteca)
                 
        elif escolha == '4':
            try:
                dias = int(input("Quantos dias você deseja avançar no tempo? "))
                mensagens = biblioteca.avancar_no_tempo(dias)
                for msg in mensagens:
                    print(msg)
                    time.sleep(0.5)
                input("\nPressione ENTER para continuar...")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                time.sleep(1.5)
                
        elif escolha == '5':
            relatorio = biblioteca.relatorio_uso()
            exibir_relatorio(relatorio)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            print("Fazendo logout de administrador...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)


            
def menu_gerenciar_itens(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 📦 Gerenciamento de acervo (Admin) ---")
        print("1. Gerenciar catálogo de livros/revistas")
        print("2. Gerenciar circulação")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_catalogo(biblioteca)
        elif escolha == '2':
            menu_gerenciar_circulacao(biblioteca)
        elif escolha == '3':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_catalogo(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 📚 Gerenciamento de catálogo ---")
        print("1. Cadastrar novo livro")
        print("2. Cadastrar nova revista")
        print("3. Listar todos os itens")
        print("4. Buscar item")
        print("5. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha in ('1', '2'):
            tipo = "livro" if escolha == '1' else "revista"
            titulo = input("Título: ")
            autor = input("Autor/Editor: ")
            editora = input("Editora: ")
            genero = input("Gênero: ")
            try:
                total_exemplares = int(input("Total de exemplares: "))
                kwargs = {}
                if tipo == 'livro':
                    kwargs['isbn'] = input("ISBN (opcional): ")
                else:
                    kwargs['edicao'] = input("Edição (opcional): ")
                
                sucesso, msg, _ = biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, **kwargs)
                print(msg)
            except ValueError:
                print("❗️ Número de exemplares deve ser um número inteiro.")
            time.sleep(1.5)
            
        elif escolha == '3':
            print("\n--- 📚 Lista de itens no acervo ---")
            itens = biblioteca.item
            if not itens:
                print("Nenhum item cadastrado.")
            else:
                for item in itens:
                    print(item)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '4':
            criterio = input("Buscar por (titulo\\autor\editora\genero): ").lower().strip()
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                valor = input(f"Digite o {criterio} que deseja buscar: ")
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado com esse critério.")
                else:
                    print("\n--- Resultados da busca ---")
                    for item in resultados:
                        print(item)
                        print("-" * 25)
            else:
                print("Critério de busca inválido.")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_circulacao(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 🔄 Gerenciamento de circulação ---")
        print("1. Realizar empréstimo")
        print("2. Realizar devolução")
        print("3. Ver reservas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Email do membro: ")
            titulo = input("Título do item: ")
            sucesso, msg, _ = biblioteca.realizar_emprestimo(email, titulo)
            if not sucesso and msg == "ITEM_INDISPONIVEL":
                print(f"❗️ Item '{titulo}' não está disponível para empréstimo no momento.")
                opcao = input("Deseja reservar o item para retirada posterior? (sim/não): ").strip().lower()
                if opcao == 'sim':
                    sucesso_reserva, msg_reserva, _ = biblioteca.realizar_emprestimo(email, titulo, para_reserva=True)
                    print(msg_reserva)
                else:
                    print("Empréstimo não realizado.")
            else:
                print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            email = input("Email do membro: ")
            titulo = input("Título do item: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if not membro:
               print(f"❗️ Membro com email {email} não encontrado.")
            else:
               multas_pendentes = biblioteca.listar_multas_do_membro(membro)
               pagamento_ok = True
               if multas_pendentes:
                   print(f"\n❗️ O membro {membro.nome} possui multas pendentes. É necessário quitá-las para devolver o item.")
                   pagamento_ok = pagamento_multas(biblioteca, membro)
              
               if pagamento_ok:
                   sucesso, msg = biblioteca.realizar_devolucao(email, titulo)
                   print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            reservas = biblioteca.listar_reservas()
            if not reservas:
                print("Nenhuma reserva de livro ativa no momento.")
            else:
                print("\n--- Lista de reservas ativas ---")
                for reserva in reservas:
                    print(reserva)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_membros(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 👤 Gerenciamento de membros (Admin) ---")
        print("1. Cadastrar novo membro")
        print("2. Listar todos os membros")
        print("3. Ver todas as multas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_cadastrar_membro(biblioteca)
            
        elif escolha == '2':
            print("\n--- 👥 Lista de membros ---")
            membros = biblioteca.membros
            if not membros:
                print("Nenhum membro cadastrado.")
            else:
                for membro in membros:
                    print(membro)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            menu_gerenciar_multas(biblioteca)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
            
def menu_gerenciar_multas(biblioteca):
    print("\n--- 💰 Todas as multas do sistema ---")
    multas = biblioteca.multas
    if not multas:
        print("Nenhuma multa registrada no sistema.")
    else:
        for multa in multas:
            print(multa)
            print("-" * 25)
    input("\nPressione ENTER para continuar...")
            
def menu_gerenciar_eventos(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 🎉 Gerenciamento de eventos (Admin) ---")
        print("1. Agendar evento")
        print("2. Divulgar eventos")
        print("3. Cancelar evento")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            data = input("Data (DD/MM/AAAA): ")
            local = input("Local: ")
            sucesso, msg, _ = biblioteca.agendar_evento(nome, descricao, data, local)
            print(msg)
            time.sleep(1.5)
            
        elif escolha == '2':
            eventos_para_divulgar = biblioteca.divulgar_eventos()
            if not eventos_para_divulgar:
                print("Nenhum evento agendado para divulgar.")
            else:
                print(f"\nDivulgando {len(eventos_para_divulgar)} evento(s)...")
                print("-" * 40)
                for evento in eventos_para_divulgar:
                    print(evento)
                    print("-" * 20)
                    time.sleep(0.7)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            nome_evento = input("Digite o nome do evento a ser cancelado: ")
            sucesso, msg = biblioteca.cancelar_evento(nome_evento)
            print(msg)
            
            time.sleep(1.5)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
  
                        
#--------------------- ADMIN E PRINCIPAL --------------------------------------------
def menu_cadastrar_membro(biblioteca):
    limpar_tela()
    print("\n--- Cadastro de novo Membro ---")
    try:
        nome = input("Digite o nome do membro: ")
        endereco = input("Digite o endereço do membro: ")
        email = input("Digite o email do membro: ")
        sucesso, msg, _ = biblioteca.cadastrar_membro(nome, endereco, email)
        print(msg)

    except ValueError as e:
        print(f"\n❗️ Erro no cadastro: {e}")
        print("Por favor, tente novamente com os dados corretos.")

    finally:
        time.sleep(2.5)


#-------------------------------- MENU MEMBRO ------------------------------------------  
def menu_membro(biblioteca, membro):
    while True:
        limpar_tela()
        print(f"\n--- 🤗 Menu do membro: {membro.nome} ---")
        print("1. Buscar item no acervo")
        print("2. Meus empréstimos e devoluções")
        print("3. Minhas multas pendentes")
        print("4. Acessar eBook")
        print("5. Ver eventos")
        print("6. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            criterio = input("Buscar por (titulo\\autor\editora\genero): ").lower().strip()
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                valor = input(f"Digite o {criterio} que deseja buscar: ")
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado.")
                else:
                    print("\n--- Resultados da busca ---")
                    for item in resultados:
                        print(item)
                        print("-" * 25)
            else:
                print("Critério de busca inválido.")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            print("\n--- Meus empréstimos ativos ---")
            emprestimos_ativos = biblioteca.listar_emprestimos_do_membro(membro)
            if not emprestimos_ativos:
                print("Você não possui empréstimos ativos.")
            else:
                for emprestimo in emprestimos_ativos:
                    print(emprestimo)
                    print("-" * 25)
                
                devolver = input("\nDeseja devolver um item? (sim/não): ").lower()
                if devolver == 'sim':
                    titulo_item = input("Digite o título do item para devolver: ")
                    multas_pendentes = biblioteca.listar_multas_do_membro(membro)
                    pagamento_ok = True
                    if multas_pendentes:
                       print("\n❗️ Você possui multas pendentes. É necessário quitá-las para devolver o item.")
                       pagamento_ok = pagamento_multas(biblioteca, membro)
                       
                    if pagamento_ok:
                       sucesso, msg = biblioteca.realizar_devolucao(membro.email, titulo_item)
                       print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            print("\n--- Minhas multas pendentes ---")
            multas_pendentes = biblioteca.listar_multas_do_membro(membro)
            if not multas_pendentes:
                print("Nenhuma multa pendente.")
            else:
                for multa in multas_pendentes:
                    print(multa)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
                    
        elif escolha == '4':
            print("\n--- 📖 Ebooks cadastrados ---")
            ebooks = [i for i in biblioteca.item if isinstance(i, Ebook)]
            if not ebooks:
                print("Nenhum ebook cadastrado atualmente.\n")
            else:
                for ebook in ebooks:
                    print(ebook)
                    print("-" * 25)
                titulo = input("Digite o título do eBook que deseja acessar: ")
                ebook_encontrado = next(
                    (i for i in ebooks if biblioteca._normalizar(i.titulo) == biblioteca._normalizar(titulo)),
                    None
                )
                if ebook_encontrado:
                    print(f"Acesse o livro clicando aqui 👉 {ebook_encontrado.link_download}")
                else:
                    print("❗️ Ebook não encontrado.")
            input("\nPressione ENTER para continuar...")

        elif escolha == '5':
            eventos = biblioteca.listar_eventos()
            if not eventos:
                print("Nenhum evento agendado no momento.")
            else:
                print("\n--- 🗓️ Eventos agendados ---")
                for evento in eventos:
                    print(evento)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            print("Fazendo logout...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
            
def exibir_relatorio(relatorio):
    print("\n" + "=" * 30)
    print("📑 Relatório de uso da biblioteca")
    print("=" * 30 + "")
    
    if not relatorio:
        print("😩 Nenhuma atividade para gerar relatório")
        return

    print("\n--- Atividade dos itens ---\n")
    print("📖 Top 5 livros mais emprestados\n")
    if relatorio["top_livros"]:
        for livro, count in relatorio["top_livros"]:
            print(f" - {livro} ({count} vezes)")
    else:
        print("Nenhum livro emprestado ainda.")
        
    print("\n\n👀 Top 3 genêros mais populares\n")
    if relatorio["top_generos"]:
        for genero, count in relatorio["top_generos"]:
            print(f" - {genero} ({count} vezes)")
    else:
        print("Nenhum gênero popular ainda.")
    
    print("\n--- Atividade dos membros ---\n")
    print("🏆 Top 3 membros mais ativos:\n")
    if relatorio["membros_ativos"]:
        for membro, count in relatorio["membros_ativos"]:
            print(f"  - {membro} ({count} empréstimos)")
    else:
        print("Nenhum membro ativo ainda.")
            
    print("\n--- Análise de multas ---\n")
    print(f"  - 💰 Valor total de multas geradas: R$ {relatorio['total_multas_geradas']:.2f}")
    print(f"  - 🤑 Valor total de multas pagas: R$ {relatorio['total_multas_pagas']:.2f}")
    print(f"  - 🪙 Taxa de pagamento de multas: {relatorio['taxa_pagamento_multas']:.1f}%")

    print("\n\n--- Estatísticas Gerais ---")
    print(f"  - Número total de itens no acervo: {relatorio['total_livros_acervo']}")
    print(f"  - Número total de membros: {relatorio['total_membros']}")
    print(f"  - Total de empréstimos realizados (histórico): {relatorio['total_emprestimos_historico']}")
    print(f"  - Itens atualmente emprestados: {relatorio['emprestimos_atuais']}")

    print("\n" + "="*30)
    print("Relatório gerado com sucesso!")
    print("="*30)

def pagamento_multas(biblioteca, membro):
    """Exibe as multas pendentes e processa o pagamento."""
    multas_pendentes = biblioteca.listar_multas_do_membro(membro)
    
    print("\n--- 💰 Multas pendentes ---")
    total_a_pagar = 0
    for multa in multas_pendentes:
        print(multa)
        total_a_pagar += multa.valor
        print("-" * 25)
    print(f"Total a pagar: R$ {total_a_pagar:.2f}")

    pagar = input("\nDeseja pagar todas as multas agora? (sim/não): ").strip().lower()
    if pagar == 'sim':
        for m in multas_pendentes:
            m.pagar()
        print("\n✔ Multas pagas com sucesso.")
        time.sleep(1.5)
        return True
    else:
        print("\n❌ Pagamento não efetuado. A devolução não pode ser concluída.")
        time.sleep(1.5)
        return False