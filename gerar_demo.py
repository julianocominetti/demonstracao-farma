"""
gerar_demo.py — Gera demo.html com dados fictícios para apresentação comercial.
Usa o mesmo template agente-fabrica.html. Não requer arquivos Excel.

Uso:
    python3 gerar_demo.py

Saída:
    demo.html  (abre direto no dashboard, sem login, com banner de demo)
"""

import json, os
from collections import defaultdict

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "agente-fabrica.html")
OUTPUT_FILE   = os.path.join(SCRIPT_DIR, "demo.html")

MESES_5   = ["Jan", "Fev", "Mar", "Abr", "Mai"]
DIAS_MES  = {"Jan": 31, "Fev": 28, "Mar": 31, "Abr": 30, "Mai": 31}
CUR_MONTH = "Mai"
DIAS_EL   = 20
DIAS_TOT  = 31

# Nome da empresa fictícia
EMPRESA = "FarmaCenter Distribuidora"

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def make_m26(metas, fats, devs, mgs):
    rows = []
    for i, mes in enumerate(MESES_5):
        meta  = metas[i]; fat = fats[i]; dev = devs[i]; mg = mgs[i]
        dias  = DIAS_MES[mes]
        decor = DIAS_EL if mes == CUR_MONTH else dias
        medDia = round(fat / decor) if decor else 0
        proj   = round(medDia * dias) if mes == CUR_MONTH else fat
        rows.append({"month": mes, "meta": meta, "fat": fat, "dev": dev,
                     "mg": mg, "medDia": medDia, "proj": proj})
    return rows

def make_m25(metas, fats, mgs):
    rows = []
    for i, mes in enumerate(MESES_5):
        meta = metas[i]; fat = fats[i]; mg = mgs[i]
        rows.append({"month": mes, "meta": meta, "fat": fat, "mg": mg,
                     "ating": round(fat / meta * 100, 1) if meta else 0})
    return rows

def make_clients(client_defs, hist):
    cur_fats  = hist[CUR_MONTH]
    prev_mes  = MESES_5[MESES_5.index(CUR_MONTH) - 1]
    prev_fats = hist[prev_mes]
    result = []
    for i, (name, city, mg) in enumerate(client_defs):
        fat_cur  = cur_fats[i]
        fat_prev = prev_fats[i]
        medDia   = round(fat_cur / DIAS_EL) if DIAS_EL else 0
        proj     = round(medDia * DIAS_TOT)
        entry = {"name": name, "city": city, "mg": mg,
                 "dev": 0, "medDia": medDia, "proj": proj,
                 "curFat": fat_cur, "prevFat": fat_prev}
        for mes in MESES_5:
            entry[mes.lower()] = hist[mes][i]
        result.append(entry)
    result.sort(key=lambda x: x["curFat"], reverse=True)
    return result

def make_cats(cat_list):
    return [{"name": n, "total": tot, "curFat": cur, "mg": mg, "m26": m26}
            for n, tot, cur, mg, m26 in cat_list]

def cm26(vals):
    return [{"month": m, "fat": v} for m, v in zip(MESES_5, vals) if v > 0]

def build_vendor(name, code, m26, m25, clients, cats):
    tot_fat  = sum(m["fat"] for m in m26)
    tot_meta = sum(m["meta"] for m in m26)
    return {"name": name, "code": code,
            "curMonth": CUR_MONTH, "daysEl": DIAS_EL, "daysTotal": DIAS_TOT,
            "ating": round(tot_fat / tot_meta * 100, 1) if tot_meta else 0,
            "m26": m26, "clients": clients, "cats": cats, "m25": m25,
            "devClients": {}, "filial": "01", "senha": code + "@"}

# ──────────────────────────────────────────────────────────────────────────────
# VENDOR 1 — ANDERSON SILVA  (SP Capital)
# ──────────────────────────────────────────────────────────────────────────────

