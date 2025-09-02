from datetime import datetime, timedelta
import unicodedata
from collections import Counter

from classes import Evento, Multa, Ebook, Reserva, Membro, Emprestimo, Livro, Revista

DIAS_EMPRESTIMO = 14
MAXIMO_EMPRESTIMO_MEMBRO = 3

#-------------------- CLASSES GERENCIADORAS ------------------------------
class GerenciadorAcervo:
    def __init__(self) -> None:
        self._item = []
    
    #Remove acentos e converte o texto para minúsculas para facilitar comparações.
    @staticmethod
    def normalizar(texto: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', texto)
                       if unicodedata.category(c) != 'Mn').lower()
    
    @property
    def itens(self) -> list:
        return list(self._item)

    def cadastrar_item(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int, tipo="livro", **kwargs) -> tuple:
        try:
            #Cria o objeto do item com base no tipo especificado.
            if tipo == "livro":
                novo_item = Livro(titulo, autor, editora, genero, total_exemplares, kwargs.get("isbn"))
            elif tipo == "revista":
                novo_item = Revista(titulo, autor, editora, genero, total_exemplares, kwargs.get("edicao"))
            elif tipo == "ebook":
                novo_item = Ebook(titulo, autor, editora, genero, total_exemplares, kwargs.get("formato"), kwargs.get("link_download"))
            else:
                return False, "Tipo inválido! Use 'livro', 'revista' ou 'ebook'.", None
            
            #Adiciona o novo item à lista do acervo.
            self._item.append(novo_item)
            return True, f"\n✔ {tipo.capitalize()} '{titulo}' cadastrado com sucesso.", novo_item
        except Exception as e:
            return False, f"Ocorreu um erro ao cadastrar o item: {e}", None

    def buscar_item(self, criterio: str, valor_busca: str) -> list:
        resultados = []
        valor_busca_lower = GerenciadorAcervo.normalizar(valor_busca)
        #Itera sobre os itens e adiciona aos resultados se corresponderem ao critério.
        for item in self._item:
            if criterio == 'titulo' and valor_busca_lower in GerenciadorAcervo.normalizar(item.titulo):
                resultados.append(item)
            elif criterio == 'autor' and valor_busca_lower in GerenciadorAcervo.normalizar(item.autor):
                resultados.append(item)
            elif criterio == 'editora' and valor_busca_lower in GerenciadorAcervo.normalizar(item.editora):
                resultados.append(item)
            elif criterio == 'genero' and valor_busca_lower in GerenciadorAcervo.normalizar(item.genero):
                resultados.append(item) 
        return resultados
    
    def buscar_por_titulo_normalizado(self, titulo_normalizado: str) -> object | None:
        return next((i for i in self._item if GerenciadorAcervo.normalizar(i.titulo) == titulo_normalizado), None)


class GerenciadorMembros:
    def __init__(self) -> None:
        self._membros = []

    @property
    def membros(self) -> list:
        return list(self._membros)

    def cadastrar_membro(self, nome: str, endereco: str, email: str) -> tuple:
        #Verifica se o e-mail já está cadastrado para evitar duplicatas.
        if any(m.email == email for m in self._membros):
            return False, f"\n❗️ Membro com email '{email}' já cadastrado.", None
        
        #Cria um novo objeto Membro e o adiciona à lista.
        novo_membro = Membro(nome, endereco, email)
        self._membros.append(novo_membro)
        return True, f"\n✔ Membro '{nome}' cadastrado com sucesso!", novo_membro
    
    def buscar_membro_por_email(self, email) -> Membro | None:
        return next((membro for membro in self._membros if membro.email == email), None)


class GerenciadorEventos:
    def __init__(self) -> None:
        self._eventos = []

    @property
    def eventos(self) -> list:
        return list(self._eventos)

    def agendar_evento(self, nome: str, descricao: str, data: str, local: str) -> tuple:
        try:
            novo_evento = Evento(nome, descricao, data, local)
            self._eventos.append(novo_evento)
            return True, f"✔ Evento '{nome}' agendado com sucesso.", novo_evento
        except Exception as e:
            return False, f"Ocorreu um erro ao agendar o evento: {e}", None
    
    def cancelar_evento(self, nome_evento: str) -> tuple:
        nome_normalizado = GerenciadorAcervo.normalizar(nome_evento)
        evento = next((e for e in self._eventos if GerenciadorAcervo.normalizar(e.nome) == nome_normalizado), None)
        
        if evento:
            self._eventos.remove(evento)
            return True, f"✔ Evento '{evento.nome}' cancelado com sucesso."
        return False, f"❗️ Evento '{nome_evento}' não encontrado."


