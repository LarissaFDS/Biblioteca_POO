# 📚 Biblioteca_POO  

Um sistema de **gerenciamento de biblioteca** desenvolvido em Python, aplicando conceitos de **Programação Orientada a Objetos (POO)** como encapsulamento, herança, polimorfismo e abstração.  

---

## 🚀 Funcionalidades

### English
- 🔎 **Catalog Search**: Search library catalog by title, author, publisher, or genre.  
- 📖 **Borrow and Return**: Users can borrow and return items.  
- 📌 **Reservation System**: Reserve items currently on loan.  
- ⏰ **Overdue Notifications**: Automated late item alerts.  
- 👤 **Member Management**: Register and manage library members.  
- 💰 **Fine System**: Calculate and pay overdue fines.  
- 📦 **Inventory Management**: Track and manage library collection.  
- 🎉 **Event Management**: Schedule and promote library events.  
- 💻 **E-books Support**: Access to digital resources and e-books.  
- 📊 **Reports & Analytics**: Generate usage statistics and trends.  

### Português
- 🔎 **Busca no Catálogo**: Pesquisa por título, autor, editora ou gênero.  
- 📖 **Empréstimo e Devolução**: Retirada e devolução de itens.  
- 📌 **Sistema de Reserva**: Reserva de livros já emprestados.  
- ⏰ **Notificações de Atraso**: Alertas automáticos de atraso.  
- 👤 **Gerenciamento de Membros**: Cadastro e administração de usuários.  
- 💰 **Multas**: Cálculo e pagamento de multas por atraso.  
- 📦 **Gerenciamento de Acervo**: Controle do inventário.  
- 🎉 **Eventos**: Agendamento e divulgação de eventos da biblioteca.  
- 💻 **E-books**: Acesso a recursos digitais.  
- 📊 **Relatórios e Análises**: Estatísticas de uso da biblioteca.  

---

## ⚙️ Como Executar

1. Clone este repositório:  
   ```bash
   git clone https://github.com/SEU_USUARIO/Biblioteca_POO.git
   cd Biblioteca_POO
   ```
2. (Opcional) Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
    ```
3. Execute o programa principal:
    ```bash
    python main.py
    ```
### Acesso de administrador
* Use o menu interativo para navegar no sistema.
* Para acessar as funcionalidades administrativas, utilize a senha: `admin123`

## **🏗️ Estrutura das Classes**
* **🔹 Item (Classe Abstrata)**
    Classe base para todos os itens do acervo. Define atributos comuns e métodos obrigatórios (__str__, info_basica).

    * **Subclasses:**

        * 📖 Livro → atributo extra: ISBN.
        * 📰 Revista → atributo extra: edição.
        * 💻 Ebook → atributos extras: formato e link de download.
           * Sobrescreve métodos para refletir disponibilidade digital.

* **🔹 Membro**
    Representa um usuário da biblioteca.
    Validação de email (@email.com).

* **🔹 Emprestimo**
    Relação entre item emprestado e membro.

* **🔹 Evento**
    Representa eventos organizados pela biblioteca.

* **🔹 Reserva**
    Gerencia reservas de itens com status: pendente, confirmada, cancelada.

* **🔹 Multa**
    Controla multas por atraso, com métodos para cálculo e pagamento.

## 📂 Organização do Projeto
    ```bash
    Biblioteca_POO/
    ├── main.py          # Ponto de entrada do sistema
    ├── menu.py          # Menus interativos
    ├── biblioteca.py    # Classe principal Biblioteca + gerenciadores
    ├── classes.py       # Classes de domínio (Item, Livro, Membro, etc.)
    ├── acervo_padrao.py # Dados de exemplo
    └── README.md
    ```
## 🖥️ Demonstração de uso

**Menu principal:**

---- Sistema de gerenciamento da biblioteca ----

1. Entrar como administrador  
2. Entrar como membro  
3. Cadastrar novo membro  
4. Sair do sistema  
Escolha uma opção:

**Menu do administrador:**

--- 👑 Menu do administrador ---  
Data atual do sistema: 06/08/2025

1. Gerenciar acervo  
2. Gerenciar membros  
3. Gerenciar eventos  
4. Avançar o tempo no sistema  
5. Gerar relatório de uso  
6. Logout  
Escolha uma opção:

--- 🤗 Menu do membro: Fulano Silva ---
Data atual do sistema: 01/09/2025
1. Buscar item no acervo
2. Meus empréstimos e devoluções
3. Minhas multas pendentes
4. Acessar eBook
5. Ver eventos
6. Logout
Escolha uma opção: 

## 📜 Licença
    Este projeto é de uso educacional e pode ser adaptado livremente.
---