def vendor_anderson():
    m26 = make_m26(
        metas=[320000, 320000, 330000, 320000, 320000],
        fats= [298400, 315200, 341600, 308800, 184500],
        devs= [  3200,   2100,   4100,   2800,   1200],
        mgs=  [  18.2,   18.8,   18.5,   19.0,   18.7])
    m25 = make_m25(
        metas=[285000, 285000, 290000, 285000, 285000],
        fats= [271200, 288400, 301600, 278000, 166200],
        mgs=  [  17.1,   17.8,   17.5,   17.9,   17.6])
    defs = [
        ("DROGARIA VIDA SAUDÁVEL",  "São Paulo",   19.2),
        ("FARMÁCIA POPULAR SP",     "São Paulo",   18.5),
        ("DROGARIA CENTRAL SUL",    "São Paulo",   19.8),
        ("ULTRAFARMA CONSOLAÇÃO",   "São Paulo",   18.0),
        ("FARMÁCIA DO POVO",        "São Paulo",   19.5),
        ("DROGARIA SÃO LUCAS",      "São Paulo",   18.3),
        ("FARMÁCIA NATIVA",         "Guarulhos",   18.9),
        ("DROGARIA MASTER",         "Guarulhos",   17.8),
        ("FARMÁCIA NOSSA SAÚDE",    "Guarulhos",   18.6),
        ("DROGARIA PLUS FARMA",     "Guarulhos",   18.1),
        ("FARMÁCIA REDE SAÚDE",     "São Paulo",   19.0),
        ("DROGARIA EXPRESSA",       "São Paulo",   17.5),
        ("FARMÁCIA BELA SAÚDE",     "Guarulhos",   18.4),
        ("DROGARIA NOVA ERA",       "São Paulo",   18.7),
    ]
    hist = {
        "Jan": [42000, 35000, 30000, 28000, 25000, 22000, 18500, 16000, 14200, 12500, 10800, 9200, 8100, 7100],
        "Fev": [44000, 36500, 31500, 29000, 26200, 23000, 19200, 16700, 14800, 13000, 11200, 9600, 8400, 7300],
        "Mar": [47500, 39000, 34000, 31200, 28000, 24800, 20500, 17800, 15800, 13900, 12000, 10300, 9000, 7900],
        "Abr": [43000, 35800, 30800, 28500, 25600, 22500, 18900, 16400, 14500, 12800, 11000, 9400, 8200, 7200],
        "Mai": [26000, 21500, 18500, 17000, 15300, 13500, 11400, 9800, 8700, 7700, 6600, 5700, 4900, 4300],
    }
    cats = make_cats([
        ("MED. GENÉRICOS",   620000,  76000, 18.5, cm26([122000, 128000, 138000, 124000, 76000])),
        ("MED. REFERÊNCIA",  430000,  52000, 19.2, cm26([ 84000,  88500,  96000,  87000, 52000])),
        ("OTC / SIMILARES",  260000,  32000, 17.8, cm26([ 51000,  53500,  58000,  52500, 32000])),
        ("DERMOCOSMÉTICOS",  155000,  19000, 20.5, cm26([ 30000,  31500,  34500,  31000, 19000])),
        ("HIGIENE E BELEZA",  83000,  10200, 16.8, cm26([ 16200,  17000,  18500,  16800, 10200])),
    ])
    return build_vendor("Anderson Silva", "001", m26, m25, make_clients(defs, hist), cats)

# ──────────────────────────────────────────────────────────────────────────────
# VENDOR 2 — CAMILA FERREIRA  (Interior SP)
# ──────────────────────────────────────────────────────────────────────────────

