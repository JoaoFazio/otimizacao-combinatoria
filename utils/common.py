"""
Módulo de utilitários comuns para todos os problemas de otimização.
Fornece funções auxiliares para leitura de entrada, escrita de saída e validação.
"""

import os
from typing import List, Any


def ler_arquivo_txt(caminho: str) -> List[str]:
    """
    Lê um arquivo de texto e retorna lista de linhas.
   
    Args:
        caminho: Caminho do arquivo a ser lido
       
    Returns:
        Lista de linhas do arquivo
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f.readlines()]


def escrever_saida(caminho_saida: str, conteudo: str):
    """
    Escreve conteúdo em arquivo de saída.
   
    Args:
        caminho_saida: Caminho do arquivo de saída
        conteudo: Conteúdo a ser escrito
    """
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
   
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(conteudo)
   
    print(f"✓ Saída salva em: {caminho_saida}")


def listar_arquivos_entrada(pasta_entradas: str, extensao: str = ".txt") -> List[str]:
    """
    Lista todos os arquivos de entrada de uma pasta.
   
    Args:
        pasta_entradas: Pasta contendo arquivos de entrada
        extensao: Extensão dos arquivos (padrão: .txt)
       
    Returns:
        Lista de caminhos completos dos arquivos
    """
    arquivos = []
    for arquivo in sorted(os.listdir(pasta_entradas)):
        if arquivo.endswith(extensao):
            arquivos.append(os.path.join(pasta_entradas, arquivo))
    return arquivos


def extrair_nome_problema(caminho_arquivo: str) -> str:
    """
    Extrai o identificador do problema do nome do arquivo.
   
    Exemplo: "Mochila10.txt" -> "10"
   
    Args:
        caminho_arquivo: Caminho do arquivo
       
    Returns:
        Identificador do problema
    """
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
   
    # Remove prefixos comuns
    for prefixo in ['Mochila', 'Entrada ', 'PDG', 'PEU', 'Circuito', 'Rainhas']:
        if nome_sem_extensao.startswith(prefixo):
            return nome_sem_extensao[len(prefixo):]
   
    return nome_sem_extensao


def formatar_tempo(segundos: float) -> str:
    """
    Formata tempo em segundos para string legível.
   
    Args:
        segundos: Tempo em segundos
       
    Returns:
        String formatada (ex: "2.35s" ou "125.4ms")
    """
    if segundos < 1:
        return f"{segundos * 1000:.1f}ms"
    return f"{segundos:.2f}s"


def imprimir_separador(titulo: str = ""):
    """
    Imprime um separador visual com título opcional.
   
    Args:
        titulo: Título a ser exibido no separador
    """
    if titulo:
        print(f"\n{'='*60}")
        print(f"  {titulo}")
        print(f"{'='*60}")
    else:
        print(f"{'='*60}")
