# Projeto: Detecção de obstáculos presentes nas vias

## 📝 Descrição

Este projeto de iniciação científica foca no desenvolvimento de um **robô móvel 4WD** para a **identificação de obstáculos em vias urbanas**. O sistema é equipado com **ESP32** para controle e um **sensor inercial MPU6050**, que permite a navegação e a detecção de variações de movimento.

Através de **técnicas de processamento de dados**, o robô analisa informações do sensor para identificar desníveis, solavancos e outros obstáculos, demonstrando sua eficácia em um ambiente controlado. O projeto proporcionou vivência prática no desenvolvimento de soluções embarcadas, na análise de dados inerciais e nos desafios de navegação para veículos robóticos autônomos.

## ⚙️ Tecnologias e Ferramentas

* **Linguagens de Programação:**
    * `C++` (firmware do ESP32)
    * `Python` (para análise de dados ou back-end)
    * `HTML`, `CSS` e `JavaScript` (para a interface de controle web)
* **Hardware:**
    * Robô móvel **4WD**
    * Microcontrolador **ESP32**
    * Sensor Inercial **MPU6050** (Acelerômetro e Giroscópio)
* **Software:**
    * **Programação embarcada** e **Web Server** no ESP32.
    * Análise e **processamento de dados inerciais**.

---

## ✨ Destaques do Projeto

* **Vivência prática** no desenvolvimento de soluções embarcadas.
* **Testes em ambiente controlado** para validação da robustez do sistema.
* **Análise de dados inerciais** para identificar variações de movimento, como desníveis e solavancos.
* Experiência em aplicações para **veículos robóticos**.
---

## 🚀 Como Executar o Projeto

Siga estes passos para configurar e executar o projeto em sua máquina local.

### 📋 Pré-requisitos

Certifique-se de que você tem o seguinte software instalado:

* `Python <versão>`
* `pip` (gerenciador de pacotes do Python)

### 📦 Instalação

1.  Clone este repositório para sua máquina local:

    ```bash
    git clone [https://github.com/](https://github.com/)<seu-usuario>/<nome-do-repositorio>.git
    cd <nome-do-repositorio>
    ```

2.  Crie um ambiente virtual (recomendado):

    ```bash
    python -m venv venv
    ```

3.  Ative o ambiente virtual:

    * No Windows:

        ```bash
        venv\Scripts\activate
        ```

    * No macOS e Linux:

        ```bash
        source venv/bin/activate
        ```

4.  Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

### ▶️ Execução

Para iniciar o sistema de detecção de obstáculos:

```bash
python <caminho-para-o-arquivo-principal, ex: main.py> <opções-se-houver>
