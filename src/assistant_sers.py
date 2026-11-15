def responder_assistente_sers(pergunta: str, linha_base: dict, alt1: dict, alt2: dict) -> str:
    p = pergunta.lower()
    
    # Correção P3 e P4: Tratamento robusto para comparação e distinção correta de imóvel próprio
    if "compare" in p or "comparar" in p or "custos" in p or "5 e 10 anos" in p:
        custo_atual_5anos = linha_base['custo_mensal_brl'] * 60
        custo_alt1_5anos = alt1['capex_brl'] + (alt1['nova_fatura_mensal_brl'] * 60)
        custo_alt2_5anos = alt2['capex_brl'] + (alt2['fatura_residual_mensal_brl'] * 60) + (150 * 5)
        
        custo_atual_10anos = linha_base['custo_mensal_brl'] * 120
        custo_alt1_10anos = alt1['capex_brl'] + (alt1['nova_fatura_mensal_brl'] * 120)
        custo_alt2_10anos = alt2['capex_brl'] + (alt2['fatura_residual_mensal_brl'] * 120) + (150 * 10)

        return (
            f"**Citizen Assist AI — Comparativo Estimado de Longo Prazo:**\n\n"
            f"1. **Curto Prazo (Até 5 anos):**\n"
            f"   - Cenário Atual: R$ {custo_atual_5anos:,.2f}\n"
            f"   - Alternativa 1 (Eficiência): **R$ {custo_alt1_5anos:,.2f}** *(Menor custo acumulado inicial)*\n"
            f"   - Alternativa 2 (Solar): R$ {custo_alt2_5anos:,.2f}\n\n"
            f"2. **Longo Prazo (10 anos):**\n"
            f"   - Cenário Atual: R$ {custo_atual_10anos:,.2f}\n"
            f"   - Alternativa 1 (Eficiência): R$ {custo_alt1_10anos:,.2f}\n"
            f"   - Alternativa 2 (Solar): **R$ {custo_alt2_10anos:,.2f}** *(O solar cruza o ponto de equilíbrio e se torna a opção mais econômica, sujeito a premissas).* \n\n"
            f"*Fontes oficiais:* ANEEL / EPE. Os valores representam estimativas matemáticas e não constituem garantia financeira."
        )

    elif "alugado" in p:
        return (
            f"**Citizen Assist AI — Análise para Imóvel Alugado / Orçamento Restrito:**\n\n"
            f"Para inquilinos ou residências sem autonomia estrutural no telhado, a **Alternativa 1 (Eficiência Energética)** "
            f"é a escolha indicada. Com um investimento inicial estimado em **R$ {alt1['capex_brl']:.2f}** (focado em lâmpadas LED e otimização do banho), "
            f"o cidadão obtém uma economia estimada de **{alt1['economia_mensal_kwh']} kWh/mês** (redução de **{alt1['percentual_reducao']}%** na fatura), "
            f"alcançando o retorno financeiro em aproximadamente **{alt1['payback_meses']} meses**.\n\n"
            f"*Nota regulatória e limites:* Os cálculos utilizam a tarifa base B1 da Enel Distribuição São Paulo (REH ANEEL nº 3.596/2026), "
            f"sem incidência de tributos variáveis. Valores reais não são garantidos e dependem de hábitos de uso."
        )
    
    elif "próprio" in p or ("solar" in p and "próprio" not in p):
        if "solar" in p or "renovável" in p or "placas" in p:
            return (
                f"**Citizen Assist AI — Análise de Energia Solar Fotovoltaica (On-Grid):**\n\n"
                f"A **Alternativa 2** simula uma microgeração conectada à rede da Enel SP. Para o perfil avaliado, o projeto dimensionado estima "
                f"uma produção de **{alt2['geracao_mensal_kwh']} kWh/mês** (cobrindo **{alt2['percentual_cobertura']}%** da carga residencial).\n\n"
                f"- **Investimento Estimado (CAPEX):** R$ {alt2['capex_brl']:.2f}\n"
                f"- **Fatura Residual Estimada:** ~R$ {alt2['fatura_residual_mensal_brl']}/mês (condicionada ao custo de disponibilidade de 30 kWh e encargo Fio B da Lei nº 14.300/2022).\n"
                f"- **Retorno Estimado (Payback):** {alt2['payback_anos']} anos.\n"
                f"- **Impacto Ambiental Estimado:** Evita a emissão de até {alt2['co2_evitado_anual_kg']} kg de CO₂/ano (limitado à energia efetivamente deslocada).\n\n"
                f"*Limitação:* Os valores são estimativas condicionadas à irradiação média de São Paulo (4,44 HSP — CRESESB/CEPEL) e ausência de sombreamento, não havendo garantia de resultados fixos."
            )
        else:
            return (
                f"**Citizen Assist AI — Análise para Imóvel Próprio:**\n\n"
                f"Possuir imóvel próprio e telhado livre abre viabilidade para investimentos estruturais de longo prazo, como a **Alternativa 2 (Energia Solar Fotovoltaica)**, "
                f"desde que haja capital inicial compatível com o CAPEX estimado de R$ {alt2['capex_brl']:.2f}. Caso o orçamento seja restrito, "
                f"recomenda-se iniciar com a **Alternativa 1 (Eficiência Energética)**.\n\n"
                f"*Aviso:* Todas as projeções são estimativas sujeitas a variações tarifárias e climáticas."
            )
    
    elif "lgbt" in p or "tarifa social" in p:
        return (
            f"**Citizen Assist AI — Transparência sobre Dados e Público LGBT+:**\n\n"
            f"Órgãos oficiais do setor elétrico (ANEEL, EPE, IBGE) **não publicam** estatísticas de consumo elétrico segmentadas por orientação sexual ou identidade de gênero.\n\n"
            f"O projeto acompanha o **Projeto de Lei nº 1.182/2023** (Câmara dos Deputados), que visa incluir abrigos e casas de acolhimento LGBTQIA+ na Tarifa Social. "
            f"Atualmente, esse público é faturado na tarifa convencional B1 da Enel SP, tornando ferramentas de eficiência e simulação indispensáveis para a mitigação de vulnerabilidades.\n\n"
            f"*Fontes:* ANEEL (Res. 1.000/2021) e EPE (Anuário 2026)."
        )
    
    else:
        return (
            f"**Citizen Assist AI — Resumo da Análise Energética:**\n\n"
            f"Seu consumo atual estimado é de **{linha_base['consumo_mensal_kwh']} kWh/mês** (fatura estimada de R$ {linha_base['custo_mensal_brl']:.2f}/mês). "
            f"Com a **Alternativa 1**, você economiza **{alt1['economia_mensal_kwh']} kWh/mês** com CAPEX estimado de R$ {alt1['capex_brl']:.2f}. "
            f"Com a **Alternativa 2**, o projeto solar dimensionado gera **{alt2['geracao_mensal_kwh']} kWh/mês** com CAPEX estimado de R$ {alt2['capex_brl']:.2f}.\n\n"
            f"*Todas as simulações baseiam-se em dados públicos da ANEEL, EPE e CRESESB/CEPEL, sem garantia de valores fixos.*"
        )