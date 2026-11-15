import json
from pathlib import Path


def carregar_base_energetica():
    caminho = Path(__file__).resolve().parent.parent / "data" / "base_energetica_sers.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_energia_kwh(potencia_watts: float, horas_dia: float, dias: int = 30) -> float:
    if potencia_watts < 0 or horas_dia < 0 or dias < 0:
        raise ValueError("Valores não podem ser negativos.")
    if horas_dia > 24:
        raise ValueError("Horas por dia não podem exceder 24.")
    return round((potencia_watts * horas_dia * dias) / 1000.0, 2)


def calcular_linha_base(
    minutos_banho_dia: float = 24.0,
    qtd_lampadas: int = 8,
    potencia_chuveiro_w: float = 5500.0,
    potencia_lampada_w: float = 20.0,
    consumo_geladeira_kwh: float = 35.0,
    tarifa_brl_kwh: float = 0.78938,
    fator_co2_kg_kwh: float = 0.04,
) -> dict:
    if tarifa_brl_kwh <= 0:
        raise ValueError("A tarifa de energia deve ser maior que zero.")

    horas_banho_dia = minutos_banho_dia / 60.0
    consumo_banho = calcular_energia_kwh(potencia_chuveiro_w, horas_banho_dia)
    consumo_lampadas = calcular_energia_kwh(potencia_lampada_w * qtd_lampadas, 5.0)
    
    # Saldo residual explicitado como estimativa de modelagem para atingir a média EPE
    saldo_residual_estimado = 54.10
    consumo_total = round(consumo_banho + consumo_geladeira_kwh + consumo_lampadas + saldo_residual_estimado, 2)
    custo_total = round(consumo_total * tarifa_brl_kwh, 2)
    emissao_anual = round(consumo_total * 12 * fator_co2_kg_kwh, 2)

    return {
        "consumo_mensal_kwh": consumo_total,
        "custo_mensal_brl": custo_total,
        "emissao_anual_co2_kg": emissao_anual,
        "detalhes": {
            "consumo_banho_kwh": consumo_banho,
            "consumo_geladeira_kwh": consumo_geladeira_kwh,
            "consumo_lampadas_kwh": consumo_lampadas,
            "saldo_residual_estimado_kwh": saldo_residual_estimado,
        }
    }


def simular_eficiencia_energetica(
    linha_base: dict,
    minutos_banho_otimizado: float = 16.0,
    qtd_lampadas: int = 8,
    potencia_chuveiro_w: float = 5500.0,
    potencia_led_w: float = 9.0,
    custo_por_lampada_brl: float = 10.0,
    tarifa_brl_kwh: float = 0.78938,
    fator_co2_kg_kwh: float = 0.04,
) -> dict:
    horas_banho_otim = minutos_banho_otimizado / 60.0
    consumo_banho_novo = calcular_energia_kwh(potencia_chuveiro_w, horas_banho_otim)
    consumo_lampadas_novo = calcular_energia_kwh(potencia_led_w * qtd_lampadas, 5.0)
    
    consumo_antigo_parcial = linha_base["detalhes"]["consumo_banho_kwh"] + linha_base["detalhes"]["consumo_lampadas_kwh"]
    consumo_novo_parcial = consumo_banho_novo + consumo_lampadas_novo
    economia_kwh = round(max(0.0, consumo_antigo_parcial - consumo_novo_parcial), 2)
    
    novo_consumo = round(max(30.0, linha_base["consumo_mensal_kwh"] - economia_kwh), 2)
    nova_fatura = round(novo_consumo * tarifa_brl_kwh, 2)
    economia_mensal_brl = round(linha_base["custo_mensal_brl"] - nova_fatura, 2)
    
    capex = round(qtd_lampadas * custo_por_lampada_brl, 2)
    payback_meses = round(capex / economia_mensal_brl, 2) if economia_mensal_brl > 0 else 999.0
    co2_evitado = round(economia_kwh * 12 * fator_co2_kg_kwh, 2)
    percentual_reducao = round((economia_kwh / linha_base["consumo_mensal_kwh"]) * 100.0, 2)

    return {
        "novo_consumo_mensal_kwh": novo_consumo,
        "economia_mensal_kwh": economia_kwh,
        "nova_fatura_mensal_brl": nova_fatura,
        "economia_mensal_brl": economia_mensal_brl,
        "capex_brl": capex,
        "payback_meses": payback_meses,
        "co2_evitado_anual_kg": co2_evitado,
        "percentual_reducao": percentual_reducao,
    }


