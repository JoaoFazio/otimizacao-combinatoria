"""
Problema das n-Rainhas (N-Queens Problem)
Algoritmo: Simulated Annealing

Referências:
- Gettysburg College: N-Queens Problem using Simulated Annealing
  https://cs.gettysburg.edu/~tneller/nsf/clue/tp/index.html
- Medium: N-Queens Problem using Backtracking
  https://medium.com/@codingfreak/n-queen-problem-using-backtracking-algorithm-11b0e5d21ecf
"""

import random
import math
import sys
import os
import time

# Adiciona pasta utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.common import *


# Parâmetros do Simulated Annealing
TEMPERATURA_INICIAL = 100.0
TEMPERATURA_MINIMA = 0.01
TAXA_RESFRIAMENTO = 0.995
MAX_ITERACOES = 10000


class NRainhas:
    """Classe para resolver problema das n-Rainhas usando Simulated Annealing."""
   
    def __init__(self, n: int, tamanhos_itens: List[int]):
        """
        Inicializa o problema das n-Rainhas.
       
        Args:
            n: Tamanho do tabuleiro (n x n)
            tamanhos_itens: Tamanhos das rainhas (para distribuição no tabuleiro)
        """
        self.n = n
        self.tamanhos_itens = tamanhos_itens
   
    def gerar_solucao_inicial(self) -> List[int]:
        """
        Gera uma posição inicial aleatória.
        Representação: lista onde índice = coluna e valor = linha
       
        Returns:
            Lista de posições das rainhas
        """
        return [random.randint(0, self.n - 1) for _ in range(self.n)]
   
    def calcular_conflitos(self, posicoes: List[int]) -> int:
        """
        Calcula número de pares de rainhas que se atacam.
       
        Args:
            posicoes: Posições das rainhas
           
        Returns:
            Número de conflitos
        """
        conflitos = 0
       
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Mesma linha
                if posicoes[i] == posicoes[j]:
                    conflitos += 1
                # Mesma diagonal
                elif abs(posicoes[i] - posicoes[j]) == abs(i - j):
                    conflitos += 1
       
        return conflitos
   
    def gerar_vizinho(self, posicoes: List[int]) -> List[int]:
        """
        Gera solução vizinha movendo uma rainha aleatoriamente.
       
        Args:
            posicoes: Posições atuais
           
        Returns:
            Novas posições
        """
        novas_posicoes = posicoes.copy()
       
        # Escolhe coluna aleatória
        coluna = random.randint(0, self.n - 1)
       
        # Move rainha para linha aleatória diferente
        nova_linha = random.randint(0, self.n - 1)
        novas_posicoes[coluna] = nova_linha
       
        return novas_posicoes
   
    def resolver(self) -> tuple:
        """
        Resolve usando Simulated Annealing.
       
        Returns:
            Tupla (melhor_solucao, num_conflitos_minimo)
        """
        print("Executando Simulated Annealing para N-Rainhas...")
        print(f"Parâmetros: N={self.n}, T0={TEMPERATURA_INICIAL}, α={TAXA_RESFRIAMENTO}")
       
        # Solução inicial
        posicoes_atuais = self.gerar_solucao_inicial()
        conflitos_atuais = self.calcular_conflitos(posicoes_atuais)
       
        melhores_posicoes = posicoes_atuais.copy()
        menor_conflitos = conflitos_atuais
       
        temperatura = TEMPERATURA_INICIAL
        iteracao = 0
       
        # Loop principal
        while temperatura > TEMPERATURA_MINIMA and iteracao < MAX_ITERACOES:
            # Se encontrou solução perfeita, para
            if menor_conflitos == 0:
                print(f"  ✓ Solução perfeita encontrada na iteração {iteracao}!")
                break
           
            # Gera vizinho
            novas_posicoes = self.gerar_vizinho(posicoes_atuais)
            novos_conflitos = self.calcular_conflitos(novas_posicoes)
           
            # Critério de aceitação
            delta = novos_conflitos - conflitos_atuais
           
            if delta <= 0 or random.random() < math.exp(-delta / temperatura):
                posicoes_atuais = novas_posicoes
                conflitos_atuais = novos_conflitos
               
                if conflitos_atuais < menor_conflitos:
                    melhores_posicoes = posicoes_atuais.copy()
                    menor_conflitos = conflitos_atuais
           
            # Feedback
            if (iteracao + 1) % 1000 == 0:
                print(f"  Iteração {iteracao + 1} - T={temperatura:.2f} - Conflitos: {menor_conflitos}")
           
            temperatura *= TAXA_RESFRIAMENTO
            iteracao += 1
       
        print(f"  Convergiu após {iteracao} iterações")
        print(f"  Solução válida: {menor_conflitos == 0}")
       
        return melhores_posicoes, menor_conflitos


def ler_entrada_rainhas(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do problema das n-Rainhas.
   
    Formato conforme Tabela 8:
    - Linha 1: Número de rainhas (n)
    - Linha 2: Tamanhos dos itens (rainhas)
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (n, tamanhos)
    """
    linhas = ler_arquivo_txt(caminho)
   
    n = int(linhas[0])
    tamanhos = [int(x) for x in linhas[1].split('\t') if x]
   
    return n, tamanhos


def formatar_saida_rainhas(posicoes: List[int], n: int) -> str:
    """
    Formata a saída com o tabuleiro e posições.
   
    Args:
        posicoes: Posições das rainhas
        n: Tamanho do tabuleiro
       
    Returns:
        String formatada
    """
    saida = f"Solução para {n}-Rainhas:\n\n"
   
    # Posições em formato texto
    saida += "Posições (coluna, linha):\n"
    for coluna, linha in enumerate(posicoes):
        saida += f"  Rainha {coluna}: ({coluna}, {linha})\n"
   
    # Tabuleiro visual
    saida += f"\nTabuleiro {n}x{n}:\n"
    for linha in range(n):
        linha_texto = ""
        for coluna in range(n):
            if posicoes[coluna] == linha:
                linha_texto += "♛ "
            else:
                linha_texto += ". "
        saida += linha_texto + "\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    n, tamanhos = ler_entrada_rainhas(caminho_entrada)
   
    print(f"Tamanho do tabuleiro: {n}x{n}")
   
    # Resolve problema
    inicio = time.time()
    problema = NRainhas(n, tamanhos)
    melhor_solucao, num_conflitos = problema.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    print(f"\n✓ Solução encontrada!")
    print(f"  Número de conflitos: {num_conflitos}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"6_rainhas{identificador}_{num_conflitos}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_rainhas(melhor_solucao, n)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DAS N-RAINHAS - SIMULATED ANNEALING")
   
    pasta_atual = os.path.dirname(__file__)
    pasta_entradas = os.path.join(pasta_atual, 'entradas')
   
    arquivos = listar_arquivos_entrada(pasta_entradas)
   
    if not arquivos:
        print("❌ Nenhum arquivo de entrada encontrado!")
        return
   
    print(f"Encontrados {len(arquivos)} arquivos de entrada\n")
   
    for arquivo in arquivos:
        processar_arquivo(arquivo)
        print()
   
    imprimir_separador("CONCLUÍDO")


if __name__ == "__main__":
    main()
