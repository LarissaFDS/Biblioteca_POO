# Biblioteca_POO

## Library Management System
* Catalog Search: Users can search the library catalog by title, author, genre, etc;
* Borrow and Return: Users can check out and return books;
* Reservation System: Users can reserve books that are currently on loan;
* Overdue Notifications: Automated notifications for overdue items;
* Member Management: Registration and management of library members;
* Fine Calculation and Payment: Calculation and payment of overdue fines;
* Inventory Management: Tracking and management of library inventory;
* Event Management: Scheduling and promoting library events;
* E-books and Online Resources: Access to digital resources and e-books;
* Reporting and Analytics: Generating reports on library usage and trends.
                         
                        Português

* Busca no Catálogo: Os usuários podem pesquisar o catálogo da biblioteca por título, autor, gênero, etc.    
* Empréstimo e Devolução: Os usuários podem retirar e devolver livros.                                       
* Sistema de Reserva: Os usuários podem reservar livros que estão atualmente emprestados.                    
* Notificações de Atraso: Notificações automáticas para itens em atraso.                                  
* Gerenciamento de Membros: Cadastro e gerenciamento dos membros da biblioteca.                             
* Cálculo e Pagamento de Multas: Cálculo e pagamento de multas por atraso.                                  
* Gerenciamento de Acervo: Acompanhamento e gerenciamento do acervo da biblioteca.                         
* Gerenciamento de Eventos: Agendamento e divulgação de eventos da biblioteca.                               
* E-books e Recursos Online: Acesso a recursos digitais e e-books.
* Relatórios e Análises: Geração de relatórios sobre o uso e as tendências da biblioteca.


# Classes
## Item (Classe Abstrata)
    Classe base para todos os itens do acervo da biblioteca.

* **Atributos:**
    * **titulo:** Título do item.
    * **autor:** Autor do item.
    * **editora:** Editora responsável pela publicação.
    * **genero:** Gênero do item.
    * **total_exemplares:** Quantidade total de cópias do item.
    * **exemplares_disponiveis:** Quantidade de cópias atualmente disponíveis para empréstimo.

* **Métodos:**
    * **verificar_disponibilidade():** Retorna True se houver exemplares disponíveis.
    * **emprestar():** Decrementa o número de exemplares disponíveis se o item estiver disponível.
    * **devolver():** Incrementa o número de exemplares disponíveis.

### Subclasses de Item
    Livro: Herda de Item.
* **Atributos Adicionais:**
    * **isbn:** Código ISBN do livro (opcional).

    Revista: Herda de Item.
* **Atributos Adicionais:**
    * **edicao:** Número ou nome da edição da revista (opcional).

    Ebook: Herda de Item.
* **Atributos Adicionais:**
    * **formato:** Formato do arquivo digital (ex: PDF, EPUB).
    * **link_download:** Link para acessar o e-book.

Observação: Métodos como emprestar() e verificar_disponibilidade() são sobrescritos para refletir a natureza digital do item (sempre disponível).

## Membro
    Representa um usuário da biblioteca.

* **Atributos:**
    * **nome:** Nome completo do membro.
    * **endereco:** Endereço do membro.
    * **email:** E-mail de contato do membro (deve terminar com @email.com).

## Emprestimo
    Registra o empréstimo de um item para um membro.

* **Atributos:**
    * **livro:** O item que foi emprestado.
    * **membro:** O membro que realizou o empréstimo.
    * **data_emprestimo:** Data em que o empréstimo foi realizado.
    * **data_devolucao_prevista:** Data limite para a devolução do item.

## Evento
    Representa um evento organizado pela biblioteca.

* **Atributos:**
    * **nome:** Nome do evento.
    * **descricao:** Breve descrição sobre o evento.
    * **data:** Data do evento (formato dd/mm/yyyy).
    * **local:** Local onde o evento ocorrerá.

## Reserva
    Gerencia a reserva de um item por um membro.

* **Atributos:**
    * **livro:** O item que foi reservado.
    * **membro:** O membro que realizou a reserva.
    * **data_reserva:** Data em que a reserva foi feita.
    * **status:** Situação da reserva ("pendente", "confirmada", "cancelada").

* **Métodos:**
    * **confirmar_reserva():** Altera o status da reserva para "confirmada".
    * **cancelar_reserva():** Altera o status da reserva para "cancelada".

## Multa
    Controla as multas geradas por empréstimos atrasados.

* **Atributos:**
    * **emprestimo_atrasado:** O objeto Emprestimo que originou a multa.
    * **valor:** O valor monetário da multa.
    * **pago:** Status booleano que indica se a multa foi paga.

* **Métodos:**
    * **pagar():** Marca a multa como paga.