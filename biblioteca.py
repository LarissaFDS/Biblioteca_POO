from datetime import datetime, timedelta
import unicodedata
from collections import Counter

from classes import Evento, Multa, Ebook, Reserva, Membro, Emprestimo, Livro, Revista

DIAS_EMPRESTIMO = 14 
MAXIMO_EMPRESTIMO_MEMBRO = 3   
    
class Biblioteca:
    def __init__(self) -> None:
        self._item = [] 
        self._membros = [] 
        self._emprestimos = [] 
        self._reservas = []
        self._eventos = []
        self._multas = [] 
        self._data_atual_simulada = datetime.now() #Define a data atual do sistema, para simulações.
        self._historico_emprestimo = [] 
    
    @property    
    def item(self):
        return self._item

    #------------------------- MÉTODOS INTERNOS ------------------------------
    def _normalizar(self, texto: str) -> str:
        #Remove acentos e converte o texto para minúsculas para facilitar comparações.
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        ).lower()
        
    @property
    def data_atual(self):
        return self._data_atual_simulada

    def avancar_no_tempo(self, dias: int) -> list[str]:
        mensagens = []
        if dias <= 0:
            mensagens.append("Por favor, insira um número de dias maior que zero.")
            return mensagens
            
        #Atualiza a data do sistema.
        self._data_atual_simulada += timedelta(days=dias)
        mensagens.append("\n" + "="*45)
        mensagens.append(f"⌛️  O tempo avançou {dias} dia(s).")
        mensagens.append(f"📅  A nova data do sistema é: {self.data_atual.strftime('%d/%m/%Y')}")
        mensagens.append("="*45)
        mensagens.append("\nExecutando verificações automáticas para a nova data...")

        #Verifica automaticamente se há empréstimos atrasados após avançar no tempo.
        mensagens_atraso = self.verificar_atrasos()
        mensagens.extend(mensagens_atraso)
        return mensagens

    #------------------------------- ITEM ------------------------------------------------
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares, tipo="livro", **kwargs) -> tuple[bool, str, object]:
        try:
            #Cria o objeto do item com base no tipo especificado.
            if tipo == "livro":
                novo_item = Livro(titulo, autor, editora, genero, total_exemplares, kwargs.get("isbn"))
            elif tipo == "revista":
                novo_item = Revista(titulo, autor, editora, genero, total_exemplares, kwargs.get("edicao"))
            elif tipo == "ebook":
                novo_item = Ebook(titulo, autor, editora, genero, total_exemplares, 
                                kwargs.get("formato"), kwargs.get("link_download"))
            else:
                return False, "Tipo inválido! Use 'livro', 'revista' ou 'ebook'.", None
            
            #Adiciona o novo item à lista do acervo.
            self._item.append(novo_item)
            return True, f"\n✔ {tipo.capitalize()} '{titulo}' cadastrado com sucesso no acervo.", novo_item
        except Exception as e:
            return False, f"Ocorreu um erro ao cadastrar o item: {e}", None

    def buscar_item(self, criterio, valor_busca) -> list:
        resultados = []
        valor_busca_lower = self._normalizar(valor_busca)

        #Itera sobre os itens e adiciona aos resultados se corresponderem ao critério.
        for item in self._item:
            if criterio == 'titulo' and valor_busca_lower in self._normalizar(item.titulo):
                resultados.append(item)
            elif criterio == 'autor' and valor_busca_lower in self._normalizar(item.autor):
                resultados.append(item)
            elif criterio == 'editora' and valor_busca_lower in self._normalizar(item.editora):
                resultados.append(item)
            elif criterio == 'genero' and valor_busca_lower in self._normalizar(item.genero):
                resultados.append(item) 
        return resultados

    def listar_itens(self) -> list:
        #Retorna uma cópia da lista de todos os itens do acervo.
        return list(self._item)
    
    def listar_reservas(self) -> list:
        #Retorna uma cópia da lista de todas as reservas ativas.
        return list(self._reservas)

    #--------------------------------- MEMBRO -------------------------------------------------------
    def cadastrar_membro(self, nome, endereco, email) -> tuple[bool, str, Membro]:
        #Verifica se o e-mail já está cadastrado para evitar duplicatas.
        if any(m.email == email for m in self._membros):
            return False, f"\n❗️ Membro com email '{email}' já cadastrado.", None
        
        #Cria um novo objeto Membro e o adiciona à lista.
        novo_membro = Membro(nome, endereco, email)
        self._membros.append(novo_membro)
        return True, f"\n✔ Membro '{nome}' cadastrado com sucesso!", novo_membro
    
    def buscar_membro_por_email(self, email) -> Membro | None:
        for membro in self._membros:
            if membro.email == email:
                return membro
        return None
    
    def listar_membros(self) -> list:
       #Retorna uma cópia da lista de todos os membros cadastrados.
        return list(self._membros)
    
    def listar_emprestimos_do_membro(self, membro: Membro) -> list[Emprestimo]:
        #Retorna a lista de empréstimos ativos de um membro específico.
        return [e for e in self._emprestimos if e.membro.email == membro.email]

    def listar_multas_do_membro(self, membro: Membro) -> list[Multa]:
        #Retorna a lista de multas pendentes de um membro específico.
        return [m for m in self._multas if m.emprestimo_atrasado.membro.email == membro.email and not m.pago]
    
    #------------------------------ EMPRESTIMO e DEVOLUÇÃO ---------------------------------------
    def realizar_emprestimo(self, email: str, titulo: str, para_reserva: bool = False) -> tuple[bool, str, object]:
        membro = self.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado.", None

        #Verifica se o membro possui multas pendentes.
        multas_pendentes = self.listar_multas_do_membro(membro)
        if multas_pendentes:
            return False, f"❗️ {membro.nome} possui multas pendentes e não pode realizar novos empréstimos.", None
        
        #Localiza o item no acervo pelo título.
        titulo_normalizado = self._normalizar(titulo)
        item = next((i for i in self._item if self._normalizar(i.titulo) == titulo_normalizado), None)
        if not item:
            return False, f"❗️ Item '{titulo}' não cadastrado no acervo.", None

        #Verifica se o membro atingiu o limite de empréstimos.
        emprestimos_membro = self.listar_emprestimos_do_membro(membro)
        if len(emprestimos_membro) >= MAXIMO_EMPRESTIMO_MEMBRO:
            return False, f"❗️ {membro.nome} já atingiu o limite de {MAXIMO_EMPRESTIMO_MEMBRO} empréstimos ativos.", None
        
        #Impede que o membro pegue o mesmo título mais de uma vez.
        if any(self._normalizar(e.livro.titulo) == titulo_normalizado for e in emprestimos_membro):
            return False, f"❗️ {membro.nome} já possui um exemplar do item '{titulo}' emprestado.", None

        data_emprestimo = self.data_atual

        #Se o item não estiver disponível, cria uma reserva.
        if not item.verificar_disponibilidade():
            if para_reserva:
                reserva = Reserva(item, membro, data_emprestimo)
                self._reservas.append(reserva)
                return True, f"✔ Reserva confirmada para {membro.nome} - Livro: {reserva.livro.titulo}", reserva
            return False, "ITEM_INDISPONIVEL", None

        #Se o item estiver disponível, realiza o empréstimo.
        if item.emprestar():
            data_devolucao_prevista = data_emprestimo + timedelta(days=DIAS_EMPRESTIMO)
            emprestimo = Emprestimo(item, membro, data_emprestimo, data_devolucao_prevista)
            self._emprestimos.append(emprestimo)
            self._historico_emprestimo.append(emprestimo)
            msg = f"\n✔ Empréstimo realizado com sucesso!\n{emprestimo}"
            return True, msg, emprestimo
        
        return False, "Ocorreu um erro desconhecido ao tentar emprestar.", None


    def realizar_devolucao(self, email: str, titulo: str) -> tuple[bool, str]:
        membro = self.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado."
        
        #Verifica se o membro tem multas para poder devolver.
        multas_pendentes = self.listar_multas_do_membro(membro)
        if multas_pendentes:
            msg = f"❗️ {membro.nome} possui multas pendentes e não pode realizar a devolução."
            return False, msg, True 

        #Encontra o empréstimo a ser devolvido.
        titulo_normalizado = self._normalizar(titulo)
        emprestimo_a_devolver = next(
            (e for e in self._emprestimos if e.membro.email == email and self._normalizar(e.livro.titulo) == titulo_normalizado),
            None
        )

        if not emprestimo_a_devolver:
            return False, f"❗️ Empréstimo do item '{titulo}' para {membro.nome} não encontrado."
            
        #Atualiza a quantidade de exemplares disponíveis e remove o empréstimo da lista de ativos.
        emprestimo_a_devolver.livro.devolver()
        self._emprestimos.remove(emprestimo_a_devolver)
        
        #Verifica se há reservas para o item devolvido e atende a primeira da fila.
        for reserva in self._reservas[:]:
            if self._normalizar(reserva.livro.titulo) == titulo_normalizado:
                print(f"\n🔔 Notificação: O livro '{reserva.livro.titulo}' ficou disponível e foi emprestado para {reserva.membro.nome}, que estava na fila de reserva.\n")
                self._reservas.remove(reserva)
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo)
                break
        
        return True, f"✔ Devolução do item '{titulo}' por {membro.nome} realizada com sucesso!"
    
    def listar_multas(self) -> list:
        #Retorna uma cópia da lista de todas as multas geradas.
        return list(self._multas)


    #------------------------------ EVENTOS -----------------------------------------------    
    def agendar_evento(self, nome, descricao, data, local) -> tuple[bool, str, Evento]:
        try:
            novo_evento = Evento(nome, descricao, data, local)
            self._eventos.append(novo_evento)
            return True, f"✔ Evento '{nome}' agendado com sucesso.", novo_evento
        except Exception as e:
            return False, f"Ocorreu um erro ao agendar o evento: {e}", None
    
    def divulgar_eventos(self) -> list:
        #Retorna os próximos 5 eventos agendados para divulgação.
        return self._eventos[:5]
    
    def cancelar_evento(self, nome_evento: str) -> tuple[bool, str]:
        nome_evento_normalizado = self._normalizar(nome_evento)
        evento = next((e for e in self._eventos if self._normalizar(e.nome) == nome_evento_normalizado), None)
        
        if evento:
            self._eventos.remove(evento)
            return True, f"✔ Evento '{evento.nome}' cancelado com sucesso."
        else:
            return False, f"❗️ Evento '{nome_evento}' não encontrado."
    
    def listar_eventos(self) -> list:
        #Retorna uma cópia da lista dos próximos 5 eventos.
        return list(self._eventos[:5])
    
    #------------------------------- Verificar atrasos da biblioteca -------------------------------
    def verificar_atrasos(self) -> list[str]:
        mensagens = []
        hoje = self.data_atual
        #Filtra apenas os empréstimos cuja data de devolução prevista já passou.
        atrasados = [e for e in self._emprestimos if e.data_devolucao_prevista < hoje]

        if not atrasados:
            mensagens.append("✔ Nenhum empréstimo atrasado para gerar multas.")
            return mensagens

        mensagens.append("\n--- Verificação de atrasos e geração de multas ---")
        for emprestimo in atrasados:
            multa_existente = next((m for m in self._multas if m.emprestimo_atrasado == emprestimo), None)

            if not multa_existente:
                nova_multa = Multa(emprestimo, 0)
                nova_multa.atualizar_valor(hoje)
                self._multas.append(nova_multa)
                mensagens.append(
                    f"🔴 Multa GERADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                    f"   - Valor: R$ {nova_multa.valor:.2f} ({nova_multa.dias_atraso} dias de atraso)."
                )
            else:
                multa_existente.atualizar_valor(hoje) #Atualiza valor e dias de atraso
                mensagens.append(
                    f"🟡 Multa ATUALIZADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                    f"   - Novo Valor: R$ {multa_existente.valor:.2f} ({multa_existente.dias_atraso} dias de atraso)."
                )
        return mensagens


    #------------------------------- Relatório de uso ---------------------------------------------------
    def relatorio_uso(self) -> dict | None:
        """Gera um relatório com estatísticas de uso da biblioteca."""
        todos_emprestimos = self._historico_emprestimo
        if not todos_emprestimos:
            return None
        
        #Calcula os livros mais emprestados.
        titulos_emprestados = [e.livro.titulo for e in todos_emprestimos]
        contagem_livro = Counter(titulos_emprestados).most_common(5)
        
        #Calcula os gêneros mais populares.
        generos_emprestados = [e.livro.genero for e in todos_emprestimos]
        contagem_genero = Counter(generos_emprestados).most_common(3)
        
        #Identifica os membros mais ativos.
        membros_ativos = [e.membro.nome for e in todos_emprestimos]
        contagem_membros = Counter(membros_ativos).most_common(3)
            
        #Analisa os dados de multas.
        total_multas_geradas = sum(m.valor for m in self._multas)
        total_multas_pagas = sum(m.valor for m in self._multas if m.pago)
        taxa_pagamento = (total_multas_pagas / total_multas_geradas * 100) if total_multas_geradas > 0 else 0
        
        #Compila todas as informações em um dicionário.
        relatorio = {
            "top_livros": contagem_livro,
            "top_generos": contagem_genero,
            "membros_ativos": contagem_membros,
            "total_multas_geradas": total_multas_geradas,
            "total_multas_pagas": total_multas_pagas,
            "taxa_pagamento_multas": taxa_pagamento,
            "total_livros_acervo": len(self._item),
            "total_membros": len(self._membros),
            "total_emprestimos_historico": len(todos_emprestimos),
            "emprestimos_atuais": len(self._emprestimos),
        }
        return relatorio