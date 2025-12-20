"""
Problema do Caixeiro Viajante e Roteamento (Traveling Salesman Problem - TSP)
Algoritmo: Simulated Annealing

Referências:
- Visual Studio Magazine: Traveling Salesman Using Simulated Annealing with Python
  https://visualstudiomagazine.com/articles/2021/12/01/traveling-salesman-using-simulated-annealing-with-python.aspx
- GeeksforGeeks: Simulated Annealing
  https://www.geeksforgeeks.org/simulated-annealing/
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
TEMPERATURA_INICIAL = 1000.0
TEMPERATURA_MINIMA = 0.01
TAXA_RESFRIAMENTO = 0.995
MAX_ITERACOES = 10000


class TSPSimulatedAnnealing:
    """Classe para resolver TSP usando Simulated Annealing."""
   
    def __init__(self, num_vertices: int, matriz_distancias: List[List[int]]):
        """
        Inicializa o problema TSP.
       
        Args:
            num_vertices: Número de vértices no grafo
            matriz_distancias: Matriz de distâncias entre vértices
        """
        self.num_vertices = num_vertices
        self.matriz_distancias = matriz_distancias
   
    def calcular_custo_rota(self, rota: List[int]) -> int:
        """
        Calcula o custo total de uma rota.
       
        Args:
            rota: Lista de vértices representando a rota
           
        Returns:
            Custo total da rota
        """
        custo = 0
        for i in range(len(rota)):
            origem = rota[i]
            destino = rota[(i + 1) % len(rota)]  # Volta para origem
            custo += self.matriz_distancias[origem][destino]
        return custo
   
    def gerar_rota_inicial(self) -> List[int]:
        """
        Gera uma rota inicial aleatória.
       
        Returns:
            Lista de vértices em ordem aleatória
        """
        rota = list(range(self.num_vertices))
        random.shuffle(rota)
        return rota
   
    def gerar_vizinho_2opt(self, rota: List[int]) -> List[int]:
        """
        Gera uma rota vizinha usando operador 2-opt.
        Inverte um segmento aleatório da rota.
       
        Args:
            rota: Rota atual
           
        Returns:
            Nova rota (vizinho)
        """
        nova_rota = rota.copy()
       
        # Escolhe dois pontos aleatórios
        i, j = sorted(random.sample(range(self.num_vertices), 2))
       
        # Inverte o segmento entre i e j
        nova_rota[i:j+1] = reversed(nova_rota[i:j+1])
       
        return nova_rota
   
    def criterio_metropolis(self, delta_custo: int, temperatura: float) -> bool:
        """
        Critério de aceitação de Metropolis.
       
        Args:
            delta_custo: Diferença de custo (novo - atual)
            temperatura: Temperatura atual
           
        Returns:
            True se a solução deve ser aceita
        """
        if delta_custo <= 0:
            return True  # Sempre aceita melhorias
       
        # Aceita pioras com probabilidade exp(-delta/T)
        probabilidade = math.exp(-delta_custo / temperatura)
        return random.random() < probabilidade
   
    def resolver(self) -> tuple:
        """
        Resolve TSP usando Simulated Annealing.
       
        Returns:
            Tupla (melhor_rota, melhor_custo, historico)
        """
        print("Executando Simulated Annealing...")
        print(f"Parâmetros: T0={TEMPERATURA_INICIAL}, Tmin={TEMPERATURA_MINIMA}, α={TAXA_RESFRIAMENTO}")
       
        # Solução inicial
        rota_atual = self.gerar_rota_inicial()
        custo_atual = self.calcular_custo_rota(rota_atual)
       
        melhor_rota = rota_atual.copy()
        melhor_custo = custo_atual
       
        temperatura = TEMPERATURA_INICIAL
        historico = []
        iteracao = 0
       
        # Loop principal
        while temperatura > TEMPERATURA_MINIMA and iteracao < MAX_ITERACOES:
            # Gera vizinho
            nova_rota = self.gerar_vizinho_2opt(rota_atual)
            novo_custo = self.calcular_custo_rota(nova_rota)
           
            # Avalia aceitação
            delta_custo = novo_custo - custo_atual
           
            if self.criterio_metropolis(delta_custo, temperatura):
                rota_atual = nova_rota
                custo_atual = novo_custo
               
                # Atualiza melhor solução
                if custo_atual < melhor_custo:
                    melhor_rota = rota_atual.copy()
                    melhor_custo = custo_atual
           
            historico.append(melhor_custo)
           
            # Feedback
            if (iteracao + 1) % 1000 == 0:
                print(f"  Iteração {iteracao + 1} - T={temperatura:.2f} - Melhor custo: {melhor_custo}")
           
            # Resfriamento
            temperatura *= TAXA_RESFRIAMENTO
            iteracao += 1
       
        print(f"  Convergiu após {iteracao} iterações")
        return melhor_rota, melhor_custo, historico


def ler_entrada_tsp(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do TSP.
   
    Formato:
    - Linha 1: Número de vértices
    - Linhas seguintes: Matriz de adjacência (distâncias)
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (num_vertices, matriz_distancias)
    """
    linhas = ler_arquivo_txt(caminho)
   
    num_vertices = int(linhas[0])
    matriz_distancias = []
   
    for i in range(1, num_vertices + 1):
        if i < len(linhas):
            # Separa por qualquer espaço em branco (espaço, tab, etc)
            linha_valores = [int(x) for x in linhas[i].split() if x]
            matriz_distancias.append(linha_valores)
   
    return num_vertices, matriz_distancias


def formatar_saida_tsp(rota: List[int], custo: int) -> str:
    """
    Formata a saída conforme especificação.
   
    Args:
        rota: Solução (sequência de vértices)
        custo: Custo total da rota
       
    Returns:
        String formatada para saída
    """
    # Adiciona retorno à origem
    rota_completa = rota + [rota[0]]
   
    saida = f"Rota: {' -> '.join(map(str, rota_completa))}\n"
    saida += f"Custo total: {custo}\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    num_vertices, matriz_distancias = ler_entrada_tsp(caminho_entrada)
   
    print(f"Número de vértices: {num_vertices}")
   
    # Resolve problema
    inicio = time.time()
    tsp = TSPSimulatedAnnealing(num_vertices, matriz_distancias)
    melhor_rota, melhor_custo, historico = tsp.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    print(f"\n✓ Solução encontrada!")
    print(f"  Custo mínimo: {melhor_custo}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"2_tsp{identificador}_{melhor_custo}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_tsp(melhor_rota, melhor_custo)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DO CAIXEIRO VIAJANTE - SIMULATED ANNEALING")
   
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
