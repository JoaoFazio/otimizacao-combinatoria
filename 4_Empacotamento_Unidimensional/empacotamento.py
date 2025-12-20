"""
Problema do Empacotamento Unidimensional (Bin Packing Problem)
Algoritmo: First Fit Decreasing (FFD) + Busca Local

Referências:
- GeeksforGeeks: Bin Packing Problem
  https://www.geeksforgeeks.org/bin-packing-problem-minimize-number-of-used-bins/
- Wikipedia: Bin Packing Problem
  https://en.wikipedia.org/wiki/Bin_packing_problem
"""

import sys
import os
import time

# Adiciona pasta utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.common import *


class EmpacotamentoUnidimensional:
    """Classe para resolver Bin Packing usando FFD + otimização."""
   
    def __init__(self, capacidade_recipiente: int, tamanhos_itens: List[int]):
        """
        Inicializa o problema de empacotamento.
       
        Args:
            capacidade_recipiente: Capacidade máxima de cada recipiente
            tamanhos_itens: Lista com tamanhos de cada item
        """
        self.capacidade = capacidade_recipiente
        self.itens = tamanhos_itens.copy()
        self.num_itens = len(tamanhos_itens)
   
    def first_fit_decreasing(self) -> List[List[int]]:
        """
        Algoritmo First Fit Decreasing (FFD).
        Implementação conforme pseudocódigo da Figura 3 da especificação.
       
        Returns:
            Lista de recipientes, cada um contendo índices dos itens
        """
        # Passo 1: Ordena itens em ordem decrescente de tamanho
        itens_indexados = [(i, tamanho) for i, tamanho in enumerate(self.itens)]
        itens_ordenados = sorted(itens_indexados, key=lambda x: x[1], reverse=True)
       
        recipientes = []
        capacidades_restantes = []
       
        # Passo 2-3: Para cada item, tenta colocar no primeiro recipiente que couber
        for idx_item, tamanho in itens_ordenados:
            colocado = False
           
            # Tenta colocar em recipiente existente
            for i, recipiente in enumerate(recipientes):
                if capacidades_restantes[i] >= tamanho:
                    # Coloca item no recipiente
                    recipiente.append(idx_item)
                    capacidades_restantes[i] -= tamanho
                    colocado = True
                    break
           
            # Se não coube em nenhum, cria novo recipiente
            if not colocado:
                recipientes.append([idx_item])
                capacidades_restantes.append(self.capacidade - tamanho)
       
        return recipientes
   
    def calcular_num_recipientes(self, solucao: List[List[int]]) -> int:
        """Retorna número de recipientes usados."""
        return len(solucao)
   
    def busca_local_melhoria(self, solucao_inicial: List[List[int]],
                            max_tentativas: int = 100) -> List[List[int]]:
        """
        Aplica busca local para tentar melhorar a solução FFD.
        Tenta mover itens entre recipientes para reduzir o número total.
       
        Args:
            solucao_inicial: Solução inicial (FFD)
            max_tentativas: Número máximo de tentativas de melhoria
           
        Returns:
            Melhor solução encontrada
        """
        melhor_solucao = [recipiente.copy() for recipiente in solucao_inicial]
        melhor_num_recipientes = len(melhor_solucao)
       
        for _ in range(max_tentativas):
            # Tenta consolidar recipientes
            melhorou = False
           
            # Para cada par de recipientes
            for i in range(len(melhor_solucao)):
                if i >= len(melhor_solucao):
                    break
                   
                for j in range(i + 1, len(melhor_solucao)):
                    if j >= len(melhor_solucao):
                        break
                   
                    # Calcula capacidade usada em cada recipiente
                    cap_i = sum(self.itens[item] for item in melhor_solucao[i])
                    cap_j = sum(self.itens[item] for item in melhor_solucao[j])
                   
                    # Se consegue juntar os dois recipientes
                    if cap_i + cap_j <= self.capacidade:
                        # Junta recipiente j em i
                        melhor_solucao[i].extend(melhor_solucao[j])
                        # Remove recipiente j
                        melhor_solucao.pop(j)
                        melhorou = True
                        break
               
                if melhorou:
                    break
           
            if not melhorou:
                break
       
        return melhor_solucao
   
    def resolver(self) -> List[List[int]]:
        """
        Resolve o problema de empacotamento.
       
        Returns:
            Melhor solução encontrada (lista de recipientes)
        """
        print("Executando First Fit Decreasing (FFD)...")
       
        # Solução inicial com FFD
        solucao_ffd = self.first_fit_decreasing()
        print(f"  FFD: {len(solucao_ffd)} recipientes")
       
        # Tenta melhorar com busca local
        print("Aplicando busca local para otimização...")
        solucao_otimizada = self.busca_local_melhoria(solucao_ffd)
        print(f"  Após otimização: {len(solucao_otimizada)} recipientes")
       
        return solucao_otimizada


def ler_entrada_empacotamento(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do problema de empacotamento.
   
    Formato conforme Tabela 6:
    - Linha 1: Capacidade dos recipientes
    - Linha 2: Número de itens
    - Linha 3: Tamanhos dos itens
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (capacidade, tamanhos_itens)
    """
    linhas = ler_arquivo_txt(caminho)
   
    capacidade = int(linhas[0])
    num_itens = int(linhas[1])
    tamanhos = [int(x) for x in linhas[2].split('\t') if x]
   
    return capacidade, tamanhos


def formatar_saida_empacotamento(solucao: List[List[int]],
                                 tamanhos: List[int],
                                 capacidade: int) -> str:
    """
    Formata a saída conforme especificação.
   
    Args:
        solucao: Lista de recipientes com itens
        tamanhos: Tamanhos dos itens
        capacidade: Capacidade dos recipientes
       
    Returns:
        String formatada para saída
    """
    saida = f"Número de recipientes utilizados: {len(solucao)}\n\n"
   
    for i, recipiente in enumerate(solucao):
        itens_str = ', '.join(map(str, recipiente))
        capacidade_usada = sum(tamanhos[item] for item in recipiente)
        saida += f"Recipiente {i + 1}: itens [{itens_str}]\n"
        saida += f"  Capacidade usada: {capacidade_usada}/{capacidade}\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    capacidade, tamanhos = ler_entrada_empacotamento(caminho_entrada)
   
    print(f"Capacidade dos recipientes: {capacidade}")
    print(f"Número de itens: {len(tamanhos)}")
   
    # Resolve problema
    inicio = time.time()
    problema = EmpacotamentoUnidimensional(capacidade, tamanhos)
    melhor_solucao = problema.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    num_recipientes = len(melhor_solucao)
    print(f"\n✓ Solução encontrada!")
    print(f"  Número mínimo de recipientes: {num_recipientes}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"4_peu{identificador}_{num_recipientes}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_empacotamento(melhor_solucao, tamanhos, capacidade)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DE EMPACOTAMENTO UNIDIMENSIONAL - FFD")
   
    # Localiza pasta de entradas
    pasta_atual = os.path.dirname(__file__)
    pasta_entradas = os.path.join(pasta_atual, 'entradas')
   
    # Lista arquivos
    arquivos = listar_arquivos_entrada(pasta_entradas)
   
    if not arquivos:
        print("❌ Nenhum arquivo de entrada encontrado!")
        return
   
    print(f"Encontrados {len(arquivos)} arquivos de entrada\n")
   
    # Processa cada arquivo
    for arquivo in arquivos:
        processar_arquivo(arquivo)
        print()
   
    imprimir_separador("CONCLUÍDO")


if __name__ == "__main__":
    main()
