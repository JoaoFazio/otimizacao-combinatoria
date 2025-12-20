"""
Problema de Designação Generalizada (Generalized Assignment Problem - GAP)
Algoritmo: Simulated Annealing com Restrições

Referências:
- INFORMS: Branch and Bound Algorithms for the Generalized Assignment Problem
  https://pubsonline.informs.org/doi/abs/10.1287/mnsc.24.9.919
- Wikipedia: Generalized Assignment Problem
  https://en.wikipedia.org/wiki/Generalized_assignment_problem
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
TEMPERATURA_INICIAL = 500.0
TEMPERATURA_MINIMA = 0.1
TAXA_RESFRIAMENTO = 0.99
MAX_ITERACOES = 5000


class DesignacaoGeneralizada:
    """Classe para resolver GAP usando Simulated Annealing."""
   
    def __init__(self, num_programadores: int, num_modulos: int,
                 custos: List[List[int]], cargas: List[List[int]],
                 capacidades: List[int]):
        """
        Inicializa o problema de designação generalizada.
       
        Args:
            num_programadores: Número de programadores disponíveis
            num_modulos: Número de módulos a serem desenvolvidos
            custos: Matriz de custos[programador][modulo]
            cargas: Matriz de cargas horárias[programador][modulo]
            capacidades: Capacidades horárias de cada programador
        """
        self.num_programadores = num_programadores
        self.num_modulos = num_modulos
        self.custos = custos
        self.cargas = cargas
        self.capacidades = capacidades
   
    def gerar_solucao_inicial_gulosa(self) -> List[int]:
        """
        Gera solução inicial usando heurística gulosa.
        Atribui cada módulo ao programador de menor custo que tenha capacidade.
       
        Returns:
            Lista de atribuições (índice = módulo, valor = programador)
        """
        atribuicao = [-1] * self.num_modulos
        cargas_usadas = [0] * self.num_programadores
       
        # Para cada módulo, tenta atribuir ao programador de menor custo
        for modulo in range(self.num_modulos):
            melhor_prog = -1
            menor_custo = float('inf')
           
            for prog in range(self.num_programadores):
                # Verifica se tem capacidade
                if cargas_usadas[prog] + self.cargas[prog][modulo] <= self.capacidades[prog]:
                    if self.custos[prog][modulo] < menor_custo:
                        menor_custo = self.custos[prog][modulo]
                        melhor_prog = prog
           
            # Se encontrou programador viável, atribui
            if melhor_prog != -1:
                atribuicao[modulo] = melhor_prog
                cargas_usadas[melhor_prog] += self.cargas[melhor_prog][modulo]
            else:
                # Se não encontrou, atribui aleatoriamente (será penalizado)
                atribuicao[modulo] = random.randint(0, self.num_programadores - 1)
       
        return atribuicao
   
    def calcular_custo_e_viabilidade(self, atribuicao: List[int]) -> tuple:
        """
        Calcula o custo total e verifica viabilidade da solução.
       
        Args:
            atribuicao: Lista de atribuições
           
        Returns:
            Tupla (custo_total, é_viável)
        """
        custo_total = 0
        cargas_usadas = [0] * self.num_programadores
       
        for modulo in range(self.num_modulos):
            prog = atribuicao[modulo]
            custo_total += self.custos[prog][modulo]
            cargas_usadas[prog] += self.cargas[prog][modulo]
       
        # Verifica se respeita capacidades
        viavel = all(cargas_usadas[p] <= self.capacidades[p]
                     for p in range(self.num_programadores))
       
        return custo_total, viavel
   
    def calcular_custo_penalizado(self, atribuicao: List[int]) -> float:
        """
        Calcula custo com penalização para soluções inviáveis.
       
        Args:
            atribuicao: Lista de atribuições
           
        Returns:
            Custo penalizado
        """
        custo, viavel = self.calcular_custo_e_viabilidade(atribuicao)
       
        if viavel:
            return float(custo)
       
        # Penaliza fortemente soluções inviáveis
        cargas_usadas = [0] * self.num_programadores
        for modulo in range(self.num_modulos):
            prog = atribuicao[modulo]
            cargas_usadas[prog] += self.cargas[prog][modulo]
       
        # Calcula excesso de carga
        excesso = sum(max(0, cargas_usadas[p] - self.capacidades[p])
                     for p in range(self.num_programadores))
       
        return float(custo) + 1000.0 * excesso
   
    def gerar_vizinho(self, atribuicao: List[int]) -> List[int]:
        """
        Gera uma solução vizinha trocando atribuição de um módulo.
       
        Args:
            atribuicao: Atribuição atual
           
        Returns:
            Nova atribuição
        """
        nova_atribuicao = atribuicao.copy()
       
        # Escolhe módulo aleatório
        modulo = random.randint(0, self.num_modulos - 1)
       
        # Atribui a outro programador aleatório
        novo_prog = random.randint(0, self.num_programadores - 1)
        nova_atribuicao[modulo] = novo_prog
       
        return nova_atribuicao
   
    def resolver(self) -> tuple:
        """
        Resolve GAP usando Simulated Annealing.
       
        Returns:
            Tupla (melhor_atribuicao, melhor_custo)
        """
        print("Executando Simulated Annealing para GAP...")
        print(f"Parâmetros: T0={TEMPERATURA_INICIAL}, Tmin={TEMPERATURA_MINIMA}, α={TAXA_RESFRIAMENTO}")
       
        # Solução inicial gulosa
        atribuicao_atual = self.gerar_solucao_inicial_gulosa()
        custo_atual = self.calcular_custo_penalizado(atribuicao_atual)
       
        melhor_atribuicao = atribuicao_atual.copy()
        melhor_custo = custo_atual
       
        temperatura = TEMPERATURA_INICIAL
        iteracao = 0
       
        # Loop principal
        while temperatura > TEMPERATURA_MINIMA and iteracao < MAX_ITERACOES:
            # Gera vizinho
            nova_atribuicao = self.gerar_vizinho(atribuicao_atual)
            novo_custo = self.calcular_custo_penalizado(nova_atribuicao)
           
            # Critério de aceitação
            delta = novo_custo - custo_atual
           
            if delta <= 0 or random.random() < math.exp(-delta / temperatura):
                atribuicao_atual = nova_atribuicao
                custo_atual = novo_custo
               
                # Atualiza melhor solução
                if custo_atual < melhor_custo:
                    melhor_atribuicao = atribuicao_atual.copy()
                    melhor_custo = custo_atual
           
            # Feedback
            if (iteracao + 1) % 500 == 0:
                custo_real, viavel = self.calcular_custo_e_viabilidade(melhor_atribuicao)
                print(f"  Iteração {iteracao + 1} - T={temperatura:.2f} - Melhor: {custo_real} (viável: {viavel})")
           
            # Resfriamento
            temperatura *= TAXA_RESFRIAMENTO
            iteracao += 1
       
        # Retorna custo real (sem penalização)
        custo_final, viavel = self.calcular_custo_e_viabilidade(melhor_atribuicao)
        print(f"  Convergiu após {iteracao} iterações")
        print(f"  Solução viável: {viavel}")
       
        return melhor_atribuicao, custo_final


def ler_entrada_gap(caminho: str) -> tuple:
    """
    Lê arquivo de entrada do GAP.
   
    Formato conforme especificação da Figura 2.
   
    Args:
        caminho: Caminho do arquivo
       
    Returns:
        Tupla (num_programadores, num_modulos, custos, cargas, capacidades)
    """
    linhas = ler_arquivo_txt(caminho)
    idx = 0
   
    num_programadores = int(linhas[idx])
    idx += 1
   
    num_modulos = int(linhas[idx])
    idx += 1
   
    # Lê matriz de custos
    custos = []
    for i in range(num_programadores):
        linha_custos = [int(x) for x in linhas[idx].split('\t') if x]
        custos.append(linha_custos)
        idx += 1
   
    # Lê matriz de cargas horárias
    cargas = []
    for i in range(num_programadores):
        linha_cargas = [int(x) for x in linhas[idx].split('\t') if x]
        cargas.append(linha_cargas)
        idx += 1
   
    # Lê capacidades
    capacidades = [int(x) for x in linhas[idx].split('\t') if x]
   
    return num_programadores, num_modulos, custos, cargas, capacidades


def formatar_saida_gap(atribuicao: List[int], custo_total: int,
                       num_programadores: int) -> str:
    """
    Formata a saída conforme especificação.
   
    Args:
        atribuicao: Lista de atribuições
        custo_total: Custo total da designação
        num_programadores: Número de programadores
       
    Returns:
        String formatada para saída
    """
    # Agrupa módulos por programador
    modulos_por_prog = {p: [] for p in range(num_programadores)}
    for modulo, prog in enumerate(atribuicao):
        modulos_por_prog[prog].append(modulo)
   
    saida = "Designação de módulos por programador:\n"
    for prog in range(num_programadores):
        modulos = modulos_por_prog[prog]
        if modulos:
            saida += f"Programador {prog}: módulos {', '.join(map(str, modulos))}\n"
        else:
            saida += f"Programador {prog}: nenhum módulo\n"
   
    saida += f"\nCusto total: {custo_total}\n"
   
    return saida


def processar_arquivo(caminho_entrada: str):
    """Processa um único arquivo de entrada."""
    imprimir_separador(f"Processando: {os.path.basename(caminho_entrada)}")
   
    # Lê entrada
    num_prog, num_mod, custos, cargas, capacidades = ler_entrada_gap(caminho_entrada)
   
    print(f"Programadores: {num_prog}")
    print(f"Módulos: {num_mod}")
   
    # Resolve problema
    inicio = time.time()
    gap = DesignacaoGeneralizada(num_prog, num_mod, custos, cargas, capacidades)
    melhor_atribuicao, melhor_custo = gap.resolver()
    tempo_decorrido = time.time() - inicio
   
    # Exibe resultado
    print(f"\n✓ Solução encontrada!")
    print(f"  Custo mínimo: {melhor_custo}")
    print(f"  Tempo de execução: {formatar_tempo(tempo_decorrido)}")
   
    # Salva saída
    identificador = extrair_nome_problema(caminho_entrada)
    pasta_saidas = os.path.join(os.path.dirname(os.path.dirname(caminho_entrada)), 'saidas')
    nome_saida = f"3_pdg{identificador}_{melhor_custo}_saida.txt"
    caminho_saida = os.path.join(pasta_saidas, nome_saida)
   
    conteudo_saida = formatar_saida_gap(melhor_atribuicao, melhor_custo, num_prog)
    escrever_saida(caminho_saida, conteudo_saida)


def main():
    """Função principal."""
    imprimir_separador("PROBLEMA DE DESIGNAÇÃO GENERALIZADA - SIMULATED ANNEALING")
   
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
