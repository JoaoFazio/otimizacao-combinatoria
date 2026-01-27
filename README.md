# Trabalho de Otimização Combinatória

Implementação de 6 problemas clássicos de otimização combinatória usando algoritmos metaheurísticos em Python.

**Disciplina:** Otimização Combinatória  
**Data de Entrega:** 05/02/2025

## 📋 Problemas Implementados

### 1. Mochila Binária (Binary Knapsack)
- **Algoritmo:** Algoritmo Genético (Genetic Algorithm)
- **Arquivo:** `1_Mochila_Binaria/mochila_binaria.py`
- **Descrição:** Maximiza benefício selecionando itens dentro da capacidade da mochila
- **Parâmetros:** População=100, Gerações=500, Mutação=1%

### 2. Caixeiro Viajante (TSP)
- **Algoritmo:** Simulated Annealing
- **Arquivo:** `2_TSP_Roteamento/tsp_roteamento.py`
- **Descrição:** Encontra a menor rota visitando todas as cidades
- **Parâmetros:** T₀=1000, α=0.995, 10000 iterações

### 3. Designação Generalizada (GAP)
- **Algoritmo:** Simulated Annealing com Restrições
- **Arquivo:** `3_Designacao_Generalizada/designacao_generalizada.py`
- **Descrição:** Atribui módulos a programadores minimizando custos
- **Parâmetros:** T₀=500, α=0.99, 5000 iterações

### 4. Empacotamento Unidimensional (Bin Packing)
- **Algoritmo:** First Fit Decreasing (FFD) + Busca Local
- **Arquivo:** `4_Empacotamento_Unidimensional/empacotamento.py`
- **Descrição:** Minimiza número de recipientes necessários
- **Método:** Heurística construtiva + otimização

### 5. Conexão de Circuitos
- **Algoritmo:** Simulated Annealing
- **Arquivo:** `5_Conexao_Circuitos/conexao_circuitos.py`
- **Descrição:** Minimiza distância total de conexões entre componentes
- **Parâmetros:** T₀=300, α=0.98, 5000 iterações

### 6. n-Rainhas
- **Algoritmo:** Simulated Annealing
- **Arquivo:** `6_N_Rainhas/n_rainhas.py`
- **Descrição:** Posiciona n rainhas sem conflitos no tabuleiro
- **Parâmetros:** T₀=100, α=0.995, 10000 iterações

## 🚀 Como Executar

### Requisitos
- Python 3.7 ou superior
- Sem dependências externas (usa apenas bibliotecas padrão)

### Executar Todos os Problemas
```bash
# Problema 1 - Mochila Binária
python 1_Mochila_Binaria/mochila_binaria.py

# Problema 2 - TSP
python 2_TSP_Roteamento/tsp_roteamento.py

# Problema 3 - Designação Generalizada
python 3_Designacao_Generalizada/designacao_generalizada.py

# Problema 4 - Empacotamento
python 4_Empacotamento_Unidimensional/empacotamento.py

# Problema 5 - Circuitos
python 5_Conexao_Circuitos/conexao_circuitos.py

# Problema 6 - n-Rainhas
python 6_N_Rainhas/n_rainhas.py
```

### Executar Tudo de Uma Vez (Windows PowerShell)
```powershell
Get-ChildItem -Recurse -Filter "*.py" | Where-Object { $_.Name -notlike "*common*" } | ForEach-Object { python $_.FullName }
```

## 📁 Estrutura do Projeto

```
OC/
├── 1_Mochila_Binaria/
│   ├── mochila_binaria.py
│   ├── entradas/          # 15 arquivos de entrada
│   └── saidas/            # Resultados gerados
├── 2_TSP_Roteamento/
│   ├── tsp_roteamento.py
│   ├── entradas/          # 15 arquivos de entrada
│   └── saidas/
├── 3_Designacao_Generalizada/
│   ├── designacao_generalizada.py
│   ├── entradas/          # 4 arquivos de entrada
│   └── saidas/
├── 4_Empacotamento_Unidimensional/
│   ├── empacotamento.py
│   ├── entradas/          # 5 arquivos de entrada
│   └── saidas/
├── 5_Conexao_Circuitos/
│   ├── conexao_circuitos.py
│   ├── entradas/          # 5 arquivos de entrada
│   └── saidas/
├── 6_N_Rainhas/
│   ├── n_rainhas.py
│   ├── entradas/          # 6 arquivos de entrada
│   └── saidas/
├── utils/
│   └── common.py          # Funções auxiliares
└── README.md
```