def vendor_camila():
    m26 = make_m26(
        metas=[240000, 240000, 240000, 240000, 240000],
        fats= [224800, 251200, 236400, 246000, 147600],
        devs= [  2400,   1800,   3000,   2200,    900],
        mgs=  [  19.5,   19.9,   19.3,   20.1,   19.8])
    m25 = make_m25(
        metas=[215000, 215000, 215000, 215000, 215000],
        fats= [204400, 229200, 217600, 228800, 136800],
        mgs=  [  18.3,   18.9,   18.6,   19.1,   18.8])
    defs = [
        ("DROGARIA CAMPINAS NORTE",  "Campinas",        20.2),
        ("FARMÁCIA SAÚDE TOTAL",     "Campinas",        19.6),
        ("DROGARIA RIBEIRÃO MALL",   "Ribeirão Preto",  20.5),
        ("FARMÁCIA BOA ESPERANÇA",   "Ribeirão Preto",  19.1),
        ("DROGARIA SOROCABA CENTER", "Sorocaba",        20.0),
        ("FARMÁCIA POPULAR INTER",   "Campinas",        18.8),
        ("DROGARIA JUNDIAÍ FARMA",   "Jundiaí",         19.8),
        ("FARMÁCIA VIDA PLENA",      "Ribeirão Preto",  19.3),
        ("DROGARIA SANTA CRUZ",      "Sorocaba",        19.6),
        ("FARMÁCIA PRIME",           "Campinas",        20.3),
        ("DROGARIA MODERNA",         "Jundiaí",         18.9),
        ("FARMÁCIA NATURAL CURE",    "Ribeirão Preto",  19.4),
        ("DROGARIA TOTAL FARMA",     "Sorocaba",        19.0),
        ("FARMÁCIA EXCELÊNCIA",      "Campinas",        20.1),
        ("DROGARIA BEM ESTAR",       "Jundiaí",         19.5),
        ("FARMÁCIA CENTRO SAÚDE",    "Ribeirão Preto",  18.7),
    ]
    hist = {
        "Jan": [24000, 20500, 18500, 16800, 15200, 13500, 12200, 10800, 9600, 8600, 7800, 7000, 6300, 5700, 5100, 4500],
        "Fev": [26800, 22800, 20600, 18800, 16900, 15100, 13600, 12000, 10700, 9600, 8700, 7800, 7000, 6300, 5700, 5000],
        "Mar": [25200, 21500, 19400, 17600, 15900, 14200, 12800, 11300, 10100, 9100, 8200, 7400, 6600, 6000, 5400, 4700],
        "Abr": [26400, 22500, 20300, 18500, 16700, 14900, 13400, 11900, 10600, 9500, 8600, 7700, 6900, 6200, 5600, 4900],
        "Mai": [15800, 13500, 12200, 11100, 10000, 8900, 8000, 7100, 6400, 5700, 5200, 4600, 4100, 3700, 3400, 2900],
    }
    cats = make_cats([
        ("MED. GENÉRICOS",   468000,  58000, 19.5, cm26([ 92000,  102000,  96000,  100000,  58000])),
        ("MED. REFERÊNCIA",  323000,  40000, 20.3, cm26([ 63000,   70500,  66000,   68500,  40000])),
        ("SUPLEMENTOS",      165000,  20400, 22.8, cm26([ 32000,   35800,  33700,   35000,  20400])),
        ("OTC / SIMILARES",  112000,  14000, 18.5, cm26([ 22000,   24600,  23100,   24000,  14000])),
        ("DERMOCOSMÉTICOS",   90000,  11200, 21.5, cm26([ 17500,   19500,  18400,   19000,  11200])),
        ("HIGIENE E BELEZA",  42000,   4000, 17.2, cm26([  8300,    9300,   8700,    9000,   4000])),
    ])
    return build_vendor("Camila Ferreira", "002", m26, m25, make_clients(defs, hist), cats)

# ──────────────────────────────────────────────────────────────────────────────
# VENDOR 3 — RODRIGO COSTA  (ABC/Santos)
# ──────────────────────────────────────────────────────────────────────────────

