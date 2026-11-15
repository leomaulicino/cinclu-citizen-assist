# cinclu — Citizen Assist AI | Módulo de Energias Renováveis e Sustentáveis (SERS)

> **"Uma cidade só é de todos quando todos conseguem chegar."**

Projeto desenvolvido para a **Global Solution 2026.2 — Ciência da Computação (Turma 1CCPQ)** da **FIAP**, referente à disciplina **Soluções em Energias Renováveis e Sustentáveis (SERS)**.

Este repositório documenta e implementa especificamente a **contribuição da disciplina de SERS** integrada ao assistente digital **cinclu (Citizen Assist AI)**, voltado à inclusão social, cidadania e apoio à população LGBT+ em situação de vulnerabilidade.

---

## Integrantes do Grupo (Turma 1CCPQ)

| Nome Completo | RM |
| :--- | :--- |
| **Enzo Posterlli Strinta** | `570035` |
| **Giovanna Tristão Lopes** | `572552` |
| **Leonardo Robert Maulicino** | `570329` |

---

## 1. Contexto, Público-Alvo e Problema Energético

* **Público Escolhido:** Cidadãos atendidos pelo ecossistema **cinclu** (com foco na comunidade LGBT+ e espaços comunitários/residências urbanas na região metropolitana de São Paulo/SP) que buscam reduzir despesas fixas mensais por meio do uso consciente de eletricidade.
* **Transparência Metodológica sobre Dados:** Órgãos oficiais do setor elétrico brasileiro (**ANEEL**, **EPE** e **IBGE**) **não coletam nem publicam** estatísticas de consumo energético (`kWh`) segmentadas por orientação sexual ou identidade de gênero. Nenhuma estatística fictícia foi criada neste projeto. O documento legislativo oficial mais próximo identificado é o **Projeto de Lei nº 1.182/2023** (Câmara dos Deputados), que propõe incluir abrigos e casas de acolhimento LGBTQIA+ na Tarifa Social de Energia Elétrica. Como o projeto ainda não é lei vigente, esse público permanece faturado na **tarifa residencial convencional (Subgrupo B1)**, tornando a gestão energética crítica para o orçamento doméstico e comunitário.
* **Necessidade Energética Abordada:** Redução do consumo elétrico residencial e avaliação técnico-econômica de alternativas de economia e geração renovável frente à tarifa convencional da Enel Distribuição São Paulo.
* **Contribuição do Citizen Assist AI:** O assistente traduz grandezas físicas e regulatórias (`W`, `kWh`, `HSP`, `CAPEX`, `OPEX`, `Payback`, regra do `Fio B` da Lei nº 14.300/2022) em orientações práticas, personalizadas conforme o tipo de moradia (imóvel alugado vs. imóvel próprio) e orçamento disponível.

---

## 2. Estrutura do Repositório e Funcionalidades (Contribuição SERS)

    cinclu-citizen-assist/
    ├── data/
    │   └── base_energetica_sers.json   # Base rastreável com dados oficiais, unidades, URLs e limitações
    ├── src/
    │   ├── __init__.py
    │   ├── sers_engine.py              # Motor físico e financeiro auditável + validação de entradas
    │   └── assistant_sers.py           # Lógica do Citizen Assist AI integrada aos resultados SERS
    ├── tests/
    │   ├── __init__.py
    │   └── test_sers.py                # Suíte automatizada de testes unitários e de integração
    ├── app.py                          # Interface web interativa em Python (Streamlit) com identidade cinclu
    ├── requirements.txt                # Dependências do projeto
    └── README.md                       # Documentação completa da contribuição de SERS

