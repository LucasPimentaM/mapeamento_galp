import pandas as pd
import xml.etree.ElementTree as ET

entry_data = pd.read_csv("entry_data.csv")
report = pd.read_csv("report.csv")

userows_entry_data = [
    "Cooling heat exchanger flow rate =",
    "Brine flow rate out of the regulating tank =",
    "Brackish water temperature at the entrance of the regulating tank =",
    "Brackish water salinity at the entrance of the regulating tank =",
    "Temperature at the entrance of the cold side =",
    "Motor power demanded/generated =",
    "Electrolyzer cell temperature =",
    "Cathode pressure ="

]

usecols_report = [
"Time (s)",
"Desal - Total water produced (kg)",
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
"Electrolyzer - Electricity demand (kWh)"
]

entry_data_filtrado = entry_data[entry_data['Entry data:'].isin(userows_entry_data)]

report_filtrado = report.filter(items=usecols_report)

report_filtrado = report_filtrado.iloc[[report_filtrado['SolarField - Solar irradiance (W/m²)'].idxmax()]].reset_index(drop=True)

# Caminho para o arquivo SVG
arquivo_svg = 'Diag_geral_2025_04_11.svg'

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

T_css1 = float(report_filtrado['HotHex - Cold side outlet temperature (°C)'].iloc[0])
S_css1 = float(report_filtrado['HotHex - Cold side salinity (wt%)'].iloc[0]/100)
css1_g_l = "s " + str(round(S_css1 * salt_water_density(T_css1, S_css1), 2)) + " g/l"

T_css2 = float(report_filtrado['HotHex - Cold side inlet temperature (°C)'].iloc[0])
S_css2 = float(report_filtrado['HotHex - Cold side salinity (wt%)'].iloc[0]/100)
css2_g_l = "s " + str(round(S_css2 * salt_water_density(T_css2, S_css2), 2)) + " g/l"

T_hfos = float(report_filtrado['Desal - Hot feedwater outlet temperature (°C)'].iloc[0])
S_hfos = float(report_filtrado['Desal - Hot feedwater outlet salinity (wt%)'].iloc[0]/100)
hfos_g_l = "s " + str(round(S_hfos * salt_water_density(T_hfos, S_hfos), 2)) + " g/l"

T_hss1 = float(report_filtrado['ColdHex - Hot side outlet temperature (°C)'].iloc[0])
S_hss1 = float(report_filtrado['ColdHex - Hot side salinity (wt%)'].iloc[0]/100)
hss1_g_l = "s " + str(round(S_hss1 * salt_water_density(T_hss1, S_hss1), 2)) + " g/l"

T_hss2 = float(report_filtrado['ColdHex - Hot side inlet temperature (°C)'].iloc[0])
S_hss2 = float(report_filtrado['ColdHex - Hot side salinity (wt%)'].iloc[0]/100)
hss2_g_l = "s " + str(round(S_hss2 * salt_water_density(T_hss2, S_hss2), 2)) + " g/l"

T_bws = float(entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'Brackish water temperature at the entrance of the regulating tank =']['Unnamed: 1'].iloc[0])
S_bws = float(entry_data_filtrado[entry_data_filtrado['Entry data:'] == 'Brackish water salinity at the entrance of the regulating tank =']['Unnamed: 1'].iloc[0])/100
bws_g_l = "s " + str(round(S_bws * salt_water_density(T_bws, S_bws), 2)) + " g/l"

T_fts = float(report_filtrado['FeedTank - Water temperature (°C)'].iloc[0])
S_fts = float(report_filtrado['FeedTank - Water salinity (wt%)'].iloc[0]/100)
fts_g_l = "s " + str(round(S_fts * salt_water_density(T_fts, S_fts), 2)) + " g/l"

total_water_produced_kg = report_filtrado['Desal - Total water produced (kg)'].iloc[0]
total_water_produced_l = str(round(total_water_produced_kg / 0.998, 2)) + " L"

film_wall_temp = report_filtrado['Desal - Film wall temperature (°C)'].iloc[0]
gap_film_boundary_temp = report_filtrado['Desal - Gap film boundary temperature (°C)'].iloc[0]
average_temp = str(round((film_wall_temp + gap_film_boundary_temp) / 2, 2)) + " °C"

motor_flow_rate_combined = "ṁ " + str(round(report_filtrado['Motor - Radiator in mass flow rate (kg/s)'].iloc[0] + report_filtrado['Motor - Radiator bypass mass flow rate (kg/s)'].iloc[0], 2)) + " kg/s"

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

for linha in entry_data_filtrado.itertuples():
    grandeza = ""
    label = linha[1].rstrip(' ')
    valor = linha[2]
    valor = "{:.2f}".format(float(valor))
    unidade = linha[3].strip()
    if unidade == '°C':
        grandeza = "T"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'kg/s':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'kg/h' or unidade == 'Kg/h':
        grandeza = "ṁ"
        valor = "{:.2f}".format(float(valor))
    if unidade == 'g/L':
        grandeza = "S"
        valor = "{:.2f}".format(float(valor))

    valor_novo = grandeza + " " + str(valor) + ' ' + unidade
    #print(valor_novo)
    substituir_texto_por_label(label, str(valor_novo))

substituir_texto_por_label("HotHex - Cold side salinity 1 (wt%)", css1_g_l)
substituir_texto_por_label("HotHex - Cold side salinity 2 (wt%)", css2_g_l)
substituir_texto_por_label("Desal - Hot feedwater outlet salinity (wt%)", hfos_g_l)
substituir_texto_por_label("ColdHex - Hot side salinity 1 (wt%)", hss1_g_l)
substituir_texto_por_label("ColdHex - Hot side salinity 2 (wt%)", hss2_g_l)
substituir_texto_por_label("Brackish water salinity at the entrance of the regulating tank =", bws_g_l)
substituir_texto_por_label("FeedTank - Water salinity (wt%)", fts_g_l)
substituir_texto_por_label("Motor - Radiator in mass flow rate (kg/s) + Motor - Radiator bypass mass flow rate (kg/s)", motor_flow_rate_combined)

# correção do valor de total de água produzida
substituir_texto_por_label("Desal - Total water produced (kg)", total_water_produced_l)

# correção do valor de temperatura média
substituir_texto_por_label("(Desal - Film wall temperature (°C)+Desal - Gap film boundary temperature (°C))/2", average_temp)

# Salvar as alterações no arquivo SVG
tree.write('Diag_geral_modificado.svg')