"""
Problema de Conexão de Circuitos (Circuit Connection Optimization)
Algoritmo: Simulated Annealing para Otimização de Conexões

Referências:
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
TEMPERATURA_INICIAL = 300.0
TEMPERATURA_MINIMA = 0.1
TAXA_RESFRIAMENTO = 0.98
MAX_ITERACOES = 5000


class ConexaoCircuitos:
    """Classe para resolver problema de conexão de circuitos."""
   
    def __init__(self, num_componentes: int, num_conexoes_total: int,
                 restricoes_min: List[int], restricoes_max: List[int],
                 posicoes: List[tuple]):
        """
        Inicializa o problema de conexão de circuitos.
       
        Args:
            num_componentes: Número de componentes no circuito
            num_conexoes_total: Número total de conexões necessárias
            restricoes_min: Mínimo de conexões por componente
            restricoes_max: Máximo de conexões por componente
            posicoes: Posições (x, y) de cada componente
        """
        self.num_componentes = num_componentes
        self.num_conexoes_total = num_conexoes_total
        self.restricoes_min = restricoes_min
        self.restricoes_max = restricoes_max
        self.posicoes = posicoes
   
    def calcular_distancia_euclidiana(self, comp1: int, comp2: int) -> float:
        """Calcula distância euclidiana entre dois componentes."""
        x1, y1 = self.posicoes[comp1]
        x2, y2 = self.posicoes[comp2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
   
    def gerar_solucao_inicial(self) -> List[tuple]:
        """
        Gera solução inicial aleatória respeitando restrições básicas.
       
        Returns:
            Lista de tuplas (componente1, componente2) representando conexões
        """
        conexoes = []
        contador_conexoes = [0] * self.num_componentes
       
        tentativas = 0
        max_tentativas = self.num_conexoes_total * 10
       
        while len(conexoes) < self.num_conexoes_total and tentativas < max_tentativas:
            # Escolhe dois componentes aleatórios
            c1 = random.randint(0, self.num_componentes - 1)
            c2 = random.randint(0, self.num_componentes - 1)
           
            if c1 == c2:
                tentativas += 1
                continue
           
            # Ordena para evitar duplicatas
            if c1 > c2:
                c1, c2 = c2, c1
           
            # Verifica se conexão já existe
            if (c1, c2) in conexoes:
                tentativas += 1
                continue
           
            # Verifica restrições
            if (contador_conexoes[c1] < self.restricoes_max[c1] and
                contador_conexoes[c2] < self.restricoes_max[c2]):
                conexoes.append((c1, c2))
                contador_conexoes[c1] += 1
                contador_conexoes[c2] += 1
           
            tentativas += 1
       
        return conexoes
   
    def calcular_custo_e_viabilidade(self, conexoes: List[tuple]) -> tuple:
        """
        Calcula custo total e verifica viabilidade.
       
        Args:
            conexoes: Lista de conexões
           
        Returns:
            Tupla (custo_total, é_viável)
        """
        # Calcula distância total
        custo_total = sum(self.calcular_distancia_euclidiana(c1, c2)
                         for c1, c2 in conexoes)
       
        # Verifica restrições
        contador_conexoes = [0] * self.num_componentes
        for c1, c2 in conexoes:
            contador_conexoes[c1] += 1
            contador_conexoes[c2] += 1
       
        viavel = all(
            self.restricoes_min[i] <= contador_conexoes[i] <= self.restricoes_max[i]
            for i in range(self.num_componentes)
        )
       
        return custo_total, viavel
   
    def calcular_custo_penalizado(self, conexoes: List[tuple]) -> float:
        """Calcula custo com penalização para soluções inviáveis."""
        custo, viavel = self.calcular_custo_e_viabilidade(conexoes)
       
        if viavel:
            return custo
       
        # Penaliza violações de restrições
        contador_conexoes = [0] * self.num_componentes
        for c1, c2 in conexoes:
            contador_conexoes[c1] += 1
            contador_conexoes[c2] += 1
       
        penalidade = 0
        for i in range(self.num_componentes):
            if contador_conexoes[i] < self.restricoes_min[i]:
                penalidade += (self.restricoes_min[i] - contador_conexoes[i]) * 100
            elif contador_conexoes[i] > self.restricoes_max[i]:
                penalidade += (contador_conexoes[i] - self.restricoes_max[i]) * 100
       
        return custo + penalidade
   
    def gerar_vizinho(self, conexoes: List[tuple]) -> List[tuple]:
        """
        Gera solução vizinha trocando uma conexão.
       
        Args:
            conexoes: Conexões atuais
           
        Returns:
            Novas conexões
        """
        novas_conexoes = conexoes.copy()
       
        if not novas_conexoes:
            return self.gerar_solucao_inicial()
       
        # Remove uma conexão aleatória
        idx_remover = random.randint(0, len(novas_conexoes) - 1)
        novas_conexoes.pop(idx_remover)
       
        # Adiciona nova conexão
        for _ in range(100):  # Tentativas limitadas
            c1 = random.randint(0, self.num_componentes - 1)
            c2 = random.randint(0, self.num_componentes - 1)
           
            if c1 != c2:
                if c1 > c2:
                    c1, c2 = c2, c1
               
                if (c1, c2) not in novas_conexoes:
                    novas_conexoes.append((c1, c2))
                    break
       
        return novas_conexoes
   
    def resolver(self) -> tuple:
        """
        Resolve usando Simulated Annealing.
       
        Returns:
            Tupla (melhores_conexoes, menor_custo)
        """
        print("Executando Simulated Annealing para Conexão de Circuitos...")
        print(f"Parâmetros: T0={TEMPERATURA_INICIAL}, Tmin={TEMPERATURA_MINIMA}, α={TAXA_RESFRIAMENTO}")
       
        # Solução inicial
        conexoes_atuais = self.gerar_solucao_inicial()
        custo_atual = self.calcular_custo_penalizado(conexoes_atuais)
       
        melhores_conexoes = conexoes_atuais.copy()
        menor_custo = custo_atual
       
        temperatura = TEMPERATURA_INICIAL
        iteracao = 0
       
        while temperatura > TEMPERATURA_MINIMA and iteracao < MAX_ITERACOES:
            # Gera vizinho
            novas_conexoes = self.gerar_vizinho(conexoes_atuais)
            novo_custo = self.calcular_custo_penalizado(novas_conexoes)
           
            # Critério de aceitação
            delta = novo_custo - custo_atual
           
            if delta <= 0 or random.random() < math.exp(-delta / temperatura):
                conexoes_atuais = novas_conexoes
                custo_atual = novo_custo
               
                if custo_atual < menor_custo:
                    melhores_conexoes = conexoes_atuais.copy()
                    menor_custo = custo_atual
           
            if (iteracao + 1) % 500 == 0:
                custo_real, viavel = self.calcular_custo_e_viabilidade(melhores_conexoes)
                print(f"  Iteração {iteracao + 1} - T={temperatura:.2f} - Melhor: {custo_real:.2f} (viável: {viavel})")
           
            temperatura *= TAXA_RESFRIAMENTO
            iteracao += 1
       
        custo_final, viavel = self.calcular_custo_e_viabilidade(melhores_conexoes)
        print(f"  Convergiu após {iteracao} iterações")
        print(f"  Solução viável: {viavel}")
       
        return melhores_conexoes, custo_final


def ler_entrada_circuitos(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do problema de circuitos.
   
    Formato:
    - Linha 1: Número de componentes
    - Linha 2: Número total de conexões
    - Linha 3: Número mínimo de conexões por componente
    - Linha 4: Posições X (separadas por tab, float com vírgula)
    - Linha 5: Posições Y (separadas por tab, float com vírgula)
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (num_componentes, num_conexoes, restricoes_min, restricoes_max, posicoes)
    """
    linhas = ler_arquivo_txt(caminho)
    idx = 0
   
    num_componentes = int(linhas[idx])
    idx += 1
   
    num_conexoes = int(linhas[idx])
    idx += 1
   
    num_min_conexoes = int(linhas[idx])
    idx += 1
   
    # Lê posições X (float com vírgula como separador decimal)
    posicoes_x = []
    for x in linhas[idx].split('\t'):
        if x.strip():
            # Substitui vírgula por ponto para conversão
            posicoes_x.append(float(x.replace(',', '.')))
    idx += 1
   
    # Lê posições Y
    posicoes_y = []
    for y in linhas[idx].split('\t'):
        if y.strip():
            # Substitui vírgula por ponto para conversão
            posicoes_y.append(float(y.replace(',', '.')))
   
    posicoes = list(zip(posicoes_x, posicoes_y))
   
    # Define restrições: mínimo = valor da linha 3, máximo = ilimitado
    restricoes_min = [num_min_conexoes] * num_componentes
    restricoes_max = [num_componentes - 1] * num_componentes  # Pode conectar com todos menos si mesmo
   
    return num_componentes, num_conexoes, restricoes_min, restricoes_max, posicoes