def vendor_rodrigo():
    m26 = make_m26(
        metas=[185000, 185000, 185000, 185000, 185000],
        fats= [172400, 179600, 192800, 181200, 108600],
        devs= [  1800,   1200,   2400,   1600,    700],
        mgs=  [  18.8,   19.2,   18.9,   19.5,   19.1])
    m25 = make_m25(
        metas=[165000, 165000, 165000, 165000, 165000],
        fats= [156800, 163600, 174400, 165200,  98800],
        mgs=  [  17.7,   18.1,   17.9,   18.4,   18.0])
    defs = [
        ("DROGARIA ABC FARMA",      "Santo André",   19.5),
        ("FARMÁCIA GRANDE ABC",     "Santo André",   18.8),
        ("DROGARIA SANTOS MARE",    "Santos",        20.0),
        ("FARMÁCIA LITORAL",        "Santos",        19.2),
        ("DROGARIA SÃO BERNARDO",   "São Bernardo",  18.6),
        ("FARMÁCIA SAÚDE ABC",      "São Caetano",   19.8),
        ("DROGARIA MAUÁ PLUS",      "Mauá",          18.4),
        ("FARMÁCIA REGIONAL",       "Santo André",   19.0),
        ("DROGARIA BAIXADA",        "Santos",        18.7),
        ("FARMÁCIA REDE ABC",       "São Bernardo",  19.3),
        ("DROGARIA EXPRESS ABC",    "Santo André",   18.2),
        ("FARMÁCIA BOM REMÉDIO",    "São Caetano",   19.6),
    ]
    hist = {
        "Jan": [26000, 22000, 18500, 16000, 14000, 12500, 11200, 10000, 9000, 8100, 7300, 6600],
        "Fev": [27200, 23000, 19400, 16800, 14700, 13100, 11700, 10500, 9400, 8500, 7600, 6900],
        "Mar": [29500, 24800, 20900, 18100, 15800, 14100, 12600, 11300, 10100, 9100, 8200, 7400],
        "Abr": [27400, 23200, 19600, 17000, 14900, 13300, 11900, 10600, 9500, 8600, 7700, 7000],
        "Mai": [16500, 13900, 11800, 10200, 8900,  8000,  7100,  6400,  5700, 5200, 4600, 4200],
    }
    cats = make_cats([
        ("MED. GENÉRICOS",  358000,  44500, 18.8, cm26([ 70000,  72500,  78000,  71500,  44500])),
        ("MED. REFERÊNCIA", 248000,  30800, 19.6, cm26([ 48000,  50200,  54000,  49500,  30800])),
        ("OTC / SIMILARES", 152000,  18900, 18.1, cm26([ 29500,  30700,  33000,  30300,  18900])),
        ("HIGIENE E BELEZA", 96000,  11800, 17.5, cm26([ 18500,  19200,  20700,  19000,  11800])),
        ("DERMOCOSMÉTICOS",  80800,  10000, 21.0, cm26([ 15500,  16000,  17100,  15700,  10000])),
        ("VETERINÁRIOS",     39600,   4800, 20.5, cm26([  7900,   8000,   8500,   7800,   4800])),
    ])
    return build_vendor("Rodrigo Costa", "003", m26, m25, make_clients(defs, hist), cats)

# ──────────────────────────────────────────────────────────────────────────────
# VENDOR 4 — TATIANA ALVES  (MG/RJ)
# ──────────────────────────────────────────────────────────────────────────────

