from datetime import datetime, timedelta
import unicodedata
from collections import Counter

from classes import Evento, Multa, Ebook, Reserva, Membro, Emprestimo, Livro, Revista

DIAS_EMPRESTIMO = 14
MAXIMO_EMPRESTIMO_MEMBRO = 3
VALOR_MULTA = 0.5
    
class Biblioteca:
    def __init__(self) -> None:
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.reservas = []
        self.eventos = []
        self.multas = []
        self.ebook = []
        self.data_atual_simulada = datetime.now()
        self.historico_emprestimo = []

    # ------------------------- MÉTODOS INTERNOS ------------------------------
    def _normalizar(self, texto: str) -> str:
        """Remove acentos e coloca em minúsculas para facilitar comparações."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        ).lower()
        
    def get_data_atual(self):
        return self.data_atual_simulada

    def avancar_no_tempo(self, dias: int) -> list[str]:
        mensagens = []
        if dias <= 0:
            mensagens.append("Por favor, insira um número de dias maior que zero.")
            return mensagens
            
        self.data_atual_simulada += timedelta(days=dias)
        mensagens.append("\n" + "="*45)
        mensagens.append(f"⌛️  O tempo avançou {dias} dia(s).")
        mensagens.append(f"📅  A nova data do sistema é: {self.get_data_atual().strftime('%d/%m/%Y')}")
        mensagens.append("="*45)
        mensagens.append("\nExecutando verificações automáticas para a nova data...")

        mensagens_atraso = self.verificar_atrasos()
        mensagens.extend(mensagens_atraso)
        return mensagens

    #------------------------------- ITEM ------------------------------------------------
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares, tipo="livro", **kwargs) -> tuple[bool, str, object]:
        try:
            if tipo == "livro":
                novo_item = Livro(titulo, autor, editora, genero, total_exemplares, kwargs.get("isbn"))
            elif tipo == "revista":
                novo_item = Revista(titulo, autor, editora, genero, total_exemplares, kwargs.get("edicao"))
            elif tipo == "ebook":
                novo_item = Ebook(titulo, autor, editora, genero, total_exemplares, 
                                kwargs.get("formato"), kwargs.get("link_download"))
            else:
                return False, "Tipo inválido! Use 'livro', 'revista' ou 'ebook'.", None
            
            self.item.append(novo_item)
            return True, f"\n✔ {tipo.capitalize()} '{titulo}' cadastrado com sucesso no acervo.", novo_item
        except Exception as e:
            return False, f"Ocorreu um erro ao cadastrar o item: {e}", None

    
    def buscar_item(self, criterio, valor_busca) -> list:
        resultados = []
        valor_busca_lower = self._normalizar(valor_busca)

        for item in self.item:
            if criterio == 'titulo' and valor_busca_lower in self._normalizar(item.titulo):
                resultados.append(item)
            elif criterio == 'autor' and valor_busca_lower in self._normalizar(item.autor):
                resultados.append(item)
            elif criterio == 'editora' and valor_busca_lower in self._normalizar(item.editora):
                resultados.append(item)
            elif criterio == 'genero' and valor_busca_lower in self._normalizar(item.genero):
                resultados.append(item) 
        return resultados
    
    def listar_reservas(self) -> list:
        return self.reservas

    #--------------------------------- MEMBRO -------------------------------------------------------
    def cadastrar_membro(self, nome, endereco, email) -> tuple[bool, str, Membro]:
        if any(m.email == email for m in self.membros):
            return False, f"\n❗️ Membro com email '{email}' já cadastrado.", None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)
        return True, f"\n✔ Membro '{nome}' cadastrado com sucesso!", novo_membro
    
    def buscar_membro_por_email(self, email) -> Membro | None:
        for membro in self.membros:
            if membro.email == email:
                return membro
        return None
    
    def listar_emprestimos_do_membro(self, membro: Membro) -> list[Emprestimo]:
        return [e for e in self.emprestimos if e.membro.email == membro.email]

    def listar_multas_do_membro(self, membro: Membro) -> list[Multa]:
        return [m for m in self.multas if m.emprestimo_atrasado.membro.email == membro.email and not m.pago]
    
    # ------------------------------ EMPRESTIMO e DEVOLUÇÃO ---------------------------------------
    def realizar_emprestimo(self, email: str, titulo: str, para_reserva: bool = False) -> tuple[bool, str, object]:
        membro = self.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado.", None

        titulo_normalizado = self._normalizar(titulo)
        item = next((i for i in self.item if self._normalizar(i.titulo) == titulo_normalizado), None)
        if not item:
            return False, f"❗️ Item '{titulo}' não cadastrado no acervo.", None

        emprestimos_membro = self.listar_emprestimos_do_membro(membro)
        if len(emprestimos_membro) >= MAXIMO_EMPRESTIMO_MEMBRO:
            return False, f"❗️ {membro.nome} já atingiu o limite de {MAXIMO_EMPRESTIMO_MEMBRO} empréstimos ativos.", None
        
        if any(self._normalizar(e.livro.titulo) == titulo_normalizado for e in emprestimos_membro):
            return False, f"❗️ {membro.nome} já possui um exemplar do item '{titulo}' emprestado.", None

        data_emprestimo = self.get_data_atual()
        if not item.verificar_disponibilidade():
            if para_reserva:
                reserva = Reserva(item, membro, data_emprestimo)
                self.reservas.append(reserva)
                return True, f"✔ Reserva confirmada para {membro.nome} - Livro: {reserva.livro.titulo}", reserva
            return False, "ITEM_INDISPONIVEL", None

        if item.emprestar():
            data_devolucao_prevista = data_emprestimo + timedelta(days=DIAS_EMPRESTIMO)
            emprestimo = Emprestimo(item, membro, data_emprestimo, data_devolucao_prevista)
            self.emprestimos.append(emprestimo)
            self.historico_emprestimo.append(emprestimo)
            msg = f"\n✔ Empréstimo realizado com sucesso!\n{emprestimo}"
            return True, msg, emprestimo
        
        return False, "Ocorreu um erro desconhecido ao tentar emprestar.", None

    def realizar_devolucao(self, email: str, titulo: str) -> tuple[bool, str]:
        membro = self.buscar_membro_por_email(email)
        if not membro:
            return False, f"❗️ Membro com email {email} não encontrado."
        
        multas_pendentes = self.listar_multas_do_membro(membro)
        if multas_pendentes:
            msg = f"❗️ {membro.nome} possui multas pendentes e não pode realizar a devolução."
            return False, msg, True 
        
        titulo_normalizado = self._normalizar(titulo)
        emprestimo_a_devolver = next((e for e in self.emprestimos if e.membro.email == email and self._normalizar(e.livro.titulo) == titulo_normalizado), None)

        if not emprestimo_a_devolver:
            return False, f"❗️ Empréstimo do item '{titulo}' para {membro.nome} não encontrado."
            
        emprestimo_a_devolver.livro.devolver()
        self.emprestimos.remove(emprestimo_a_devolver)
        
        return True, f"✔ Devolução do item '{titulo}' por {membro.nome} realizada com sucesso!"
        
    # ------------------------------ EVENTOS -----------------------------------------------    
    def agendar_evento(self, nome, descricao, data, local) -> tuple[bool, str, Evento]:
        try:
            novo_evento = Evento(nome, descricao, data, local)
            self.eventos.append(novo_evento)
            return True, f"✔ Evento '{nome}' agendado com sucesso.", novo_evento
        except Exception as e:
            return False, f"Ocorreu um erro ao agendar o evento: {e}", None
    
    def divulgar_eventos(self) -> list:
        return self.eventos[:5]
    
    def cancelar_evento(self, nome_evento: str) -> tuple[bool, str]:
        nome_evento_normalizado = self._normalizar(nome_evento)
        evento = next((e for e in self.eventos if self._normalizar(e.nome) == nome_evento_normalizado), None)
        
        if evento:
            self.eventos.remove(evento)
            return True, f"✔ Evento '{evento.nome}' cancelado com sucesso."
        else:
            return False, f"❗️ Evento '{nome_evento}' não encontrado."
    
    def listar_eventos(self) -> list:
        return self.eventos[:5]

    # ------------------------------- Verificar atrasos da biblioteca -------------------------------
    def verificar_atrasos(self) -> list[str]:
        mensagens = []
        hoje = self.get_data_atual()
        atrasados = [e for e in self.emprestimos if e.data_devolucao_prevista < hoje]

        if not atrasados:
            mensagens.append("✔ Nenhum empréstimo atrasado para gerar multas.")
            return mensagens

        mensagens.append("\n--- Verificação de atrasos e geração de multas ---")
        for emprestimo in atrasados:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            if dias_atraso > 0:
                valor_multa = dias_atraso * VALOR_MULTA
                multa_existente = next((m for m in self.multas if m.emprestimo_atrasado == emprestimo), None)
                if not multa_existente:
                    nova_multa = Multa(emprestimo, valor_multa)
                    self.multas.append(nova_multa)
                    mensagens.append(f"🔴 Multa GERADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n   - Valor: R$ {valor_multa:.2f} ({dias_atraso} dias de atraso).")
                else:
                    multa_existente.valor = valor_multa
                    mensagens.append(f"🟡 Multa ATUALIZADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n   - Novo Valor: R$ {valor_multa:.2f} ({dias_atraso} dias de atraso).")
        return mensagens


    #------------------------------- Relatório de uso ---------------------------------------------------
    def relatorio_uso(self) -> dict | None:
        todos_emprestimos = self.historico_emprestimo
        if not todos_emprestimos:
            return None
        
        #Atividade dos itens
        titulos_emprestados = [e.livro.titulo for e in todos_emprestimos]
        contagem_livro = Counter(titulos_emprestados).most_common(5)
        
        genero_emprestados = [e.livro.genero for e in todos_emprestimos]
        contagem_genero = Counter(genero_emprestados).most_common(3)
        
        #Atividade dos membros
        membros_ativos = [e.membro.nome for e in todos_emprestimos]
        contagem_membros = Counter(membros_ativos).most_common(3)
            
        #Análise de multas
        total_multas_geradas = sum(m.valor for m in self.multas)
        total_multas_pagas = sum(m.valor for m in self.multas if m.pago)
        taxa_pagamento = (total_multas_pagas / total_multas_geradas * 100) if total_multas_geradas > 0 else 0
        
        relatorio = {
            "top_livros": contagem_livro,
            "top_generos": contagem_genero,
            "membros_ativos": contagem_membros,
            "total_multas_geradas": total_multas_geradas,
            "total_multas_pagas": total_multas_pagas,
            "taxa_pagamento_multas": taxa_pagamento,
            "total_livros_acervo": len(self.item),
            "total_membros": len(self.membros),
            "total_emprestimos_historico": len(todos_emprestimos),
            "emprestimos_atuais": len(self.emprestimos),
        }
        return relatorio