## 📚 Referências Bibliográficas

### Mochila Binária (Genetic Algorithm)
- Gitconnected: [Genetic Algorithm for Knapsack Problem](https://levelup.gitconnected.com/genetic-algorithm-for-knapsack-problem-e5ee69b5c8ab)
- GeeksforGeeks: [0/1 Knapsack using Genetic Algorithm](https://www.geeksforgeeks.org/0-1-knapsack-using-genetic-algorithm/)

### TSP (Simulated Annealing)
- Visual Studio Magazine: [Traveling Salesman Using Simulated Annealing with Python](https://visualstudiomagazine.com/articles/2021/12/01/traveling-salesman-using-simulated-annealing-with-python.aspx)
- GeeksforGeeks: [Simulated Annealing in AI](https://www.geeksforgeeks.org/simulated-annealing/)

### Designação Generalizada
- INFORMS PubsOnline: [Branch and Bound Algorithms for the Generalized Assignment Problem](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.24.9.919)
- Wikipedia: [Generalized Assignment Problem](https://en.wikipedia.org/wiki/Generalized_assignment_problem)

### Bin Packing (FFD)
- GeeksforGeeks: [Bin Packing Problem](https://www.geeksforgeeks.org/bin-packing-problem-minimize-number-of-used-bins/)
- Wikipedia: [Bin Packing Problem](https://en.wikipedia.org/wiki/Bin_packing_problem)

### Conexão de Circuitos & n-Rainhas (Simulated Annealing)
- GeeksforGeeks: [Simulated Annealing](https://www.geeksforgeeks.org/simulated-annealing/)
- Gettysburg College: [N-Queens Problem using Simulated Annealing](https://cs.gettysburg.edu/~tneller/nsf/clue/tp/index.html)

## ⚙️ Detalhes de Implementação

### Algoritmo Genético (Mochila)
- **Representação:** Cromossomo binário (0/1 para cada item)
- **Seleção:** Torneio (k=5)
- **Crossover:** Um ponto
- **Mutação:** Bit-flip
- **Elitismo:** Mantém melhor indivíduo

### Simulated Annealing (TSP, GAP, Circuitos, n-Rainhas)
- **Critério de Aceitação:** Metropolis (e^(-ΔE/T))
- **Operador de Vizinhança:** 
  - TSP: 2-opt swap
  - GAP: Trocar atribuição de módulo
  - Circuitos: Trocar conexão
  - n-Rainhas: Mover rainha
- **Resfriamento:** Geométrico (T = α * T)

### First Fit Decreasing (Empacotamento)
1. Ordena itens em ordem decrescente
2. Para cada item, coloca no primeiro recipiente que couber
3. Se não couber, cria novo recipiente
4. Aplica busca local para consolidar recipientes

## 📊 Formato de Saída

Todas as saídas seguem o padrão especificado:
```
{numero}_{problema}{identificador}_{valor}_saida.txt
```

Exemplos:
- `1_mochila10_105_saida.txt`
- `2_tsp25_1234_saida.txt`
- `3_pdg2_58_saida.txt`

## ✅ Conformidade com Especificações

- ✅ Implementação própria de métodos de otimização
- ✅ Sem uso de códigos prontos de repositórios
- ✅ Funções auxiliares permitidas (ordenação, I/O)
- ✅ Linguagem: Python
- ✅ Critério de parada: Número fixo de iterações
- ✅ Execução de todas as entradas fornecidas
- ✅ Evidência de execução (prints durante processamento)
- ✅ Saídas nomeadas conforme especificação

## 👥 Autores
João Gabriel e Vinicius Eduardo

---

**Observação:** Este projeto foi desenvolvido como parte do trabalho da disciplina de Otimização Combinatória, implementando algoritmos metaheurísticos para problemas NP-difíceis conforme as especificações fornecidas.