1. **Base Estruturada Rastreável (`data/base_energetica_sers.json`):** Armazena parâmetros oficiais, unidades de medida, classificações (`dado_publico_oficial`, `dado_publico_mercado`, `premissa_estimada`), links verificáveis e limitações técnicas.
2. **Motor de Cálculo Auditável (`src/sers_engine.py`):**
   * Decomposição física do consumo residencial médio oficial (`179,1 kWh/mês` — EPE) por equipamento (`E = P × t × d / 1000`).
   * Simulação da **Alternativa 1 (Eficiência Energética: LED + Gestão de Banho)**.
   * Simulação da **Alternativa 2 (Fonte Renovável: Microgeração Solar Fotovoltaica On-Grid)** considerando irradiação de São Paulo (`4,44 HSP`), taxa de desempenho (`75%`), custo de disponibilidade monofásico (`30 kWh`) e escalonamento de `60%` da TUSD Fio B em 2026 (Lei nº 14.300/2022).
   * Validação rigorosa de entradas e tratamento de erros.
3. **Assistente Conversacional Integrado (`src/assistant_sers.py`):** Responde dúvidas do cidadão com base nos cálculos executados, informa fontes verificáveis e exibe obrigatoriamente condições e limitações em todas as recomendações.
4. **Interface Web Interativa (`app.py`):** Aplicação em **Python + Streamlit** com a identidade visual do **cinclu**, controles dinâmicos de simulação e consulta ao assistente.

---

## 3. Como Executar e Testar a Solução

### Pré-requisitos
* Python 3.10 ou superior instalado.

### Passo a passo para execução local

1. Clone o repositório e acesse a pasta do projeto:

        git clone https://github.com/leomaulicino/cinclu-citizen-assist
        cd cinclu-citizen-assist

2. Instale a dependência necessária:

        pip install -r requirements.txt

3. Execute os testes técnicos automatizados (validação matemática e de integração):

        python tests/test_sers.py -v

4. Inicie a interface web do cinclu (Citizen Assist AI):

        streamlit run app.py

Após executar o último comando, a interface abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 4. Dados Utilizados, Premissas e Metodologia

| Variável | Valor | Unidade | Classificação | Origem / Fonte | Premissas e Limitações |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Consumo residencial médio** | `179,1` | `kWh/mês` | Dado Público Oficial | **EPE** — Anuário Estatístico de Energia Elétrica 2026 (`2.149,2 kWh/ano`) | Média nacional por unidade consumidora; varia conforme região e número de moradores. |
| **Tarifa Base (Subgrupo B1)** | `0,78938` | `R$/kWh` | Dado Público Oficial | **ANEEL / Enel SP** — REH nº 3.596/2026 (`TUSD R$ 0,47242 + TE R$ 0,31696`) | Tarifa homologada **sem tributos** (ICMS, PIS/COFINS e COSIP incidem conforme faixa). |
| **Custo de disponibilidade** | `30` (`R$ 23,68`) | `kWh/mês` | Dado Público Oficial | **ANEEL** — REN nº 1.000/2021 | Valor mínimo mensal faturável para ligação monofásica (`50 kWh` bifásico; `100 kWh` trifásico). |
| **Irradiação solar média (SP)** | `4,44` | `kWh/m².dia` | Dado Público Oficial | **CRESESB / CEPEL** — SunData v3.0 (São Paulo/SP, plano horizontal) | Média anual histórica (HSP); varia por inclinação, azimute e sombreamento. |
| **Custo sistema solar turnkey** | `3.620,00` | `R$/kWp` | Dado Público de Mercado | **Greener** — Estudo Estratégico GD (`R$ 3,62/Wp` até `2 kWp`) | Inclui equipamentos, projeto, instalação e homologação; varia por telhado. |
| **Fator de emissão SIN** | `0,04` | `kg CO₂/kWh` | Dado Público Oficial | **MCTI / EPE** — Fatores de Emissão do SIN (`0,04 tCO₂/MWh`) | Média anual da matriz elétrica brasileira. |
| **Horas diárias de uso** | `24 min/dia` (chuveiro) e `5 h/dia` (luz) | `h/dia` | Premissa Estimada | Modelagem com potências nominais **PROCEL/INMETRO** (`5.500 W` e `20 W`) | Premissas operacionais estimadas para decompor os `179,1 kWh/mês` da EPE. |
| **Taxa de desempenho solar** | `0,75` (`75%`) | Fração | Premissa Estimada | Engenharia Fotovoltaica | Considera perdas por temperatura, inversor, cabeamento e sujeira. |

