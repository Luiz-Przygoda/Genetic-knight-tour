# O Problema do Passeio do Cavalo
![Logo do projeto](https://github.com/Luiz-Przygoda/Genetic-knight-tour/blob/main/imgs/knights%20tour%20logo.png)
Uma Análise Comparativa com Algoritmo Genético fundamentada em Python.

## Introdução

Este projeto apresenta uma ferramenta visual e interativa para explorar e resolver o clássico problema do **Passeio do Cavalo**. A aplicação não apenas encontra soluções, mas também serve como uma plataforma de demonstração para comparar diferentes abordagens algorítmicas, com foco especial em uma implementação robusta de **Algoritmo Genético**.

Desenvolvido para fins acadêmicos, este software oferece uma interface gráfica moderna e funcionalidades didáticas para facilitar a compreensão de conceitos complexos de algoritmos e inteligência artificial.

[video-demo.webm](https://github.com/user-attachments/assets/357795b5-6250-4028-b8ee-baf4080281f4)

---

## Sobre o Projeto

O projeto aborda o problema do Passeio do Cavalo, que busca um caminho onde o cavalo visite todas as casas do tabuleiro uma única vez. Um caso clássico de caminho hamiltoniano.
São exploradas três abordagens:

1. **Warnsdorff:** heurística gulosa que prioriza casas com menos movimentos futuros, rápida mas sem garantia de solução;

2. **Backtracking:** método exaustivo que sempre encontra solução, porém com alto custo computacional;

3. **Algoritmo Genético:** foco principal do projeto, inspirado na seleção natural, evolui uma população de soluções por meio de seleção, cruzamento e mutação até atingir resultados ótimos ou próximos do ótimo.

A interface gráfica interativa permite visualizar e comparar o desempenho dos algoritmos em tempo real, com foco didático e experimental.

## Funcionalidades Principais

O projeto implementa três métodos para resolver o Passeio do Cavalo — Warnsdorff, Backtracking e Algoritmo Genético — em uma interface moderna e interativa feita com Tkinter e o tema sv-ttk.
O sistema inclui:

* **Tabuleiro dinâmico em tela cheia**, com redimensionamento automático;

* **Animação passo a passo** com opção de pausar e retomar;

* **Controle total do Algoritmo Genético**, permitindo acompanhar sua evolução em tempo real por meio de um gráfico integrado (matplotlib);

* **Visualização didática da heurística de Warnsdorff**, mostrando os graus de movimento ao passar o mouse;

* **Barra de status informativa**, exibindo dados como geração, aptidão e tempo de execução.
  

## Tecnologias Utilizadas

* **Python 3**
* **Tkinter:** Para a construção da interface gráfica.
* **Matplotlib:** Para a plotagem do gráfico de evolução do GA.
* **sv-ttk:** Para aplicar o tema moderno "Sun Valley" à interface.


## Como Executar

Siga os passos abaixo para executar o projeto em sua máquina local.

### Pré-requisitos

* Python 3.8 ou superior instalado.
* `pip` (gerenciador de pacotes do Python) disponível no seu terminal.

### Passos de Instalação

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone https://github.com/Luiz-Przygoda/Genetic-knight-tour
    cd Genetic-knight-tour
    ```

2.  **Instale as dependências necessárias:**
    ```bash
    pip install matplotlib sv-ttk
    ```

3.  **Execute o programa:**
    ```bash
    python knight_tour_gui1.py
    ```


## **Colaboradores**
| [<img src="https://avatars.githubusercontent.com/u/142179999?v=4" width="115">](https://github.com/Luiz-Przygoda) | [<img src="https://avatars.githubusercontent.com/u/113839563?v=4" width="115">](https://github.com/Wyllye) | [<img src="https://avatars.githubusercontent.com/u/125486974?v=4" width="115">](https://github.com/mariaglx) | [<img src="https://avatars.githubusercontent.com/u/75136675?v=4" width="115">](https://github.com/marcobgh)|
|:--------------------------------------------------------------------------:|:-----------------------------------------------------------------------:|:-----------------------------------------------------------------------:|:--------------------------------------------------------------------:|
| **Luiz-Przygoda**                                                              | **Wyllye**                                                               | **Mariaglx**                                                           | **Marcobgh**                                                              |