class GerenciadorOperacoes:
    def __init__(self, gerenciador_acervo: GerenciadorAcervo, gerenciador_membros: GerenciadorMembros) -> None:
        self._emprestimos = []
        self._reservas = []
        self._multas = []
        self._historico_emprestimo = []
        
        #Injeção de dependência dos outros gerenciadores
        self.acervo = gerenciador_acervo
        self.membros = gerenciador_membros

    @property
    def emprestimos(self) -> list: 
        return list(self._emprestimos)
    
    @property
    def reservas(self) -> list: 
        return list(self._reservas)
    @property
    def multas(self) -> list: 
        return list(self._multas)
    
    @property
    def historico_emprestimo(self) -> list: 
        return list(self._historico_emprestimo)
    
    def listar_emprestimos_do_membro(self, membro: Membro) -> list:
        return [e for e in self._emprestimos if e.membro.email == membro.email]

    def listar_multas_do_membro(self, membro: Membro) -> list:
        return [m for m in self._multas if m.emprestimo_atrasado.membro.email == membro.email and not m.pago]

    def realizar_emprestimo(self, email: str, titulo: str, data_atual: datetime, para_reserva: bool = False) -> tuple:
        membro = self.membros.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado.", None

        #Verifica se o membro possui multas pendentes.
        if self.listar_multas_do_membro(membro):
            return False, f"❗️ {membro.nome} possui multas pendentes.", None
        
        #Localiza o item no acervo pelo título.
        titulo_normalizado = GerenciadorAcervo.normalizar(titulo)
        item = self.acervo.buscar_por_titulo_normalizado(titulo_normalizado)
        if not item:
            return False, f"❗️ Item '{titulo}' não cadastrado no acervo.", None

        #Verifica se o membro atingiu o limite de empréstimos.
        emprestimos_membro = self.listar_emprestimos_do_membro(membro)
        if len(emprestimos_membro) >= MAXIMO_EMPRESTIMO_MEMBRO:
            return False, f"❗️ {membro.nome} atingiu o limite de {MAXIMO_EMPRESTIMO_MEMBRO} empréstimos.", None
        
        #Impede que o membro pegue o mesmo título mais de uma vez.
        if any(GerenciadorAcervo.normalizar(e.livro.titulo) == titulo_normalizado for e in emprestimos_membro):
            return False, f"❗️ {membro.nome} já possui um exemplar de '{titulo}'.", None

        #Se o item não estiver disponível, cria uma reserva.
        if not item.verificar_disponibilidade():
            if para_reserva:
                reserva = Reserva(item, membro, data_atual)
                self._reservas.append(reserva)
                return True, f"✔ Reserva confirmada para {membro.nome} - Livro: {reserva.livro.titulo}", reserva
            return False, "ITEM_INDISPONIVEL", None
        
        #Se o item estiver disponível, realiza o empréstimo.
        if item.emprestar():
            data_devolucao = data_atual + timedelta(days=DIAS_EMPRESTIMO)
            emprestimo = Emprestimo(item, membro, data_atual, data_devolucao)
            self._emprestimos.append(emprestimo)
            self._historico_emprestimo.append(emprestimo)
            return True, f"\n✔ Empréstimo realizado com sucesso!\n{emprestimo}", emprestimo
        
        return False, "Ocorreu um erro desconhecido ao tentar emprestar.", None

    def realizar_devolucao(self, email: str, titulo: str, data_atual: datetime) -> tuple:
        membro = self.membros.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado."
        
        #Verifica se o membro tem multas para poder devolver.
        if self.listar_multas_do_membro(membro):
            return False, f"❗️ {membro.nome} possui multas pendentes."

        #Encontra o empréstimo a ser devolvido.
        titulo_normalizado = GerenciadorAcervo.normalizar(titulo)
        emprestimo = next((e for e in self._emprestimos if e.membro.email == email and GerenciadorAcervo.normalizar(e.livro.titulo) == titulo_normalizado), None)

        if not emprestimo:
            return False, f"❗️ Empréstimo de '{titulo}' para {membro.nome} não encontrado."
        
        #Atualiza a quantidade de exemplares disponíveis e remove o empréstimo da lista de ativos.    
        emprestimo.livro.devolver()
        self._emprestimos.remove(emprestimo)
        
        #Verifica se há reservas para o item devolvido e atende a primeira da fila.
        for reserva in self._reservas[:]:
            if GerenciadorAcervo.normalizar(reserva.livro.titulo) == titulo_normalizado:
                print(f"\n🔔 Notificação: O livro '{reserva.livro.titulo}' ficou disponível e foi emprestado para {reserva.membro.nome}.")
                self._reservas.remove(reserva)
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo, data_atual)
                break
        
        return True, f"✔ Devolução de '{titulo}' por {membro.nome} realizada com sucesso!"

    def verificar_atrasos(self, data_atual: datetime) -> list:
        mensagens = []
        atrasados = [e for e in self._emprestimos if e.data_devolucao_prevista < data_atual]

        if not atrasados:
            mensagens.append("✔ Nenhum empréstimo atrasado para gerar multas.")
            return mensagens

        mensagens.append("\n--- Verificação de atrasos e geração de multas ---")
        for emprestimo in atrasados:
            multa_existente = next((m for m in self._multas if m.emprestimo_atrasado == emprestimo), None)
            if not multa_existente:
                nova_multa = Multa(emprestimo, 0)
                nova_multa.atualizar_valor(data_atual)
                self._multas.append(nova_multa)
                mensagens.append(
                    f"🔴 Multa GERADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                    f"   - Valor: R$ {nova_multa.valor:.2f} ({nova_multa.dias_atraso} dias de atraso)."
                )           
            else:
                #Atualiza valor e dias de atraso
                multa_existente.atualizar_valor(data_atual)
                mensagens.append(
                    f"🟡 Multa ATUALIZADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                    f"   - Novo Valor: R$ {multa_existente.valor:.2f} ({multa_existente.dias_atraso} dias de atraso)."
                )        
        return mensagens


