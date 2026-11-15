import math
import streamlit as st
from src.assistant_sers import responder_assistente_sers
from src.sers_engine import (
    calcular_linha_base,
    carregar_base_energetica,
    recomendar_por_perfil,
    simular_eficiencia_energetica,
    simular_solar_ongrid,
)

st.set_page_config(
    page_title="cinclu — Citizen Assist AI | Energia & Sustentabilidade (SERS)",
    layout="wide",
)

base_json = carregar_base_energetica()
params = base_json["parametros_oficiais"]

st.markdown(
    """
    <style>
        .cinclu-header {
            background: #F6F5FA;
            padding: 1.4rem 1.8rem;
            border-radius: 16px;
            margin-bottom: 1.2rem;
            border: 1px solid #EAE6F5;
        }
        .cinclu-logo-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.45rem;
        }
        .cinclu-brand {
            font-size: 2.25rem;
            font-weight: 800;
            color: #1A0B3B;
            letter-spacing: -0.035em;
            line-height: 1;
        }
        .cinclu-slogan {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1A0B3B;
            margin: 0;
        }
        .cinclu-sub {
            color: #4A4458;
            margin-top: 0.35rem;
            margin-bottom: 0;
            font-size: 0.94rem;
        }
        .pride-bar {
            height: 6px;
            border-radius: 999px;
            margin-top: 0.95rem;
            background: linear-gradient(
                90deg,
                #F46A6A 0%,
                #F89B4B 20%,
                #F8D347 40%,
                #52C98A 60%,
                #2CC5E9 80%,
                #7A63F5 100%
            );
        }
    </style>
    <div class="cinclu-header">
        <div class="cinclu-logo-row">
            <svg width="42" height="42" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="cincluArcGrad" x1="28" y1="6" x2="26" y2="34" gradientUnits="userSpaceOnUse">
                        <stop offset="0%" stop-color="#28C7FA"/>
                        <stop offset="28%" stop-color="#B8E942"/>
                        <stop offset="54%" stop-color="#FF914D"/>
                        <stop offset="78%" stop-color="#F84F86"/>
                        <stop offset="100%" stop-color="#7B61FF"/>
                    </linearGradient>
                </defs>
                <path d="M28.5 10.5A12.5 12.5 0 1 0 28.5 29.5" stroke="url(#cincluArcGrad)" stroke-width="5.2" stroke-linecap="round"/>
                <circle cx="24.2" cy="20" r="2.7" fill="#1A0B3B"/>
            </svg>
            <span class="cinclu-brand">cinclu</span>
        </div>
        <p class="cinclu-slogan">Uma cidade só é de todos quando todos conseguem chegar.</p>
        <p class="cinclu-sub">
            <strong>Módulo SERS — Soluções em Energias Renováveis e Sustentáveis</strong> | FIAP Global Solution 2026.2 (Turma 1CCPQ)
        </p>
        <div class="pride-bar"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("1. Sua Rotina Atual")
    st.caption("Informe apenas o que você já usa hoje. Valores padrão baseados na média oficial EPE (179,1 kWh/mês).")
    minutos_banho = st.slider(
        "Soma de banho elétrico por dia na casa (min/dia)",
        min_value=5,
        max_value=60,
        value=24,
        help="Some os minutos de banho de todas as pessoas da casa no dia. Ex.: 2 pessoas x 12 min = 24 min/dia.",
    )
    qtd_lampadas = st.number_input(
        "Quantidade de lâmpadas na casa",
        min_value=1,
        max_value=50,
        value=8,
    )

    st.divider()
    st.subheader("2. Meta de Economia (Alt. 1)")
    reducao_banho = st.slider(
        "Quantos minutos/dia você consegue reduzir no banho?",
        min_value=0,
        max_value=minutos_banho,
        value=min(8, minutos_banho),
        help="Ex.: cortar 4 minutos do banho de duas pessoas reduz 8 min/dia.",
    )
    minutos_banho_otim = max(0, minutos_banho - reducao_banho)
    st.caption(f"Meta: cair de **{minutos_banho} min** para **{minutos_banho_otim} min/dia** (+ troca para LED).")

    st.divider()
    st.subheader("3. Sua Moradia e Orçamento")
    imovel_proprio = st.checkbox("Moro em imóvel próprio", value=False)
    telhado_viavel = st.checkbox("Tenho telhado livre sem sombra", value=False)
    orcamento = st.number_input(
        "Quanto posso investir agora (R$)",
        min_value=0.0,
        max_value=50000.0,
        value=200.0,
        step=50.0,
    )

# 1. Calcula o cenário atual primeiro
linha_base = calcular_linha_base(
    minutos_banho_dia=float(minutos_banho),
    qtd_lampadas=int(qtd_lampadas),
    tarifa_brl_kwh=params["tarifa_base_b1_brl_kwh"]["valor"],
    fator_co2_kg_kwh=params["fator_emissao_sin_kg_kwh"]["valor"],
)

# 2. Dimensiona automaticamente o projeto solar futuro ideal para o consumo atual
geracao_por_kwp_mes = params["irradiacao_solar_sp_hsp"]["valor"] * 30.0 * params["taxa_desempenho_solar"]["valor"]
consumo_compensavel = max(0.0, linha_base["consumo_mensal_kwh"] - params["custo_disponibilidade_monofasico_kwh"]["valor"])
kwp_sugerido = consumo_compensavel / geracao_por_kwp_mes
placas_sugeridas = max(1, min(10, math.ceil(kwp_sugerido / 0.50)))

with st.sidebar:
    with st.expander("Simulação Solar Futura (Avançado — Opcional)"):
        st.caption(
            f"Com base no seu consumo de **{linha_base['consumo_mensal_kwh']} kWh/mês**, "
            f"o sistema dimensionou automaticamente **{placas_sugeridas} placas solares** para uma eventual instalação futura."
        )
        qtd_placas_solares = st.slider(
            "Simular quantidade de placas (500 W cada)",
            min_value=1,
            max_value=10,
            value=placas_sugeridas,
        )

potencia_solar = round(qtd_placas_solares * 0.50, 2)

alt1 = simular_eficiencia_energetica(
    linha_base=linha_base,
    minutos_banho_otimizado=float(minutos_banho_otim),
    qtd_lampadas=int(qtd_lampadas),
    tarifa_brl_kwh=params["tarifa_base_b1_brl_kwh"]["valor"],
    fator_co2_kg_kwh=params["fator_emissao_sin_kg_kwh"]["valor"],
)
alt2 = simular_solar_ongrid(
    linha_base=linha_base,
    potencia_sistema_kwp=float(potencia_solar),
    hsp_diario=params["irradiacao_solar_sp_hsp"]["valor"],
    taxa_desempenho=params["taxa_desempenho_solar"]["valor"],
    custo_kwp_brl=params["custo_kwp_turnkey_brl"]["valor"],
    tarifa_brl_kwh=params["tarifa_base_b1_brl_kwh"]["valor"],
    disponibilidade_kwh=params["custo_disponibilidade_monofasico_kwh"]["valor"],
    tusd_fio_b_brl_kwh=params["tusd_fio_b_referencia_brl_kwh"]["valor"],
    percentual_fio_b=params["percentual_fio_b_2026"]["valor"],
    fator_co2_kg_kwh=params["fator_emissao_sin_kg_kwh"]["valor"],
)

st.subheader("1. Comparação Técnica, Econômica e Ambiental (Mesma Demanda)")
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("#### Cenário Atual (Linha de Base)")
        st.metric("Consumo Mensal", f"{linha_base['consumo_mensal_kwh']} kWh/mês")
        st.metric("Fatura Base Estimada", f"R$ {linha_base['custo_mensal_brl']:.2f}/mês")
        st.write(f"**Emissão Anual:** {linha_base['emissao_anual_co2_kg']} kg CO₂/ano")
        st.caption("Tarifa base Enel SP B1 sem impostos (REH 3.596/2026).")

with col2:
    with st.container(border=True):
        st.markdown("#### Alternativa 1: Eficiência Energética")
        st.metric("Economia Mensal", f"{alt1['economia_mensal_kwh']} kWh/mês", f"-{alt1['percentual_reducao']}%")
        st.metric("Nova Fatura Estimada", f"R$ {alt1['nova_fatura_mensal_brl']:.2f}/mês", f"-R$ {alt1['economia_mensal_brl']:.2f}")
        st.write(f"**Investimento (CAPEX):** R$ {alt1['capex_brl']:.2f}")
        st.write(f"**Retorno (Payback):** {alt1['payback_meses']} meses")
        st.write(f"**CO₂ Evitado:** {alt1['co2_evitado_anual_kg']} kg/ano")

with col3:
    with st.container(border=True):
        st.markdown("#### Alternativa 2: Instalação Solar Futura")
        st.metric("Geração Solar Estimada", f"{alt2['geracao_mensal_kwh']} kWh/mês", f"{alt2['percentual_cobertura']}% da carga")
        st.metric("Fatura Residual Estimada", f"~R$ {alt2['fatura_residual_mensal_brl']:.2f}/mês")
        st.write(f"**Projeto Dimensionado:** {qtd_placas_solares} placas ({potencia_solar:.2f} kWp)")
        st.write(f"**Investimento (CAPEX):** R$ {alt2['capex_brl']:.2f}")
        st.write(f"**Retorno (Payback):** {alt2['payback_anos']} anos")
        st.write(f"**CO₂ Evitado:** {alt2['co2_evitado_anual_kg']} kg/ano")

rec = recomendar_por_perfil(imovel_proprio, telhado_viavel, orcamento, alt2['capex_brl'])
st.info(f"**Recomendação Personalizada para o Perfil Selecionado:** {rec['escolha']} — {rec['justificativa']}")

st.divider()
st.subheader("2. Citizen Assist AI — Consulte o Assistente Energético")

c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
pergunta_selecionada = ""
if c_btn1.button("Moro de aluguel: qual escolher?"):
    pergunta_selecionada = "Moro em imóvel alugado, qual alternativa escolher?"
if c_btn2.button("Como funciona a energia solar?"):
    pergunta_selecionada = "Explique a alternativa de energia solar renovável"
if c_btn3.button("Compare as duas alternativas"):
    pergunta_selecionada = "Compare as duas alternativas"
if c_btn4.button("Transparência sobre dados LGBT+"):
    pergunta_selecionada = "Qual a relação com dados LGBT+ e Tarifa Social?"

pergunta_usuario = st.text_input(
    "Digite sua dúvida sobre consumo, economia, energia solar ou fontes:",
    value=pergunta_selecionada,
    placeholder="Ex.: Quanto economizo trocando lâmpadas e reduzindo o banho?",
)

if pergunta_usuario:
    st.markdown(responder_assistente_sers(pergunta_usuario, linha_base, alt1, alt2))

with st.expander("3. Fontes Verificáveis, Premissas e Limitações (Auditoria Técnica)"):
    st.warning(base_json["metadados_projeto"]["transparencia_recorte_lgbt"])
    for chave, info in params.items():
        st.markdown(
            f"- **{chave}** (`{info['classificacao']}`): **{info['valor']} {info['unidade']}** — "
            f"{info['fonte']} ([Link oficial]({info['url']})). *Limitação:* {info['limitacao']}"
        )

st.caption("Integrantes (Turma 1CCPQ): Enzo Posterlli Strinta (RM 570035) | Giovanna Tristão Lopes (RM 572552) | Leonardo Robert Maulicino (RM 570329)")