def vendor_tatiana():
    m26 = make_m26(
        metas=[275000, 275000, 275000, 275000, 275000],
        fats= [261200, 284800, 269600, 292400, 175200],
        devs= [  2800,   2000,   3400,   2600,   1100],
        mgs=  [  20.1,   20.5,   19.8,   20.8,   20.4])
    m25 = make_m25(
        metas=[245000, 245000, 245000, 245000, 245000],
        fats= [236400, 259600, 247200, 268000, 159600],
        mgs=  [  19.0,   19.5,   19.2,   19.8,   19.4])
    defs = [
        ("DROGARIA MINAS GERAIS",   "Belo Horizonte", 20.8),
        ("FARMÁCIA CONTAGEM",       "Contagem",       20.2),
        ("DROGARIA NOVA BH",        "Belo Horizonte", 21.0),
        ("FARMÁCIA RIO FARMA",      "Rio de Janeiro", 20.5),
        ("DROGARIA ZONA SUL RJ",    "Rio de Janeiro", 21.3),
        ("FARMÁCIA COPACABANA",     "Rio de Janeiro", 20.9),
        ("DROGARIA BH NORTE",       "Belo Horizonte", 19.8),
        ("FARMÁCIA PRIME MG",       "Contagem",       20.6),
        ("DROGARIA CENTRO RJ",      "Rio de Janeiro", 20.1),
        ("FARMÁCIA SAÚDE MG",       "Belo Horizonte", 20.4),
        ("DROGARIA MEIER",          "Rio de Janeiro", 19.7),
        ("FARMÁCIA NITERÓI",        "Niterói",        20.3),
        ("DROGARIA BELORIZONTINA",  "Belo Horizonte", 20.0),
        ("FARMÁCIA BARRA DA TIJUCA","Rio de Janeiro", 21.5),
        ("DROGARIA CONTAGEM PLUS",  "Contagem",       19.9),
    ]
    hist = {
        "Jan": [32000, 26500, 24000, 22000, 19500, 17500, 15500, 14000, 12500, 11200, 10100, 9100, 8200, 7400, 6700],
        "Fev": [35000, 29000, 26200, 24000, 21300, 19200, 16900, 15300, 13700, 12200, 11000, 9900, 8900, 8000, 7300],
        "Mar": [33000, 27300, 24700, 22600, 20100, 18100, 15900, 14400, 12900, 11500, 10400, 9300, 8400, 7600, 6800],
        "Abr": [36800, 30500, 27600, 25300, 22400, 20200, 17800, 16100, 14400, 12800, 11600, 10400, 9400, 8500, 7600],
        "Mai": [22000, 18300, 16600, 15200, 13400, 12100, 10700, 9700, 8600, 7700, 6900, 6200, 5600, 5100, 4600],
    }
    cats = make_cats([
        ("MED. GENÉRICOS",   567000,  70000, 20.1, cm26([111000, 121000, 114500, 124000,  70000])),
        ("MED. REFERÊNCIA",  392000,  48400, 21.0, cm26([ 76500,  83500,  79200,  85800,  48400])),
        ("SUPLEMENTOS",      215000,  26500, 23.5, cm26([ 42000,  45900,  43400,  47200,  26500])),
        ("OTC / SIMILARES",  148000,  18200, 19.3, cm26([ 28800,  31400,  29800,  32300,  18200])),
        ("DERMOCOSMÉTICOS",  118000,  14500, 22.0, cm26([ 23000,  25100,  23800,  25600,  14500])),
        ("HIGIENE E BELEZA",  62000,   7600, 17.9, cm26([ 12000,  13200,  12500,  13500,   7600])),
        ("VETERINÁRIOS",      30000,   3700, 21.2, cm26([  5900,   6400,   6100,   6600,   3700])),
    ])
    return build_vendor("Tatiana Alves", "004", m26, m25, make_clients(defs, hist), cats)

# ──────────────────────────────────────────────────────────────────────────────
# DIRETOR — consolida todos os vendedores
# ──────────────────────────────────────────────────────────────────────────────