#------------------------ CLASSE DE CONTROLE ----------------------------
class Biblioteca:
    #delega as operações para os gerenciadores
    def __init__(self) -> None:
        self._data_atual_simulada = datetime.now()
        
        self.acervo = GerenciadorAcervo()
        self.membros = GerenciadorMembros()
        self.eventos = GerenciadorEventos()
        self.operacoes = GerenciadorOperacoes(self.acervo, self.membros)

    @property
    def data_atual(self):
        return self._data_atual_simulada

    def avancar_no_tempo(self, dias: int) -> list:
        if dias <= 0:
            return ["Por favor, insira um número de dias maior que zero."]
        
        self._data_atual_simulada += timedelta(days=dias)
        mensagens = ["\n" + "="*45]
        mensagens.append(f"⌛️  O tempo avançou {dias} dia(s).")
        mensagens.append(f"📅  A nova data do sistema é: {self.data_atual.strftime('%d/%m/%Y')}")
        mensagens.append("="*45 + "\n")
        
        mensagens.extend(self.operacoes.verificar_atrasos(self.data_atual))
        return mensagens

    # --- MÉTODOS DELEGADOS AOS GERENCIADORES ---
    def normalizar(self, texto: str):
        return self.acervo.normalizar(texto)
    def cadastrar_item(self, *args, **kwargs) -> tuple:
        return self.acervo.cadastrar_item(*args, **kwargs)

    def buscar_item(self, *args, **kwargs) -> list:
        return self.acervo.buscar_item(*args, **kwargs)

    def listar_itens(self) -> list:
        return self.acervo.itens

    def cadastrar_membro(self, *args, **kwargs) -> tuple:
        return self.membros.cadastrar_membro(*args, **kwargs)

    def buscar_membro_por_email(self, email: str) -> Membro | None:
        return self.membros.buscar_membro_por_email(email)

    def listar_membros(self) -> list:
        return self.membros.membros

    def realizar_emprestimo(self, email: str, titulo: str, para_reserva: bool = False) -> tuple:
        return self.operacoes.realizar_emprestimo(email, titulo, self.data_atual, para_reserva)

    def realizar_devolucao(self, email: str, titulo: str) -> tuple:
        return self.operacoes.realizar_devolucao(email, titulo, self.data_atual)

    def agendar_evento(self, *args, **kwargs) -> tuple:
        return self.eventos.agendar_evento(*args, **kwargs)

    def cancelar_evento(self, *args, **kwargs) -> tuple:
        return self.eventos.cancelar_evento(*args, **kwargs)

    def listar_eventos(self) -> list:
        return self.eventos.eventos
    def divulgar_eventos(self) -> list:
        #Retorna os próximos 5 eventos agendados para divulgação.
        return self.eventos.eventos[:5]

    def listar_reservas(self) -> list:
        return self.operacoes.reservas
    
    def listar_multas(self) -> list:
        return self.operacoes.multas
    
    def listar_emprestimos_do_membro(self, membro: Membro) -> list:
        return self.operacoes.listar_emprestimos_do_membro(membro)

    def listar_multas_do_membro(self, membro: Membro) -> list:
        return self.operacoes.listar_multas_do_membro(membro)
    
    #----------------- RELATÓRIOS E ESTATÍSTICAS -----------------
    def relatorio_uso(self) -> dict | None:
        #Gera um relatório com estatísticas de uso da biblioteca.
        historico = self.operacoes.historico_emprestimo
        if not historico:
            return None
        
        contagem_livro = Counter(e.livro.titulo for e in historico).most_common(5)  #Calcula os livros mais emprestados.
        contagem_genero = Counter(e.livro.genero for e in historico).most_common(3) #Calcula os gêneros mais populares.
        contagem_membros = Counter(e.membro.nome for e in historico).most_common(3) #Identifica os membros mais ativos.
        
        #Analisa os dados de multas.
        multas_geradas = self.operacoes.multas
        total_geradas = sum(m.valor for m in multas_geradas)
        total_pagas = sum(m.valor for m in multas_geradas if m.pago)
        taxa_pagamento = (total_pagas / total_geradas * 100) if total_geradas > 0 else 0
        
        #Compila todas as informações em um dicionário.
        return {
            "top_livros": contagem_livro,
            "top_generos": contagem_genero,
            "membros_ativos": contagem_membros,
            "total_multas_geradas": total_geradas,
            "total_multas_pagas": total_pagas,
            "taxa_pagamento_multas": taxa_pagamento,
            "total_livros_acervo": len(self.acervo.itens),
            "total_membros": len(self.membros.membros),
            "total_emprestimos_historico": len(historico),
            "emprestimos_atuais": len(self.operacoes.emprestimos),
        }