def simular_solar_ongrid(
    linha_base: dict,
    potencia_sistema_kwp: float = 1.50,
    hsp_diario: float = 4.44,
    taxa_desempenho: float = 0.75,
    custo_kwp_brl: float = 3620.0,
    tarifa_brl_kwh: float = 0.78938,
    disponibilidade_kwh: float = 30.0,
    tusd_fio_b_brl_kwh: float = 0.17795,
    percentual_fio_b: float = 0.60,
    fator_co2_kg_kwh: float = 0.04,
) -> dict:
    if potencia_sistema_kwp <= 0:
        raise ValueError("Potência do sistema solar deve ser maior que zero.")
    
    geracao_mensal = round(potencia_sistema_kwp * hsp_diario * 30.0 * taxa_desempenho, 2)
    consumo = linha_base["consumo_mensal_kwh"]
    
    geracao_compensavel = min(geracao_mensal, consumo)
    encargo_fio_b = round(geracao_compensavel * tusd_fio_b_brl_kwh * percentual_fio_b, 2)
    
    consumo_liquido_faturavel = max(disponibilidade_kwh, round(consumo - geracao_mensal, 2))
    fatura_residual = round((consumo_liquido_faturavel * tarifa_brl_kwh) + encargo_fio_b, 2)
    
    economia_mensal_brl = round(max(0.0, linha_base["custo_mensal_brl"] - fatura_residual), 2)
    capex = round(potencia_sistema_kwp * custo_kwp_brl, 2)
    
    economia_anual_brl = round((economia_mensal_brl * 12.0) - 150.0, 2)
    payback_anos = round(capex / economia_anual_brl, 2) if economia_anual_brl > 0 else 99.0
    
    # Correção P2: O CO2 evitado restringe-se estritamente à energia efetivamente compensada pelo consumo da rede
    energia_efetivamente_deslocada_kwh = min(geracao_mensal, consumo)
    co2_evitado = round(energia_efetivamente_deslocada_kwh * 12 * fator_co2_kg_kwh, 2)
    
    percentual_cobertura = round(min(100.0, (geracao_mensal / consumo) * 100.0), 2)

    return {
        "geracao_mensal_kwh": geracao_mensal,
        "fatura_residual_mensal_brl": fatura_residual,
        "economia_mensal_brl": economia_mensal_brl,
        "capex_brl": capex,
        "economia_liquida_anual_brl": economia_anual_brl,
        "payback_anos": payback_anos,
        "co2_evitado_anual_kg": co2_evitado,
        "percentual_cobertura": percentual_cobertura,
    }


def recomendar_por_perfil(imovel_proprio: bool, telhado_viavel: bool, orcamento_brl: float, capex_solar_real: float) -> dict:
    if imovel_proprio and telhado_viavel and orcamento_brl >= capex_solar_real:
        return {
            "escolha": "Alternativa 2: Fonte Renovável (Solar On-Grid)",
            "justificativa": f"O cidadão possui imóvel próprio, telhado livre e orçamento compatível com o CAPEX dimensionado de R$ {capex_solar_real:.2f}, viabilizando o maior retorno e abatimento de emissões de longo prazo."
        }
    elif not imovel_proprio:
        return {
            "escolha": "Alternativa 1: Eficiência Energética (LED + Gestão de Banho)",
            "justificativa": "Como o cidadão reside em imóvel alugado, reformas estruturais e instalação de painéis solares fixos são inviáveis. A eficiência energética oferece ganho imediato com baixo investimento."
        }
    elif not telhado_viavel:
        return {
            "escolha": "Alternativa 1: Eficiência Energética (LED + Gestão de Banho)",
            "justificativa": "A ausência de um telhado viável sem sombreamento impede a captação fotovoltaica adequada, tornando a eficiência energética a via ideal."
        }
    else:
        return {
            "escolha": "Alternativa 1: Eficiência Energética (Fase Inicial) / Economia Doméstica",
            "justificativa": f"O orçamento disponível (R$ {orcamento_brl:.2f}) é inferior ao CAPEX necessário para o sistema solar dimensionado (R$ {capex_solar_real:.2f}). Recomenda-se iniciar com a Eficiência Energética e planejar financiamento futuro."
        }