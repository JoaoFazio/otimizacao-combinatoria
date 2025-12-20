"""
Problema da Mochila Binária (Binary Knapsack Problem)
Algoritmo: Algoritmo Genético (Genetic Algorithm)

Referências:
- Gitconnected: Genetic Algorithm for Knapsack Problem
  https://levelup.gitconnected.com/genetic-algorithm-for-knapsack-problem-e5ee69b5c8ab
- GeeksforGeeks: 0/1 Knapsack using Genetic Algorithm
  https://www.geeksforgeeks.org/0-1-knapsack-using-genetic-algorithm/
"""

import random
import sys
import os
import time

# Adiciona pasta utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.common import *


# Parâmetros do Algoritmo Genético
TAMANHO_POPULACAO = 100
NUM_GERACOES = 500
TAXA_MUTACAO = 0.01
TAMANHO_TORNEIO = 5


class MochilaBinaria:
    """Resolve problema da mochila com Algoritmo Genético."""
   
    def __init__(self, capacidade, valores, custos):
        self.capacidade = capacidade
        self.valores = valores
        self.custos = custos
        self.num_itens = len(valores)
       
    def criar_individuo(self):
        # Cria cromossomo binário aleatório
        return [random.randint(0, 1) for _ in range(self.num_itens)]
   
    def criar_populacao_inicial(self):
        # Gera população inicial
        return [self.criar_individuo() for _ in range(TAMANHO_POPULACAO)]
   
    def calcular_fitness(self, individuo):
        # Calcula valor total e peso
        valor_total = sum(self.valores[i] * individuo[i] for i in range(self.num_itens))
        peso_total = sum(self.custos[i] * individuo[i] for i in range(self.num_itens))
       
        # Penaliza se ultrapassar capacidade
        if peso_total > self.capacidade:
            return 0
       
        return valor_total
   
    def selecao_torneio(self, populacao):
        # Seleção por torneio
        torneio = random.sample(populacao, TAMANHO_TORNEIO)
        return max(torneio, key=self.calcular_fitness)
   
    def crossover_um_ponto(self, pai1, pai2):
        # Crossover de 1 ponto
        ponto_corte = random.randint(1, self.num_itens - 1)
       
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
       
        return filho1, filho2
   
    def mutacao(self, individuo):
        # Mutação bit-flip
        individuo_mutado = individuo.copy()
       
        for i in range(self.num_itens):
            if random.random() < TAXA_MUTACAO:
                individuo_mutado[i] = 1 - individuo_mutado[i]
       
        return individuo_mutado
   
    def resolver(self):
        # Executa o AG
        print("Executando Algoritmo Genético...")
        print(f"Parâmetros: Pop={TAMANHO_POPULACAO}, Ger={NUM_GERACOES}, Mut={TAXA_MUTACAO}")
       
        # População inicial
        populacao = self.criar_populacao_inicial()
       
        # Inicializa melhor solução com primeiro indivíduo
        melhor_global = populacao[0].copy()
        melhor_fitness_global = self.calcular_fitness(melhor_global)
        historico = []
       
        # Evolução
        for geracao in range(NUM_GERACOES):
            # Avalia população
            fitness_populacao = [self.calcular_fitness(ind) for ind in populacao]
           
            # Atualiza melhor solução
            idx_melhor = fitness_populacao.index(max(fitness_populacao))
            if fitness_populacao[idx_melhor] > melhor_fitness_global:
                melhor_global = populacao[idx_melhor].copy()
                melhor_fitness_global = fitness_populacao[idx_melhor]
           
            historico.append(melhor_fitness_global)
           
            # Feedback a cada 100 gerações
            if (geracao + 1) % 100 == 0:
                print(f"  Geração {geracao + 1}/{NUM_GERACOES} - Melhor fitness: {melhor_fitness_global}")
           
            # Nova geração
            nova_populacao = []
           
            # Elitismo: mantém o melhor indivíduo
            nova_populacao.append(melhor_global.copy())
           
            # Gera resto da população
            while len(nova_populacao) < TAMANHO_POPULACAO:
                # Seleção
                pai1 = self.selecao_torneio(populacao)
                pai2 = self.selecao_torneio(populacao)
               
                # Crossover
                filho1, filho2 = self.crossover_um_ponto(pai1, pai2)
               
                # Mutação
                filho1 = self.mutacao(filho1)
                filho2 = self.mutacao(filho2)
               
                nova_populacao.append(filho1)
                if len(nova_populacao) < TAMANHO_POPULACAO:
                    nova_populacao.append(filho2)
           
            populacao = nova_populacao
       
        return melhor_global, melhor_fitness_global, historico


def ler_entrada_mochila(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do problema da mochila.
   
    Formato:
    - Linha 1: Capacidade da mochila
    - Linha 2: Benefícios dos itens (separados por tab)
    - Linha 3: Custos dos itens (separados por tab)
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (capacidade, valores, custos)
    """
    linhas = ler_arquivo_txt(caminho)
   
    capacidade = int(linhas[0])
    valores = [int(x) for x in linhas[1].split('\t') if x]
    custos = [int(x) for x in linhas[2].split('\t') if x]
   
    return capacidade, valores, custos


def formatar_saida_mochila(individuo: List[int], fitness: int) -> str:
    """
    Formata a saída conforme especificação.
   
    Args:
        individuo: Solução (itens selecionados)
        fitness: Valor total obtido
       
    Returns:
        String formatada para saída
    """
    itens_selecionados = [str(i) for i, selecionado in enumerate(individuo) if selecionado == 1]
   
    saida = f"Itens selecionados: {', '.join(itens_selecionados)}\n"
    saida += f"Valor total: {fitness}\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    capacidade, valores, custos = ler_entrada_mochila(caminho_entrada)
   
    print(f"Capacidade: {capacidade}")
    print(f"Número de itens: {len(valores)}")
   
    # Resolve problema
    inicio = time.time()
    mochila = MochilaBinaria(capacidade, valores, custos)
    melhor_individuo, melhor_fitness, historico = mochila.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    print(f"\n✓ Solução encontrada!")
    print(f"  Benefício máximo: {melhor_fitness}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Calcula peso usado
    peso_usado = sum(custos[i] * melhor_individuo[i] for i in range(len(custos)))
    print(f"  Peso utilizado: {peso_usado}/{capacidade}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"1_mochila{identificador}_{melhor_fitness}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_mochila(melhor_individuo, melhor_fitness)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DA MOCHILA BINÁRIA - ALGORITMO GENÉTICO")
   
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