def formatar_saida_circuitos(conexoes: List[tuple], custo_total: float) -> str:
    """
    Formata a saída conforme especificação.
   
    Args:
        conexoes: Lista de conexões
        custo_total: Soma das distâncias
       
    Returns:
        String formatada
    """
    saida = "Conexões estabelecidas:\n"
    for i, (c1, c2) in enumerate(conexoes, 1):
        saida += f"  Conexão {i}: componente {c1} <-> componente {c2}\n"
   
    saida += f"\nCusto total (soma das distâncias): {custo_total:.2f}\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    num_comp, num_con, rest_min, rest_max, posicoes = ler_entrada_circuitos(caminho_entrada)
   
    print(f"Componentes: {num_comp}")
    print(f"Conexões necessárias: {num_con}")
   
    # Resolve problema
    inicio = time.time()
    problema = ConexaoCircuitos(num_comp, num_con, rest_min, rest_max, posicoes)
    melhores_conexoes, menor_custo = problema.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    print(f"\n✓ Solução encontrada!")
    print(f"  Custo mínimo: {menor_custo:.2f}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"5_circuito{identificador}_{int(menor_custo)}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_circuitos(melhores_conexoes, menor_custo)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DE CONEXÃO DE CIRCUITOS - SIMULATED ANNEALING")
   
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