---

## 5. Cálculos e Comparação das Alternativas (Mesma Demanda e Período)

### Fórmulas Aplicadas
* **Consumo de Energia Elétrica:** `E = (P × t × d) / 1.000` (`kWh/mês`, com `d = 30 dias`)
* **Geração Solar Fotovoltaica:** `Gs = P_kWp × HSP × d × η` (`kWh/mês`)

### Decomposição da Linha de Base (`179,1 kWh/mês` — EPE)
1. **Chuveiro Elétrico (`5.500 W`, `24 min/dia`):** `(5.500 × 0,40 × 30) / 1.000 = 66,00 kWh/mês`
2. **Geladeira 1 Porta (PROCEL/INMETRO):** `35,00 kWh/mês`
3. **Iluminação (`8 × 20 W = 160 W`, `5 h/dia`):** `(160 × 5,0 × 30) / 1.000 = 24,00 kWh/mês`
4. **Demais Equipamentos (saldo residual EPE):** `54,10 kWh/mês`
* **Fatura Base Mensal (sem impostos):** `179,1 × R$ 0,78938 = R$ 141,38/mês` (`R$ 1.696,54/ano`).

### Quadro Comparativo Técnico, Econômico e Ambiental

| Critério | Cenário Atual (Linha de Base) | Alternativa 1: Eficiência Energética (8 LED 9W + Banho 16 min/dia) | Alternativa 2: Fonte Renovável (Solar On-Grid `1,50 kWp`) |
| :--- | :--- | :--- | :--- |
| **Consumo / Geração Mensal** | Consumo: `179,10 kWh/mês` | Economia: `35,20 kWh/mês` (`-19,65%`) | Geração: `149,85 kWh/mês` (`83,67%` da carga) |
| **Fatura Mensal Estimada** | `R$ 141,38 / mês` | `R$ 113,59 / mês` | `~R$ 39,68 / mês` (mínimo `30 kWh` + Fio B) |
| **Investimento Inicial (CAPEX)** | `R$ 0,00` | `R$ 80,00` (estimado) | `R$ 5.430,00` (base Greener) |
| **Custo Operacional (OPEX)** | `R$ 0,00 / ano` | `R$ 0,00 / ano` | `R$ 150,00 / ano` (limpeza/manutenção estimada) |
| **Economia Líquida Anual** | `R$ 0,00 / ano` | `R$ 333,43 / ano` | `R$ 1.070,40 / ano` (descontando OPEX) |
| **Payback Simples Estimado** | Não se aplica | **`2,88 meses`** | **`5,07 anos`** |
| **Custo Acumulado (5 anos)** | `R$ 8.482,68` | **`R$ 6.895,51`** (melhor curto prazo) | `R$ 8.560,80` (ponto de equilíbrio no ano 5) |
| **Custo Acumulado (10 anos)** | `R$ 16.965,35` | `R$ 13.711,02` | **`R$ 11.691,60`** (melhor longo prazo) |
| **CO₂ Evitado (Anual)** | `0,00 kg CO₂/ano` | `16,90 kg CO₂/ano` | **`71,93 kg CO₂/ano`** |

### Justificativa das Recomendações
* **Imóveis alugados, apartamentos ou orçamento inicial restrito:** A **Alternativa 1 (Eficiência Energética)** é recomendada por exigir investimento estimado de apenas `R$ 80,00`, não depender de reformas ou autorização estrutural e apresentar retorno em menos de 3 meses.
* **Imóveis próprios com telhado sem sombreamento e horizonte acima de 5 anos:** A **Alternativa 2 (Solar Fotovoltaica On-Grid)** oferece o maior ganho ambiental (`4,25×` mais CO₂ evitado) e a maior economia financeira acumulada em 10 anos, sendo recomendada em conjunto com a redução prévia de desperdícios.
* **Limitações:** Nenhuma economia ou prazo de retorno é garantido. Os resultados reais dependem das alíquotas tributárias aplicadas na fatura, disciplina de uso, orientação/sombreamento do telhado e regras regulatórias da Lei nº 14.300/2022.