def build_director(todos):
    por_mes26 = defaultdict(lambda: {"meta":0,"fat":0,"dev":0,"_wmg":0,"proj":0,"medDia":0})
    for d in todos.values():
        for m in d["m26"]:
            pm = por_mes26[m["month"]]
            pm["meta"]   += m["meta"]; pm["fat"]    += m["fat"]
            pm["dev"]    += m["dev"];  pm["_wmg"]   += m["fat"] * m["mg"]
            pm["proj"]   += m["proj"]; pm["medDia"] += m["medDia"]
    m26 = []
    for mes in MESES_5:
        if mes not in por_mes26: continue
        v = por_mes26[mes]; fat = v["fat"]
        m26.append({"month": mes, "meta": round(v["meta"]), "fat": round(fat),
                    "dev": round(v["dev"]), "mg": round(v["_wmg"]/fat, 1) if fat else 0,
                    "medDia": round(v["medDia"]), "proj": round(v["proj"])})

    por_mes25 = defaultdict(lambda: {"meta":0,"fat":0,"_wmg":0})
    for d in todos.values():
        for m in d["m25"]:
            pm = por_mes25[m["month"]]
            pm["meta"] += m["meta"]; pm["fat"] += m["fat"]
            pm["_wmg"] += m["fat"] * m["mg"]
    m25 = []
    for mes in MESES_5:
        if mes not in por_mes25: continue
        v = por_mes25[mes]; fat = v["fat"]
        m25.append({"month": mes, "meta": round(v["meta"]), "fat": round(fat),
                    "mg": round(v["_wmg"]/fat, 1) if fat else 0,
                    "ating": round(fat/v["meta"]*100, 1) if v["meta"] else 0})

    por_cat = defaultdict(lambda: {"tot":0,"cur":0,"_wmg":0,"meses":defaultdict(float)})
    for d in todos.values():
        for cat in d["cats"]:
            pc = por_cat[cat["name"]]
            pc["tot"]  += cat["total"]; pc["cur"]  += cat["curFat"]
            pc["_wmg"] += cat["total"] * cat["mg"]
            for entry in cat["m26"]:
                pc["meses"][entry["month"]] += entry["fat"]
    categories = []
    for name, v in sorted(por_cat.items(), key=lambda x: x[1]["tot"], reverse=True):
        fat_t = v["tot"]
        cat_m = [{"month": mes, "fat": round(v["meses"][mes])} for mes in MESES_5 if v["meses"].get(mes, 0) > 0]
        categories.append({"name": name, "total": round(fat_t), "curFat": round(v["cur"]),
                           "mg": round(v["_wmg"]/fat_t, 1) if fat_t else 0, "m26": cat_m})

    cli_unif = defaultdict(lambda: {"fat":0,"dev":0,"_wmg":0,"city":"","prevFat":0,"m26":defaultdict(float)})
    for d in todos.values():
        for c in d["clients"]:
            key = c["name"].upper().strip()
            cu = cli_unif[key]
            cu["fat"]     += c["curFat"]; cu["dev"]     += c["dev"]
            cu["_wmg"]    += c["curFat"] * c["mg"];  cu["prevFat"] += c["prevFat"]
            if not cu["city"] and c["city"]: cu["city"] = c["city"]
            for mes in MESES_5:
                v = c.get(mes.lower(), 0)
                if v: cu["m26"][mes] += v
    top_clients = []
    for name, v in sorted(cli_unif.items(), key=lambda x: sum(x[1]["m26"].values()), reverse=True)[:30]:
        fat_acum = sum(v["m26"].values())
        if fat_acum < 1000: continue
        fat_cur = v["fat"]
        cli_m = [{"month": mes, "fat": round(v["m26"][mes])} for mes in MESES_5 if v["m26"].get(mes, 0) > 0]
        top_clients.append({"name": name[:40], "city": v["city"][:25], "fat": round(fat_acum),
                            "curFat": round(fat_cur), "mg": round(v["_wmg"]/fat_cur, 1) if fat_cur else 0,
                            "dev": round(v["dev"]), "prevFat": round(v["prevFat"]), "m26": cli_m})

    por_cidade = defaultdict(lambda: defaultdict(float))
    for d in todos.values():
        for c in d["clients"]:
            city = c["city"].strip()
            if not city: continue
            for mes in MESES_5:
                v = c.get(mes.lower(), 0)
                if v: por_cidade[city][mes] += v
    cities = []
    for city, md in sorted(por_cidade.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]:
        fat_total = sum(md.values())
        cur_fat   = md.get(CUR_MONTH, 0)
        c_m26     = [{"month": mes, "fat": round(md[mes])} for mes in MESES_5 if mes in md]
        cities.append({"name": city[:30], "fat": round(fat_total), "curFat": round(cur_fat), "m26": c_m26})

    vendors = []
    for d in sorted(todos.values(), key=lambda x: sum(m["fat"] for m in x["m26"]), reverse=True):
        vendors.append({"name": d["name"], "code": d["code"], "curMonth": d["curMonth"],
                        "ating": d["ating"], "totalClients": len(d["clients"]),
                        "m26": d["m26"], "cats": d["cats"][:8], "clients": d["clients"][:30]})

    total_clients = sum(1 for v in cli_unif.values() if sum(v["m26"].values()) > 0)
    return {"m26": m26, "m25": m25, "categories": categories, "topClients": top_clients,
            "cities": cities, "vendors": vendors, "devClients": {}, "curMonth": CUR_MONTH,
            "totalClients": total_clients}

# ──────────────────────────────────────────────────────────────────────────────
# PATCHES DE DEMO
# ──────────────────────────────────────────────────────────────────────────────

