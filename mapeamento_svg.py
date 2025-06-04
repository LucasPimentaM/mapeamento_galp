# %% [markdown]
# ## **Mapeamento Galp**
# 
# ##### **___Informações___**
# 
# **Projeto:** Galp
# 
# **Autor:** Lucas Pimenta dos Santos Monteiro
# 
# **Data:** 24/02/2025
# 
# ##### **___Objetivo___**
# 
# A ideia desse cógido é automatizar a visualização de uma imagem .svg gerada no Inkscape de acordo com o output do programa (report.csv) e os dados de entrada definidos (entry_data.csv).
# 
# Para isso foram criados rótulos no Inkscape que identificam cada elemento de texto a partir do inkscape:label. Cada label recebeu o nome equivalente a variável proveniente do report.csv e entry_data.csv que representa o valor desejado.

# %% [markdown]
# ##### **Importando as Bibliotecas**

# %%
import pandas as pd
import xml.etree.ElementTree as ET

# %%
entry_data = pd.read_csv("entry_data.csv")
report = pd.read_csv("report.csv")

# %% [markdown]
# ##### **Verificando os Dados**

# %%
entry_data.head()

# %%
report.head()

# %% [markdown]
# ##### **Definindo as Colunas que serão utilizadas de cada dataframe**

# %%
userows_entry_data = [
    "Cooling heat exchanger flow rate =",
    "Brine flow rate out of the regulating tank =",
    "Temperature at the entrance of the cold side =",
    "Motor power demanded/generated =",                                     
    "Electrolyzer cell temperature =",                                      
    "Cathode pressure =",
    "RO feedtank brackish water temperature =",
    "RO feedtank brackish water salinity =",
    "RO pump power ="
]

