# Passeio do Cavalo: Uma Análise Comparativa com Algoritmo Genético
---
![Logo do projeto](https://github.com/Luiz-Przygoda/Genetic-knight-tour/blob/main/imgs/knights%20tour%20logo.png)
Uma Análise Comparativa com Algoritmo Genético fundamentada em Python.

## Introdução

Este projeto apresenta uma ferramenta visual e interativa para explorar e resolver o clássico problema do **Passeio do Cavalo**. A aplicação não apenas encontra soluções, mas também serve como uma plataforma de demonstração para comparar diferentes abordagens algorítmicas, com foco especial em uma implementação robusta de **Algoritmo Genético**.

Desenvolvido para fins acadêmicos, este software oferece uma interface gráfica moderna e funcionalidades didáticas para facilitar a compreensão de conceitos complexos de algoritmos e inteligência artificial.

---

## Sobre o Projeto

O Passeio do Cavalo é um problema matemático que consiste em encontrar um caminho para uma peça de cavalo em um tabuleiro de xadrez, de forma que ela visite cada casa exatamente uma vez. Este é um exemplo clássico de um problema de busca de caminho hamiltoniano, conhecido por sua complexidade combinatória.

Este projeto explora três métodos distintos para resolver o problema:

1.  **Heurística de Warnsdorff:** Uma abordagem gulosa (greedy) e muito eficiente. A regra instrui o cavalo a se mover para a casa que tem o menor número de saídas válidas futuras, evitando que fique preso em cantos do tabuleiro. É extremamente rápido, mas não garante uma solução em todos os casos.
2.  **Backtracking:** Um algoritmo de força bruta que testa exaustivamente todas as possibilidades de caminho. Embora garanta encontrar uma solução se ela existir, seu custo computacional é muito alto, tornando-o inviável para tabuleiros maiores ou em tempo real.
3.  **Algoritmo Genético (GA):** A abordagem central deste trabalho. O GA é uma meta-heurística inspirada no processo de seleção natural de Darwin. Ele trabalha com uma "população" de soluções candidatas (passeios) que evoluem ao longo de gerações através de operadores genéticos como seleção, cruzamento (crossover) e mutação, convergindo para uma solução ótima ou próxima da ótima.

A interface gráfica foi projetada para ser uma ferramenta de ensino, permitindo ao usuário visualizar, controlar e comparar o desempenho desses algoritmos em tempo real.

---

## ✨ Funcionalidades Principais

O projeto implementa três métodos para resolver o Passeio do Cavalo — Warnsdorff, Backtracking e Algoritmo Genético — em uma interface moderna e interativa feita com Tkinter e o tema sv-ttk.
O sistema inclui:

* **Tabuleiro dinâmico em tela cheia**, com redimensionamento automático;

* **Animação passo a passo** com opção de pausar e retomar;

* **Controle total do Algoritmo Genético**, permitindo acompanhar sua evolução em tempo real por meio de um gráfico integrado (matplotlib);

* **Visualização didática da heurística de Warnsdorff**, mostrando os graus de movimento ao passar o mouse;

* **Barra de status informativa**, exibindo dados como geração, aptidão e tempo de execução.
  
---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Tkinter:** Para a construção da interface gráfica.
* **Matplotlib:** Para a plotagem do gráfico de evolução do GA.
* **sv-ttk:** Para aplicar o tema moderno "Sun Valley" à interface.

---

## 🚀 Como Executar

Siga os passos abaixo para executar o projeto em sua máquina local.

### Pré-requisitos

* Python 3.8 ou superior instalado.
* `pip` (gerenciador de pacotes do Python) disponível no seu terminal.

### Passos de Instalação

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Instale as dependências necessárias:**
    ```bash
    pip install matplotlib sv-ttk
    ```

3.  **Execute o programa:**
    ```bash
    python nome_do_seu_arquivo.py
    ```
    *(Substitua `nome_do_seu_arquivo.py` pelo nome do seu script principal, por exemplo, `knight_tour_gui_presentation_final.py`)*

---

## 🎓 Fundamentação Teórica

A implementação dos algoritmos neste trabalho foi baseada em metodologias e análises encontradas na literatura acadêmica. As principais referências que guiaram o desenvolvimento foram:

* **Para o Algoritmo Genético:**
    * Herath, H. K. E. H. S. B., de Silva, C. V. S. S. S., & Bandara, P. M. R. M. (2012). **An efficient genetic algorithm for the knight's tour problem**. *2012 International Conference on Advances in ICT for Emerging Regions (ICTer)*.
    * *Este artigo foi fundamental para a modelagem da solução, utilizando uma representação por permutação e operadores genéticos (crossover e mutação) adequados para o problema.*

---

## 👨‍💻 Autores

* Luiz Gustavo Przygoda
* Marco Antônio Borghetti
* Maria Isabel Wirth Marafon
* Vinicius Andrei Wille