DEMO_CSS = """
<style id="demo-style">
#demo-banner{
  position:fixed;top:0;left:50%;transform:translateX(-50%);z-index:9999;
  background:linear-gradient(90deg,#0d1b2a,#1b263b);
  color:#fff;padding:7px 14px;border-radius:0 0 14px 14px;
  font-size:11px;font-weight:700;
  display:flex;align-items:center;gap:8px;
  box-shadow:0 2px 16px rgba(0,0,0,.5);white-space:nowrap;
  border-bottom:2px solid var(--primary,#00D68F)
}
#demo-banner .db-label{color:var(--primary,#00D68F);letter-spacing:.6px}
#demo-banner .db-sep{color:#333}
#demo-banner button{
  background:rgba(0,214,143,.12);border:1px solid rgba(0,214,143,.35);
  color:#00D68F;padding:3px 10px;border-radius:20px;
  font-size:10px;font-weight:700;cursor:pointer;transition:background .15s
}
#demo-banner button:hover{background:rgba(0,214,143,.28)}
#demo-banner button.active{background:rgba(0,214,143,.32);border-color:#00D68F}
#demo-banner .db-vend-sel{
  position:absolute;top:38px;left:50%;transform:translateX(-50%);
  background:#141926;border:1px solid #1E2B40;border-radius:10px;
  padding:6px 0;min-width:200px;box-shadow:0 4px 20px rgba(0,0,0,.6);
  display:none;z-index:10000
}
#demo-banner .db-vend-sel.open{display:block}
#demo-banner .db-vend-sel button{
  display:block;width:100%;border:none;border-radius:0;background:none;
  color:#E8EDF5;padding:9px 16px;font-size:12px;text-align:left;
  border-bottom:1px solid #1E2B40
}
#demo-banner .db-vend-sel button:last-child{border-bottom:none}
#demo-banner .db-vend-sel button:hover{background:rgba(0,214,143,.08);color:#00D68F}
.hdr{top:36px !important}
</style>
"""

DEMO_JS = """
<script id="demo-script">
(function() {
  var VENDOR_CODES = ["001","002","003","004"];
  var VENDOR_NAMES = {
    "001": "Anderson Silva",
    "002": "Camila Ferreira",
    "003": "Rodrigo Costa",
    "004": "Tatiana Alves"
  };
  var vendDropOpen = false;

  function createBanner() {
    var b = document.createElement('div');
    b.id = 'demo-banner';
    b.innerHTML =
      '<span class="db-label">&#128138; DEMO</span>' +
      '<span class="db-sep">|</span>' +
      '<span style="color:#7A8AA0;font-size:10px">FarmaCenter Distribuidora</span>' +
      '<span class="db-sep">|</span>' +
      '<button id="db-btn-dir" onclick="demoBootDir()">&#127970; Diretoria</button>' +
      '<button id="db-btn-vend" onclick="demoToggleVend()">&#128100; Representante &#9660;</button>' +
      '<div class="db-vend-sel" id="db-vend-drop"></div>';
    document.body.appendChild(b);

    var drop = document.getElementById('db-vend-drop');
    VENDOR_CODES.forEach(function(cod) {
      var btn = document.createElement('button');
      btn.textContent = VENDOR_NAMES[cod];
      btn.onclick = function() { demoBootVend(cod); };
      drop.appendChild(btn);
    });

    document.addEventListener('click', function(e) {
      if (!e.target.closest('#demo-banner')) {
        document.getElementById('db-vend-drop').classList.remove('open');
        vendDropOpen = false;
      }
    });
  }

  window.demoBootDir = function() {
    document.getElementById('db-vend-drop').classList.remove('open');
    vendDropOpen = false;
    document.getElementById('db-btn-dir').classList.add('active');
    document.getElementById('db-btn-vend').classList.remove('active');
    bootDir('demo');
  };

  window.demoBootVend = function(cod) {
    document.getElementById('db-vend-drop').classList.remove('open');
    vendDropOpen = false;
    document.getElementById('db-btn-dir').classList.remove('active');
    document.getElementById('db-btn-vend').classList.add('active');
    bootData(VENDORS_DATA[cod]);
  };

  window.demoToggleVend = function() {
    vendDropOpen = !vendDropOpen;
    var drop = document.getElementById('db-vend-drop');
    if (vendDropOpen) drop.classList.add('open');
    else drop.classList.remove('open');
  };

  window.addEventListener('DOMContentLoaded', function() {
    createBanner();
    demoBootDir();
  });
})();
</script>
"""

