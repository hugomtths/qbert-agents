# Q*bert Agents
### Comparativo de Paradigmas de Inteligência Artificial aplicados ao jogo Q*bert

> Projeto desenvolvido como requisito do Estudo Dirigido da disciplina de Inteligência Artificial (2026.1) do Bacharelado em Ciência da Computação da Universidade Federal do Agreste de Pernambuco (UFAPE), ministrada pelo Prof. Dr. Luis Filipe.

O estudo tem como objetivo implementar, analisar e demonstrar diferentes paradigmas de agentes inteligentes, relacionando as decisões de projeto, os métodos de treinamento e os resultados obtidos aos conceitos estudados na disciplina.

---

# Sobre o Projeto

Este projeto apresenta um estudo comparativo entre três paradigmas clássicos da Inteligência Artificial aplicados ao clássico jogo Q*bert, desenvolvido em Python utilizando a biblioteca Pygame.

O objetivo do agente é percorrer toda a pirâmide isométrica do jogo, fazendo com que cada bloco mude de cor (pinte toda a malha), realizando o menor número possível de movimentos e evitando cair no abismo.

Além da versão tradicional do problema, foi implementado um ambiente dinâmico contendo um inimigo inteligente (Cobra Coily), tornando necessária a tomada de decisões em tempo real.

---

# Modos de Jogo

O ambiente possui dois cenários distintos.

### Modo Estático (Sem Inimigos)

Neste modo o ambiente é completamente determinístico. O único objetivo do agente é encontrar a melhor sequência possível de movimentos para pintar toda a pirâmide utilizando o menor número de passos.



### Modo Dinâmico (Com Inimigos)

Neste cenário surge Coily, a cobra clássica do Q*bert. Inicialmente ela nasce como uma bola roxa e, após alguns movimentos, choca e passa a perseguir continuamente o agente. Agora o problema deixa de ser apenas encontrar um caminho ótimo. O agente precisa pintar os blocos, evitar colisões, recalcular estratégias constantemente e sobreviver enquanto conclui o objetivo.

---

# Agentes Implementados

- Agente baseado em estado, objetivo e busca heurística (Algoritmo A*);
- Agente que aprende por meio de aprendizado por reforço (Q-Learning);
- Agente que aprende por meio de algoritmo genético.

---

# Comparativo dos Agentes

| Agente | Paradigma | Modo Estático | Modo Dinâmico |
|---------|-----------|---------------|---------------|
| **Busca Heurística (A\*)** | Busca informada | Encontra a rota ótima com mínimo custo | Recalcula continuamente para evitar a cobra Coily |
| **Algoritmo Genético** | Computação Evolutiva | Evolui boas sequências rapidamente |Demonstra limitações em ambientes dinâmicos |
| **Q-Learning** | Aprendizado por Reforço | Aprende uma política eficiente após treinamento | Melhor adaptação ao ambiente dinâmico, reagindo naturalmente ao comportamento da cobra |

---

# Instalação e Execução

## Pré-requisitos

- Python 3.8 ou superior

---

### 1. Clone o repositório

```bash
git clone https://github.com/hugomtths/qbert-agents.git
```

Entre na pasta do projeto:

```bash
cd qbert_agents
```

---

### 2. Crie um ambiente virtual

### Windows

```bash
python -m venv venv
```

Ative:

```bash
venv\Scripts\activate
```

---

### Linux / macOS

```bash
python3 -m venv venv
```

Ative:

```bash
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Execute o projeto

```bash
python jogo_qbert.py
```
---

# Tecnologias Utilizadas

- Python
- Pygame
- Algoritmo A*
- Algoritmos Genéticos
- Q-Learning

---

# Contribuidores

* **[Hugo Matheus Costa Araújo](https://github.com/hugomtths)**
* **[Luís Henrique Domingos da Silva](https://github.com/LuisH07)**