usecols_report = [
"Time (s)",
"Overall - Net water production (L)",
"Desal - Distilled water production rate (kg/h)",
"FeedTank - Brackish water inlet flow rate (kg/h)",
"ColdHex - Heat transfer rate (W)",
"ColdHex - Cold side outlet temperature (°C)",
"Desal - Hot feedwater outlet temperature (°C)",
"Desal - Hot feedwater outlet mass flow rate (kg/h)",
"Desal - Hot feedwater outlet salinity (wt%)",
"HotHex - Cold side salinity (wt%)",
"ColdHex - Hot side outlet temperature (°C)",
"ColdHex - Hot side salinity (wt%)",
"HotHex - Cold side salinity (wt%)",
"HotHex - Heat transfer rate (W)",
"HotHex - Hot side outlet temperature (°C)",
"HotHex - Hot side inlet temperature (°C)",
"HotHex - Cold side outlet temperature (°C)",
"ColdHex - Hot side inlet temperature (°C)",
"ColdHex - Hot side inlet mass flow rate (kg/h)",
"HotHex - Cold side inlet temperature (°C)",
"Time (s)",
"SolarField - Solar irradiance (W/m²)", # segundo 11088 -> tempo de máximo
"SolarField - Efficiency",
"SolarField - Solar field inlet temperature (°C)",
"SolarField - Solar field outlet temperature (°C)",
"CircuitFromSolar - Outlet temperature (°C)",
"CircuitToSolar - Inlet temperature (°C)",
"ColdHex - Hot side salinity (wt%)",
"FeedTank - Water salinity (wt%)",
"FeedTank - Water temperature (°C)",
"Desal - Film wall temperature (°C)",
"Desal - Gap film boundary temperature (°C)",
"HCPV - Inlet temperature (°C)",
"HCPV - Outlet temperature (°C)",
"HCPV - Mass flow rate (kg/s)",
"HCPV - Heat transfer rate recovered from the solar cells (kW)",
"HCPV - Electrical power (kW)",
"HCPV - Global panel electrical efficiency (%)",
"HCPV - Electrical energy generated (kWh)",
"CircuitToSolar - Mass flow rate (kg/s)",
"ETC - Efficiency",
"ETC - ETC inlet temperature (°C)",
"ETC - ETC outlet temperature (°C)",
"ETC - Mass flow rate (kg/s)",
"PVT - PVT inlet temperature (°C)",
"PVT - Thermal Efficiency",
"PVT - Electrical power output (W)",
"PVT - Electrical Efficiency",
"PVT - Electrical energy generated (kWh)",
"PVT - PVT outlet temperature (°C)",
"PVT - Mass flow rate (kg/s)",
"PVT - Heat transfer rate (W)",
"ETC - Heat transfer rate (W)",
"SolarField - Heat transfer rate (W)",
"Reservoir - Temperature (°C)",
"Mix Valve - Mass flow rate in from reservoir(kg/s)",
"Mix Valve - Temperature in from reservoir(kg/s)",
"Mix Valve - Out Temperature (°C)",
"Mix Valve - Out Mass flow rate (kg/s)",
"Motor - Outlet mass flow rate (kg/s)",
"Motor - Outlet temperature motor (°C)",
"Motor - Radiator in mass flow rate (kg/s)",
"Motor - Radiator bypass mass flow rate (kg/s)",
"Motor - Recirculation mass flow rate (kg/s)",
"Motor - Nominal Mass flow rate (kg/s)",
"Motor - Mixture temperature engine (°C)",
"Motor - Mixture temperature radiator (°C)",
"Motor - Oulet temperature radiator (°C)",
"Motor - Heat coolant (kW)",
"Motor - System efficiency",
"Motor - Electrical energy generated/demanded (kWh)",
"Motor - Fuel consumed (L)",
"Motor - Fuel consumption (L/h)",
"Motor - Fuel consumption (g/kWh)",
"Electrolyzer - Hydrogen flow rate (Nm³/h)",
"Electrolyzer - Hydrogen produced (Nm³)",
"Electrolyzer - Water consumption rate (kg/h)",
"Electrolyzer - Water consumed (kg)",
"Electrolyzer - Conversion efficiency (%)",
"Electrolyzer - Heat transfer rate generated (W)",
"Electrolyzer - Power demand (W)",
"Electrolyzer - Electricity demand (kWh)",
"RO Feedtank - Temperature (°C)",
"RO Module - Brine outlet salinity (wt%)",
"RO Module - Brine outflow rate (kg/h)",
"RO Feedtank - Mass outflow rate (kg/h)",
"RO Feedtank - Salinity (wt%)",
"RO Pump - Outlet pressure (bar)",
"RO Module - Permeate salinity (wt%)",
"RO Pump - Electricity consumption (kWh)",
"Mix Valve - Mass flow rate in from central reservoir(kg/s)",
"Mix Valve - Mass flow rate in from central reservoir(kg/s)",
"Mix Valve - Temperature in from central reservoir(kg/s)",
"Central Reservoir - Temperature (°C)",
"Overall - Net electricity generation (kWh)",
"Overall - Net heat recovered (kWh)",
"Overall - Salinity of the treated water (wt%)",
"Motor - Heat transfer rate (kW)"
]

# %% [markdown]
# ##### Filtrando os Dataframes de Acordo com as Colunas

# %%
entry_data_filtrado = entry_data[entry_data['Entry data:'].isin(userows_entry_data)]
entry_data_filtrado

# %%
report_filtrado = report.filter(items=usecols_report)
report_filtrado.head()

# %% [markdown]
# #### Separando o tempo final para o overall results

# %%
report_filtrado_tempo_final = report_filtrado.tail(1)
report_filtrado_tempo_final.head()

# %%
# Net electricity generation

net_electricity_generation = str(round(float(report_filtrado_tempo_final['Overall - Net electricity generation (kWh)'].iloc[0]), 2)) + " kWh"
print("Net electricity generation:", net_electricity_generation)

# Net water production -> tem que colocar no valor do Overall - Net water production - ft - (L) no svg