CAT_METAS_DEMO = """const CAT_METAS = [
  { name: 'MED. GENÉRICOS',  pct: 0.40 },
  { name: 'MED. REFERÊNCIA', pct: 0.28 },
  { name: 'OTC / SIMILARES', pct: 0.14 },
  { name: 'DERMOCOSMÉTICOS', pct: 0.08 },
  { name: 'SUPLEMENTOS',     pct: 0.06 },
  { name: 'HIGIENE E BELEZA',pct: 0.03 },
  { name: 'VETERINÁRIOS',    pct: 0.01 },
];"""

CAT_METAS_ORIG = """const CAT_METAS = [
  { name: 'CONSERVAS',              pct: 0.60 },
  { name: 'MOLHOS E TEMPEROS',      pct: 0.30 },
  { name: 'CEREAIS',                pct: 0.04 },
  { name: 'DOCES E GELEIAS',        pct: 0.02 },
  { name: 'ACUCARES E CONFEITARIA', pct: 0.02 },
  { name: 'EMPORIO - REVENDA',      pct: 0.02 },
];"""

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"✗ Template não encontrado: {TEMPLATE_FILE}")
        return

    print("⚙️  Gerando dados demo — segmento farmacêutico...")
    todos = {
        "001": vendor_anderson(),
        "002": vendor_camila(),
        "003": vendor_rodrigo(),
        "004": vendor_tatiana(),
    }
    dir_data   = build_director(todos)
    dir_logins = {"demo": "demo123"}

    print("📝 Lendo template...")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    vendors_json  = json.dumps(todos,       ensure_ascii=False, separators=(',', ':'))
    director_json = json.dumps(dir_data,    ensure_ascii=False, separators=(',', ':'))
    logins_json   = json.dumps(dir_logins,  ensure_ascii=False, separators=(',', ':'))

    html = html.replace(
        "const VENDORS_DATA = {}; /* GERADO POR gerar_html.py */",
        f"const VENDORS_DATA = {vendors_json}; /* DEMO */")
    html = html.replace(
        "const DIRECTOR_DATA = {}; /* GERADO POR gerar_html.py */",
        f"const DIRECTOR_DATA = {director_json}; /* DEMO */")
    html = html.replace(
        "const DIR_LOGINS = {}; /* GERADO POR gerar_html.py */",
        f"const DIR_LOGINS = {logins_json}; /* DEMO */")
    html = html.replace("DATA_ATUALIZACAO", "Demo — FarmaCenter Distribuidora")

    html = html.replace(CAT_METAS_ORIG, CAT_METAS_DEMO)
    html = html.replace(
        "<title>Agente Fábrica</title>",
        "<title>InfoVendas Demo — FarmaCenter Distribuidora</title>")
    html = html.replace(
        '<div class="screen active" id="login">',
        '<div class="screen" id="login">')
    html = html.replace("</head>", DEMO_CSS + "</head>")
    html = html.replace("</body>", DEMO_JS + "</body>")

    print("💾 Salvando demo.html...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Demo farmacêutico gerado com sucesso!")
    print(f"   Arquivo: {OUTPUT_FILE}")
    print(f"   Tamanho: {os.path.getsize(OUTPUT_FILE)/1024:.0f} KB")
    print(f"\n📊 Representantes:")
    for cod, d in todos.items():
        tot = sum(m["fat"] for m in d["m26"])
        print(f"   [{cod}] {d['name']:<18} R${tot/1000:>6.0f}k | {len(d['clients'])} clientes | ating {d['ating']}%")
    print(f"\n🏢 Diretoria consolidada:")
    print(f"   {len(dir_data['vendors'])} representantes | {len(dir_data['categories'])} categorias | "
          f"{len(dir_data['topClients'])} top clientes | {len(dir_data['cities'])} cidades")
    print(f"\n🚀 Para abrir: abra demo.html no navegador")
    print(f"   Para hospedar: arraste demo.html no Vercel ou GitHub Pages")

if __name__ == "__main__":
    main()
