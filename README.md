# Biblioteca_POO

## Library Management System
• Catalog Search: Users can search the library catalog by title, author, genre, etc;
• Borrow and Return: Users can check out and return books;
• Reservation System: Users can reserve books that are currently on loan;
• Overdue Notifications: Automated notifications for overdue items;
• Member Management: Registration and management of library members;
• Fine Calculation and Payment: Calculation and payment of overdue fines;
• Inventory Management: Tracking and management of library inventory;
• Event Management: Scheduling and promoting library events;
• E-books and Online Resources: Access to digital resources and e-books;
• Reporting and Analytics: Generating reports on library usage and trends.
                         
                        Português

# -Busca no Catálogo: Os usuários podem pesquisar o catálogo da biblioteca por título, autor, gênero, etc.    
# -Empréstimo e Devolução: Os usuários podem retirar e devolver livros.                                       
# -Sistema de Reserva: Os usuários podem reservar livros que estão atualmente emprestados.                    
# -Notificações de Atraso: Notificações automáticas para itens em atraso.                                  
# -Gerenciamento de Membros: Cadastro e gerenciamento dos membros da biblioteca.                             
# -Cálculo e Pagamento de Multas: Cálculo e pagamento de multas por atraso.                                  
# -Gerenciamento de Acervo: Acompanhamento e gerenciamento do acervo da biblioteca.                         
# -Gerenciamento de Eventos: Agendamento e divulgação de eventos da biblioteca.                               
# -E-books e Recursos Online: Acesso a recursos digitais e e-books.
# -Relatórios e Análises: Geração de relatórios sobre o uso e as tendências da biblioteca.


## Classes
    # Item (para ser mais genérico e incluir revistas, etc.)
        Atributos: titulo, autor, genero, editora, nº de exemplares.
        Métodos: Verficar disponibilidade, cadastrar_item.

    # Membro
        Atributos: nome, endereco, contato(email).
        Métodos: cadastrar_membro
        
    # Emprestimo
        Atributos: livro, membro, data_emprestimo, data_devolucao_prevista.
        Métodos: emprestar(aux), realizar_emprestimo

    # Devolucao
        Atributos: Item, Membro, multa
        Métodos: devolver(aux), realizar_devolucao, notificar_atrasos

    # Evento
        Atributos: nome, descricao, data, local.
        Métodos: agendar_evento, cancelar_evento.

    # Reserva
        Atributos: livro, membro, dataReserva.
        Métodos: confirmar_reserva, cancelar_reserva.
    
    # Ebook
        Atributos: formato do arquivo, link para download.
        Métodos: baixar_livro, ler_artigo.


    Biblioteca
        Atributos: lista de livros, lista de membros, lista de emprestimos.
        Métodos:
            -buscar item
            -listar reserva

            -buscar membro (email)
            -listar emprestimo (membro)
            -listar multas (membro)
            
            -divulgar eventos