net_water_production = str(round(float(report_filtrado_tempo_final['Overall - Net water production (L)'].iloc[0]), 2)) + " L"
print("Net water production:", net_water_production)

# Net heat recovered

net_heat_recovered = str(round(float(report_filtrado_tempo_final['Overall - Net heat recovered (kWh)'].iloc[0]), 2)) + " kWh"
print("Net heat recovered:", net_heat_recovered)


# %% [markdown]
# ##### Separando apenas o tempo de máxima radiação solar do output gerado no report.csv

# %%
report_filtrado.tail()

# %%
report_filtrado = report_filtrado.iloc[[report_filtrado['SolarField - Solar irradiance (W/m²)'].idxmax()]].reset_index(drop=True)
report_filtrado.head()

# %% [markdown]
# ##### Lendo o arquivo do Inkscape e definindo uma função de substituição de valores

# %%
# Caminho para o arquivo SVG
arquivo_svg = 'Diag_geral_2025_06_04.svg'

# Parse o arquivo SVG
tree = ET.parse(arquivo_svg)
root = tree.getroot()

# Definir namespaces
namespaces = {'svg': 'http://www.w3.org/2000/svg', 'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

def substituir_texto_por_label(label, novo_texto):
    # Encontre todos os elementos do tipo 'text'
    textos = root.findall('.//svg:text', namespaces)
    
    # Para cada elemento 'text' encontrado
    for texto in textos:
        # Verifique se o elemento 'text' possui o atributo 'inkscape:label'
        if texto.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label') == label:
            # Itere sobre os elementos 'tspan' dentro do elemento 'text'
            for tspan in texto.findall('.//svg:tspan', namespaces):
                # Substitua o texto do 'tspan' pelo novo texto
                tspan.text = novo_texto

# %% [markdown]
# #### Definindo Função para Cálculo da Salinidade em g/l

# %% [markdown]
# Atualmente o código gera no report a salinidade em porcentagem de peso wt% (weight percent), porém a salinidade depende da densidade que é inversamente proporcional a temperatura, por isso é necessário o uso da função a seguir:

# %%
def salt_water_density(T, s):
    a0 = 9.999 * 10**2
    a1 = 2.034 * 10**-2
    a2 = -6.162 * 10**-3
    a3 = 2.261 * 10**-5
    a4 = -4.657 * 10**-8
    b0 = 8.020 * 10**2
    b1 = -2.001
    b2 = 1.677 * 10**-2
    b3 = -3.060 * 10**-5
    b4 = -1.613 * 10**-5

    result = (a0 + a1 * T + a2 * T**2 + a3 * T**3 + a4 * T**4 + 
              b0 * s + b1 * s * T + b2 * s * T**2 + 
              b3 * s * T**3 + b4 * s**2 * T**2)

    return result

# %% [markdown]
# #### Definindo cada a temperatura para cada Salinidade

# %%
# De cima para baixo no desenho e da esquerda para a direita, temos

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#### HotHex - Cold side salinity (wt%) -> está presente na primeira e na segunda instância de salinidade, os valores são iguais em wt% mas distintos em g/L


# A temperatura da primeira instância (mais a esquerda) é a variável HotHex - Cold side outlet temperature (°C)

# No desenho, o nome dessa instância da salinidade foi alterado para HotHex - Cold side salinity 1 (wt%)

T_css1 = float(report_filtrado['HotHex - Cold side outlet temperature (°C)'].iloc[0])
S_css1 = float(report_filtrado['HotHex - Cold side salinity (wt%)'].iloc[0]/100)
css1_g_l = "s " + str(round(S_css1 * salt_water_density(T_css1, S_css1), 2)) + " g/l"

# A temperatura da segunda instância (mais a direita) é a variável HotHex - Cold side inlet temperature (°C)
# No desenho, o nome dessa instância da salinidade foi alterado para HotHex - Cold side salinity 2 (wt%)

T_css2 = float(report_filtrado['HotHex - Cold side inlet temperature (°C)'].iloc[0])
S_css2 = float(report_filtrado['HotHex - Cold side salinity (wt%)'].iloc[0]/100)
css2_g_l = "s " + str(round(S_css2 * salt_water_density(T_css2, S_css2), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#### Desal - Hot feedwater outlet salinity (wt%) -> terceira instância de salinidade

# A temperatura da terceira instância está na variável -> Desal - Hot feedwater outlet temperature (°C)

T_hfos = float(report_filtrado['Desal - Hot feedwater outlet temperature (°C)'].iloc[0])
S_hfos = float(report_filtrado['Desal - Hot feedwater outlet salinity (wt%)'].iloc[0]/100)
hfos_g_l = "s " + str(round(S_hfos * salt_water_density(T_hfos, S_hfos), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#### ColdHex - Hot side salinity (wt%) -> está presente na quarta e quinta instância de salinidade

# A temperatura da quarta instância (mais para cima) é a variável ColdHex - Hot side outlet temperature (°C)
# No desenho, o nome dessa instância da salinidade foi alterado para ColdHex - Hot side salinity 1 (wt%)

T_hss1 = float(report_filtrado['ColdHex - Hot side outlet temperature (°C)'].iloc[0])
S_hss1 = float(report_filtrado['ColdHex - Hot side salinity (wt%)'].iloc[0]/100)
hss1_g_l = "s " + str(round(S_hss1 * salt_water_density(T_hss1, S_hss1), 2)) + " g/l"

# A temperatura da quinta instância (mais para baixo) é a variável ColdHex - Hot side inlet temperature (°C)
# No desenho, o nome dessa instância da salinidade foi alterado para ColdHex - Hot side salinity 2 (wt%)

T_hss2 = float(report_filtrado['ColdHex - Hot side inlet temperature (°C)'].iloc[0])
S_hss2 = float(report_filtrado['ColdHex - Hot side salinity (wt%)'].iloc[0]/100)
hss2_g_l = "s " + str(round(S_hss2 * salt_water_density(T_hss2, S_hss2), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#### Brackish water salinity at the entrance of the regulating tank = -> está presente na sexta instância de salinidade

# A temperatura da sexta instância está na variável -> Brackish water temperature at the entrance of the regulating tank =

#T_bws = float(entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'Brackish water temperature at the entrance of the regulating tank =']['Unnamed: 1'].iloc[0])
#S_bws = float(entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'Brackish water salinity at the entrance of the regulating tank =']['Unnamed: 1'].iloc[0])/100
#bws_g_l = "s " + str(round(S_bws * salt_water_density(T_bws, S_bws), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#### FeedTank - Water salinity (wt%) -> está presente na sétima instância de salinidade

# A temperatura da sétima instância está na variável -> FeedTank - Water temperature (°C)

T_fts = float(report_filtrado['FeedTank - Water temperature (°C)'].iloc[0])
S_fts = float(report_filtrado['FeedTank - Water salinity (wt%)'].iloc[0]/100)
fts_g_l = "s " + str(round(S_fts * salt_water_density(T_fts, S_fts), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#### RO Module - Brine outlet salinity (wt%) -> está presente na oitava instância de salinidade
# A temperatura da oitava instância está na variável -> RO Feedtank - Temperature (°C)
T_ros = float(report_filtrado['RO Feedtank - Temperature (°C)'].iloc[0])
S_ros = float(report_filtrado['RO Module - Brine outlet salinity (wt%)'].iloc[0]/100)
ros_g_l = "s " + str(round(S_ros * salt_water_density(T_ros, S_ros), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# RO feedtank brackish water salinity =
ro_feedtank_brackish_water_salinity = float(entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'RO feedtank brackish water salinity =']['Unnamed: 1'].iloc[0])/100
# RO feedtank brackish water temperature =
ro_feedtank_brackish_water_temperature = entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'RO feedtank brackish water temperature =']['Unnamed: 1'].iloc[0]

# RO feedtank brackish water salinity g/L
ro_feedtank_brackish_water_salinity_g_l = "s " + str(round(float(ro_feedtank_brackish_water_salinity) * salt_water_density(float(ro_feedtank_brackish_water_temperature), ro_feedtank_brackish_water_salinity), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# RO Feedtank - Salinity (wt%)

ro_feedtank_salinity = float(report_filtrado['RO Feedtank - Salinity (wt%)'].iloc[0])/100
ro_feedtank_temperature = report_filtrado['RO Feedtank - Temperature (°C)'].iloc[0]
ro_feedtank_salinity_g_l = "s " + str(round(float(ro_feedtank_salinity) * salt_water_density(float(ro_feedtank_temperature), ro_feedtank_salinity), 2)) + " g/l"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# RO Module - Permeate salinity (wt%)
ro_module_permeate_salinity = float(report_filtrado['RO Module - Permeate salinity (wt%)'].iloc[0])/100
ro_module_permeate_salinity_g_l = "s " + str(round(ro_module_permeate_salinity * salt_water_density(float(report_filtrado['RO Feedtank - Temperature (°C)'].iloc[0]), ro_module_permeate_salinity), 2)) + " g/l"


# calculando o Salinity of the treated water

salinity_treated_water = float(report_filtrado_tempo_final['Overall - Salinity of the treated water (wt%)'].iloc[0]/100)
salinity_treated_water_temperature = 25 # assumindo temperatura ambiente de 25°C
salinity_treated_water_g_l = "s " + str(round(salinity_treated_water * salt_water_density(salinity_treated_water_temperature,salinity_treated_water), 2)) + " g/l"
print("Salinity of the treated water:", salinity_treated_water)
print("Salinity of the treated water:", salinity_treated_water_g_l)

# %% [markdown]
# #### Passando o Desal - Total water produced (kg) para litro -> vamos dividir o valor em kg por 0.998

# %%
#total_water_produced_kg = report_filtrado['Desal - Total water produced (kg)'].iloc[0]
#total_water_produced_l = str(round(total_water_produced_kg / 0.998, 2)) + " L"
total_water_produced_l = str(round(float(report_filtrado['Overall - Net water production (L)'].iloc[0]),2)) + " L"
print(total_water_produced_l)

# %% [markdown]
# #### Calculando o valor de (Desal - Film wall temperature (°C)+Desal - Gap film boundary temperature (°C))/2

# %%
film_wall_temp = report_filtrado['Desal - Film wall temperature (°C)'].iloc[0]
gap_film_boundary_temp = report_filtrado['Desal - Gap film boundary temperature (°C)'].iloc[0]
average_temp = "T "+ str(round((film_wall_temp + gap_film_boundary_temp) / 2, 2)) + " °C"

# %% [markdown]
# #### Calculando o valor de Motor - Radiator in mass flow rate (kg/s) + Motor - Radiator bypass mass flow rate (kg/s)

# %%
motor_flow_rate_combined = "ṁ " + str(round(report_filtrado['Motor - Radiator in mass flow rate (kg/s)'].iloc[0] + report_filtrado['Motor - Radiator bypass mass flow rate (kg/s)'].iloc[0], 2)) + " kg/s"
print(motor_flow_rate_combined)

# %% [markdown]
# #### Calculando [RO Module - Brine outflow rate (kg/h)] - [RO Feedtank - Mass outflow rate (kg/h)]

# %%
#[RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)]

ro_brine_calc = report_filtrado['RO Module - Brine outflow rate (kg/h)'].iloc[0] - report_filtrado['FeedTank - Brackish water inlet flow rate (kg/h)'].iloc[0]
#ro_brine_calc = "ṁ " + str(round(ro_brine_calc/3600, 2)) + " kg/s"
ro_brine_calc = "ṁ " + str(round(ro_brine_calc, 2)) + " kg/h"
print(ro_brine_calc)


# %% [markdown]
# #### Calculando [RO Feedtank - Mass outflow rate (kg/h)] - ([RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)])

# %%
#[RO Feedtank - Mass outflow rate (kg/h)] - ([RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)])

ro_feedtank_calc = float(report_filtrado['RO Feedtank - Mass outflow rate (kg/h)'].iloc[0]) - float(ro_brine_calc.split(" ")[1])
#ro_feedtank_calc = "ṁ " + str(round(float(ro_feedtank_calc/3600), 2)) + " kg/s"
ro_feedtank_calc = "ṁ " + str(round(float(ro_feedtank_calc), 2)) + " kg/h"
print(ro_feedtank_calc)

# %% [markdown]
# #### Calculando [RO Feedtank - Mass outflow rate (kg/h)] - [RO Module - Brine outflow rate (kg/h)]

# %%
# [RO Feedtank - Mass outflow rate (kg/h)] - [RO Module - Brine outflow rate (kg/h)]

ro_feedtank_brine_calc = float(report_filtrado['RO Feedtank - Mass outflow rate (kg/h)'].iloc[0]) - float(report_filtrado['RO Module - Brine outflow rate (kg/h)'].iloc[0])
#ro_feedtank_brine_calc = "ṁ " + str(round(float(ro_feedtank_brine_calc)/3600, 2)) + " kg/s"
ro_feedtank_brine_calc = "ṁ " + str(round(float(ro_feedtank_brine_calc), 2)) + " kg/h"
print(ro_feedtank_brine_calc)

# %% [markdown]
# ##### Substituindo os Valores

# %%
for coluna, valor in report_filtrado.items():
    valor = valor.iloc[0]
    grandeza = ""
    if '(' in coluna and ')' in coluna:
        unidade = coluna[coluna.rfind('(') + 1:coluna.rfind(')')]
        unidade = unidade.strip()
    elif coluna == "SolarField - Efficiency" or coluna == "PVT - Thermal Efficiency" or coluna == "ETC - Efficiency" or coluna == "PVT - Electrical Efficiency" or coluna == "Motor - System efficiency":
        unidade = "%"
    else:
        unidade = ""
    if coluna == "PVT - Heat transfer rate (W)" or coluna == "SolarField - Heat transfer rate (W)" or coluna == "ETC - Heat transfer rate (W)" or coluna == "PVT - Electrical power output (W)" or coluna == "Electrolyzer - Heat transfer rate generated (W)" or coluna == "Electrolyzer - Power demand (W)":
        unidade = "kW"
        valor = "{:.2f}".format(float(valor/1000))
    if coluna == "HotHex - Heat transfer rate (W)" or coluna == "ColdHex - Heat transfer rate (W)":
        unidade = "kW"
        grandeza = "Q"
        valor = "{:.2f}".format(float(valor/1000))
    #if coluna == "RO Module - Brine outflow rate (kg/h)" or coluna == "FeedTank - Brackish water inlet flow rate (kg/h)" or coluna == "RO Feedtank - Mass outflow rate (kg/h)":
    #    unidade = "kg/s"
    #    grandeza = "ṁ"
    #    valor = "{:.2f}".format(float(valor/3600))
    if unidade == '°C':
        grandeza = "T"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'kg/s':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'Kg/h' or unidade == 'kg/h':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'g/L':
        grandeza = "S"
        valor = "{:.2f}".format(float(valor))
    valor = "{:.2f}".format(float(valor))
    valor_novo = grandeza + " " + str(valor) + " " + unidade
    print(valor_novo)
    substituir_texto_por_label(coluna, valor_novo)

# %%
for linha in entry_data_filtrado.itertuples():
    grandeza = ""
    label = linha[1].rstrip(' ')
    valor = linha[2]
    valor = "{:.2f}".format(float(valor))
    unidade = linha[3].strip()
    if unidade == '°C':
        grandeza = "T"
        if label == "Electrolyzer cell temperature =":
            grandeza = ""
        valor = "{:.2f}".format(float(valor))
    if unidade == 'kg/s':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'kg/h' or unidade == 'Kg/h':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
        #if label == "Brine flow rate out of the regulating tank =":
        #    grandeza = "ṁ"
        #    unidade = "kg/s"
        #    valor = "{:.2f}".format(float(valor)/3600)
    if unidade == 'g/L':
        grandeza = "S"
        valor = "{:.2f}".format(float(valor))

    valor_novo = grandeza + " " + str(valor) + ' ' + unidade
    print(label, valor_novo)
    substituir_texto_por_label(label, str(valor_novo))

# %%
substituir_texto_por_label("HotHex - Cold side salinity 1 (wt%)", css1_g_l)
substituir_texto_por_label("HotHex - Cold side salinity 2 (wt%)", css2_g_l)
substituir_texto_por_label("Desal - Hot feedwater outlet salinity (wt%)", hfos_g_l)
substituir_texto_por_label("ColdHex - Hot side salinity 1 (wt%)", hss1_g_l)
substituir_texto_por_label("ColdHex - Hot side salinity 2 (wt%)", hss2_g_l)
#substituir_texto_por_label("Brackish water salinity at the entrance of the regulating tank =", bws_g_l)
substituir_texto_por_label("FeedTank - Water salinity (wt%)", fts_g_l)
substituir_texto_por_label("RO Module - Brine outlet salinity (wt%)", ros_g_l)
substituir_texto_por_label("RO feedtank brackish water salinity =", ro_feedtank_brackish_water_salinity_g_l)
substituir_texto_por_label("Motor - Radiator in mass flow rate (kg/s) + Motor - Radiator bypass mass flow rate (kg/s)", motor_flow_rate_combined)

# correção do valor de total de água produzida
substituir_texto_por_label("Desal - Total water produced (kg)", total_water_produced_l)

# correção do valor de temperatura média
substituir_texto_por_label("(Desal - Film wall temperature (°C)+Desal - Gap film boundary temperature (°C))/2", average_temp)

# valor do [RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)]
substituir_texto_por_label("[RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)]", ro_brine_calc)

# valor do [RO Feedtank - Mass outflow rate (kg/h)] - ([RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)])
substituir_texto_por_label("[RO Feedtank - Mass outflow rate (kg/h)] - ([RO Module - Brine outflow rate (kg/h)] - [FeedTank - Brackish water inlet flow rate (kg/h)])", ro_feedtank_calc)

# valor RO Feedtank - Salinity (wt%)
substituir_texto_por_label("RO Feedtank - Salinity (wt%)", ro_feedtank_salinity_g_l)

# RO Module - Permeate salinity (wt%)
substituir_texto_por_label("RO Module - Permeate salinity (wt%)", ro_module_permeate_salinity_g_l)

# [RO Feedtank - Mass outflow rate (kg/h)] - [RO Module - Brine outflow rate (kg/h)]
substituir_texto_por_label("[RO Feedtank - Mass outflow rate (kg/h)] - [RO Module - Brine outflow rate (kg/h)]", ro_feedtank_brine_calc)

# Substituindo os valores de overall do tempo final
substituir_texto_por_label("Overall - Net electricity generation (kWh)", net_electricity_generation)
substituir_texto_por_label("Overall - Net water production - ft - (L)", net_water_production)
substituir_texto_por_label("Overall - Net heat recovered (kWh)", net_heat_recovered)
substituir_texto_por_label("Overall - Salinity of the treated water (wt%)", salinity_treated_water_g_l)

# %% [markdown]
# ##### Salvando o arquivo

# %%
# Salvar as alterações no arquivo SVG
tree.write('Diag_geral_modificado.svg')