---

## 6. Testes Técnicos e Testes com Usuários

### Testes Técnicos Automatizados (`tests/test_sers.py`)
Validados via `unittest` (`5/5 testes aprovados`):
* Conferência exata da decomposição de `179,1 kWh/mês` e fatura base (`R$ 141,38`).
* Conferência matemática da Alternativa 1 (economia de `35,2 kWh/mês`, payback `2,88 meses`) e Alternativa 2 (geração de `149,85 kWh/mês`, fatura residual `R$ 39,68`, payback `5,07 anos`).
* Rejeição de entradas inválidas (potência negativa, horas > 24, tarifa nula).
* Presença obrigatória de fontes verificáveis e avisos de limitações em todas as respostas do assistente.

### Testes com Usuários (Roteiro Estruturado)

| Participante | Situação Testada | Comentários Recebidos | Dificuldades Identificadas | Ajustes Realizados |
| :--- | :--- | :--- | :--- | :--- |
| **Participante 01** *(Perfil: Inquilino / Orçamento Restrito)* | Simulação da Alternativa 1 (Eficiência Energética) e perguntas ao assistente. | *"Achei bem fácil de mexer. Como moro de aluguel, ver que consigo abaixar quase 20% da minha conta só trocando as lâmpadas e controlando o tempo do banho, sem precisar mexer em estrutura nenhuma, me deu uma luz enorme de economia."* | Nenhuma dificuldade relatada; achou os controles de minutos de banho diretos e práticos. | Validação positiva da proposta focada em inquilinos; nenhum ajuste estrutural necessário. |
| **Participante 02** *(Perfil: Morador avaliando energia solar futura)* | Simulação da Instalação Solar Futura e comparação de custos acumulados em 5 e 10 anos. | *"Gostei de ver a simulação das placas no telhado e o cálculo de quanto tempo o investimento demora para se pagar. É bem legal ver que, embora no começo a solar seja cara, a longo prazo ela realmente compensa na conta de luz."* | Inicialmente achou que os valores da fatura já vinham com todos os impostos estaduais embutidos. | Inclusão de notas explicativas mais claras reforçando que a tarifa base é da Enel SP sem tributos (REH 3.596/2026). |

---

## 7. Referências Verificáveis

1. **ANEEL / Enel Distribuição São Paulo** — *Resolução Homologatória nº 3.596/2026 (Tarifas Grupo B1 vigentes)*: https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html
2. **ANEEL** — *Resolução Normativa nº 1.000/2021 (Regras de Prestação do Serviço Público de Distribuição)*: https://www2.aneel.gov.br/cedoc/ren20211000.html
3. **Brasil — Lei nº 14.300, de 6 de janeiro de 2022** — *Marco Legal da Microgeração e Minigeração Distribuída (Art. 27 — Fio B)*: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm
4. **EPE (Empresa de Pesquisa Energética)** — *Anuário Estatístico de Energia Elétrica 2026 (Sumário Executivo)*: https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-160/topico-168/Anuario_Sumario%20Executivo_2026_V1.pdf
5. **CRESESB / CEPEL** — *Sistema SunData v3.0 (Potencial Solar — São Paulo/SP)*: https://cresesb.cepel.br/index.php?section=sundata
6. **PROCEL / Eletrobras & INMETRO** — *Tabelas de Consumo e Eficiência Energética (PBE)*: https://www.gov.br/inmetro/pt-br/assuntos/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica
7. **MCTI (Ministério da Ciência, Tecnologia e Inovação)** — *Fatores de Emissão de CO₂ do Sistema Interligado Nacional (SIN)*: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
8. **Câmara dos Deputados** — *Projeto de Lei nº 1.182/2023 (Inclusão de abrigos e casas de acolhimento LGBTQIA+ na Tarifa Social)*: https://www.camara.leg.br/proposicoesWeb/prop_mostrarintegra?codteor=3018324