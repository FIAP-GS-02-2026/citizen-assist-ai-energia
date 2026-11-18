# Citizen Assist AI Mobilidade: energia na recarga de bike e patinete elétrico

Contribuição da disciplina **Soluções em Energias Renováveis e Sustentáveis** para o Citizen Assist AI Mobilidade, na Global Solution 2026.2 da FIAP (Ciência da Computação, turma 1CCR).

O assistente fica no repositório [citizen-assist-ai](https://github.com/FIAP-GS-02-2026/citizen-assist-ai). Este repositório traz a análise de energia que sustenta as orientações da categoria "Energia e mobilidade elétrica" desse assistente.

## Integrantes

| Nome | RM |
| --- | --- |
| Glauco Kelly | 572840 |
| Gabriel Fagundes | 569074 |
| Thiago Renatino | 569073 |

## Público e necessidade energética

**Público:** quem mora em São Paulo e usa bicicleta elétrica ou patinete elétrico para ir de casa até o ponto de ônibus e voltar. É o mesmo público do assistente, que orienta quem depende do ônibus municipal.

**Necessidade:** recarregar a bateria todo dia na tomada de casa. A pessoa não sabe quanto isso pesa na conta de luz, se a bandeira tarifária muda muito o valor, se vale pôr placa solar para isso e o que fazer com a bateria quando ela acaba.

**Como as orientações ajudam:** o assistente responde, em linguagem simples e com a fonte, quanto custa uma carga, quanto dá por ano, quando a Tarifa Branca ou a energia solar compensam e onde descartar a bateria. Tudo vem desta análise, com as premissas declaradas.

## Funcionalidades de energia no assistente

A categoria "Energia e mobilidade elétrica" do assistente tem 7 orientações. Todas mostram a fonte, a data de verificação e o aviso de que o assistente não é canal oficial. As orientações 18, 20 e 23 trazem os números desta análise; a 24 vem da recomendação 5; a 19 explica a bandeira usada na tabela de carga; a 21 e a 22 não entram nos cálculos, mas complementam o atendimento ao mesmo público (regras de placa, CNH e velocidade).

| id | Orientação | Base |
| --- | --- | --- |
| 18 | Quanto custa carregar bike ou patinete elétrico na tomada | Tarifa B1 da Enel SP + valor por carga desta análise |
| 19 | Bandeira tarifária: quando o kWh fica mais caro | ANEEL |
| 20 | Energia solar em casa: créditos na conta de luz e cobrança do Fio B | Lei 14.300/2022 |
| 21 | Bicicleta elétrica e patinete: precisa de placa ou CNH? | Resolução Contran 996/2023 |
| 22 | Velocidade de bike elétrica e patinete na ciclovia e na calçada | Prefeitura de São Paulo |
| 23 | Tomada ou energia solar: o que compensa para carregar bike e patinete | **resultado desta análise** |
| 24 | Onde descartar a bateria da bike ou do patinete elétrico | Lei 12.305/2010 |

As orientações 23 e 24 estão em [`integracao/orientacoes_novas.json`](integracao/orientacoes_novas.json), idênticas às que estão na base do assistente.

**Exemplo no assistente:**

```
Digite sua dúvida (0 para voltar): vale a pena carregar a bike com energia solar ou na tomada?
Confiança da resposta: ALTA (11 pontos)
>> Tomada ou energia solar: o que compensa para carregar bike e patinete [Energia e mobilidade elétrica]
Pela análise da equipe, rodando 6 km por dia, carregar na tomada custa perto de R$ 12 por ano na bike e
R$ 13 no patinete (uma carga completa: R$ 0,59 e R$ 0,21) e emite cerca de 0,7 kg de CO2 por ano, pelo
fator da rede de 2025 do MCTI. A Tarifa Branca economiza menos de R$ 2 por ano e vale para a casa toda.
A energia solar não emite na operação, mas só compensa como parte de um sistema da casa: a parte da bike
custa uns R$ 28 e se paga em 2,4 a 5 anos (até 7 nos cenários mais caros), porque a cobrança do Fio B
sobe até 2028 (Lei 14.300). Referências: tarifa da Enel, irradiação do SunData/CEPEL, emissões do MCTI e
Lei 14.300; o preço do painel é dado de mercado. São estimativas, não valores garantidos: dependem dos
impostos, da bandeira do mês e do seu uso.
```

## Como executar

Requer Python 3.9 ou superior e não usa bibliotecas externas.

```bash
python3 analise.py          # imprime a comparação e grava os CSVs em resultados/
python3 -m unittest -v      # 24 testes dos cálculos e dos dados
```

Para ver as orientações funcionando, rode o assistente no outro repositório (`python3 main.py`), escolha "2. Navegar por categorias" e depois "Energia e mobilidade elétrica", ou faça uma das perguntas do exemplo acima.

## Estrutura

```
citizen-assist-ai-energia/
├── README.md
├── analise.py                    comparação das alternativas e gravação dos resultados
├── energia.py                    fórmulas (energia, custo, potência solar, compensação, emissão)
├── dados/
│   ├── premissas.csv             cada número com unidade, tipo, fonte e período
│   ├── irradiacao_sao_paulo.csv  irradiação mês a mês (CRESESB SunData)
│   └── fator_emissao_sin.csv     fator de emissão do SIN mês a mês em 2025 (MCTI)
├── resultados/                   gerados por analise.py
│   ├── comparacao.csv
│   ├── recarga_completa.csv
│   ├── sensibilidade.csv
│   ├── sensibilidade_solar.csv
│   └── solar_mensal.csv
├── integracao/
│   └── orientacoes_novas.json    orientações 23 e 24 para o assistente
├── docs/
│   ├── fontes.md                 trechos de cada fonte, copiados da página
│   └── testes-com-usuarios.md    situações testadas, comentários e ajustes
└── tests/
    └── test_energia.py
```

## Dados e premissas

Período de referência comum: **12 meses**, para a mesma necessidade (mesma distância e mesmos dias de uso em todas as alternativas). Tarifas em vigor desde 04/07/2026. Unidades: Wh e kWh para energia, W e Wp para potência, R$/kWh para tarifa, kWh/m².dia para irradiação, kg de CO2 para emissão.

Cada linha de [`dados/premissas.csv`](dados/premissas.csv) diz de onde veio o número:

| Dado | Valor | Tipo | Origem |
| --- | --- | --- | --- |
| Tarifa B1 convencional (TUSD + TE) | 472,42 + 316,96 R$/MWh = R$ 0,789/kWh | oficial | Enel SP, REH ANEEL 3.596/2026 |
| Tarifa Branca B1, fora de ponta | 367,33 + 301,91 R$/MWh = R$ 0,669/kWh | oficial | Enel SP |
| Tarifa Branca B1, ponta | 997,85 + 482,45 R$/MWh = R$ 1,480/kWh | oficial | Enel SP |
| Bandeiras amarela, vermelha 1 e vermelha 2 | +0,01885, +0,04463 e +0,07877 R$/kWh | oficial | ANEEL |
| Bateria e autonomia da bike | 630 Wh, 80 km | fabricante | Caloi E-Vibe Explorer SUV (nível 1 de assistência) |
| Bateria e autonomia do patinete | 221 Wh, 25 km | fabricante | Xiaomi Electric Scooter 4 Lite (2ª geração) |
| Irradiação média em São Paulo, painel a 21° | 4,66 kWh/m².dia | oficial | CRESESB/CEPEL SunData (Atlas Solar INPE 2017) |
| Taxa de desempenho do sistema solar | 75% | referência técnica | Manual de Engenharia FV CEPEL/CRESESB: 70% a 80% |
| Parcela do Fio B cobrada em 2026 | 60% | oficial | Lei 14.300/2022, art. 27 |
| Fator de emissão do SIN em 2025 | 0,0461 tCO2/MWh | oficial | MCTI |
| Preço de sistema solar residencial | R$ 2,45/Wp | **mercado (estimado)** | Radar Solfácil, via Agência Cenário Energia |
| Eficiência do carregador | 85% | **premissa da equipe** | sem fonte para esses modelos; testada de 75% a 95% |
| Distância por dia | 6 km (3 de ida e 3 de volta) | **premissa da equipe** | testada de 2 a 20 km/dia |
| Dias de uso por ano | 264 (22 por mês) | **premissa da equipe** | dias úteis |

## Cálculos

1. **Consumo por km:** bateria ÷ autonomia. Bike: 630 Wh ÷ 80 km = 7,9 Wh/km. Patinete: 221 Wh ÷ 25 km = 8,8 Wh/km.
2. **Energia tirada da tomada:** a tomada entrega mais do que a bateria guarda, porque parte vira calor. Energia da tomada = energia na bateria ÷ eficiência. Uma carga completa da bike puxa 630 ÷ 0,85 = 741 Wh da tomada.
3. **Energia por ano:** Wh/km × km por dia × dias ÷ eficiência. Bike: 7,875 × 6 × 264 ÷ 0,85 = 14,7 kWh por ano.
4. **Custo:** kWh × (tarifa + acréscimo da bandeira).
5. **Potência solar necessária**, pela equação 6.28 do Manual CEPEL/CRESESB: P (Wp) = (E ÷ TD) ÷ HSP, com E em Wh/dia na média do ano. Bike: (40,2 Wh/dia ÷ 0,75) ÷ 4,66 h = 11,5 Wp.
6. **Valor de cada kWh solar compensado** num sistema novo: o art. 27 da Lei 14.300 manda cobrar sobre a energia compensada 60% do Fio B a partir de 2026, 75% a partir de 2027 e 90% a partir de 2028; de 2029 em diante vale a regra do art. 17, que a ANEEL ainda vai calcular. A tabela da Enel não separa o Fio B, por isso a conta sai como faixa. No pior caso, o Fio B é a TUSD inteira e o percentual sobe ano a ano: o kWh compensado vale R$ 0,506 em 2026, R$ 0,435 em 2027, R$ 0,364 em 2028 e R$ 0,317 de 2029 em diante (premissa da equipe: 100% da TUSD). No melhor caso, vale a tarifa inteira.
7. **Emissão:** kWh tirados da rede × fator de emissão do SIN. Na operação, a energia solar não emite.
8. **Retorno:** no melhor caso, investimento ÷ economia por ano. No pior caso, a economia de cada ano muda com o percentual do Fio B, e o retorno é o ano em que a economia acumulada paga o investimento. Sem juros nem reajuste.

## Resultados

**Carga completa (0 a 100%), tarifa convencional, sem tributos:**

| Veículo | kWh da tomada | Verde | Amarela | Vermelha 1 | Vermelha 2 |
| --- | --- | --- | --- | --- | --- |
| Bike (630 Wh) | 0,741 | R$ 0,59 | R$ 0,60 | R$ 0,62 | R$ 0,64 |
| Patinete (221 Wh) | 0,260 | R$ 0,21 | R$ 0,21 | R$ 0,22 | R$ 0,23 |

**Comparação em 12 meses, bike, 6 km por dia:**

| Alternativa | Custo por ano | Investimento | Retorno | CO2 por ano | Viabilidade |
| --- | --- | --- | --- | --- | --- |
| A) Tomada, tarifa convencional | R$ 11,58 | nenhum | não se aplica | 0,68 kg | Imediata, em qualquer tomada |
| B) Tomada, Tarifa Branca fora de ponta | R$ 9,82 | nenhum | não se aplica | 0,68 kg | Vale para a casa inteira; a ponta custa R$ 1,48/kWh |
| C) Solar em casa, sistema novo em 2026 | R$ 0,00 a R$ 4,16 em 2026 (até R$ 6,93 a partir de 2029) | R$ 28 (11,5 Wp) | 2,4 a 4,9 anos | 0 na operação | Só como parte de um sistema da casa |

No patinete os números são parecidos: R$ 13,00 por ano na tomada, R$ 11,02 na Tarifa Branca e R$ 32 de parcela solar, com o mesmo retorno.

**Sensibilidade** ([`resultados/sensibilidade.csv`](resultados/sensibilidade.csv) e [`resultados/sensibilidade_solar.csv`](resultados/sensibilidade_solar.csv)):

- Com 2 a 20 km por dia e eficiência de 75% a 95%, a bike custa de R$ 3,45 a R$ 43,76 por ano na tomada. Mesmo se impostos e outros itens dobrassem a conta, o maior valor ficaria abaixo de R$ 90 por ano.
- Com preço de R$ 2,08 a R$ 3,06 por Wp e taxa de desempenho de 70% a 80%, a parcela solar se paga em 3,7 a 7,0 anos no pior caso do Fio B.
- Mês a mês ([`resultados/solar_mensal.csv`](resultados/solar_mensal.csv)), a parcela solar gera menos que o consumo de abril a julho e em setembro (o mês mais fraco é junho, com 1,05 kWh para 1,22 kWh de consumo). A sobra dos outros meses vira crédito, que vale por 60 meses.

## Recomendações e justificativas

1. **Carregar na tomada de casa é barato e não precisa de mudança.** Custo: menos de R$ 1 por carga e perto de R$ 12 por ano. Viabilidade: total, sem investimento. Impacto: 0,68 kg de CO2 por ano, porque a rede brasileira emitiu em média 46 g de CO2 por kWh em 2025. É a recomendação para a maioria do público.
2. **A bandeira tarifária muda pouco o valor da carga.** Na vermelha 2, a carga da bike sobe de R$ 0,59 para R$ 0,64, e o ano passaria de R$ 11,58 para R$ 12,74 se a bandeira ficasse vermelha 2 o ano todo. Não vale mudar a rotina por causa da bandeira.
3. **Tarifa Branca não compensa só por causa da bike.** A economia é de R$ 1,76 por ano, e a adesão muda a conta da casa inteira: no horário de ponta o kWh custa R$ 1,48, quase o dobro da tarifa convencional. Só faz sentido para quem já concentra o consumo da casa fora da ponta. Fins de semana e feriados nacionais são sempre fora de ponta.
4. **Energia solar compensa como parte de um sistema da casa, não só para a bike.** A parcela da bike é pequena (11,5 Wp, cerca de R$ 28) e se paga em 2,4 a 4,9 anos (até 7 anos nos cenários mais caros), porque a cobrança do Fio B sobe até 2028. Sozinha, porém, não existe: um sistema tem custos fixos de projeto, inversor, instalação e pedido de acesso à Enel que esta conta não inclui. Exige telhado ou área própria; quem mora em apartamento pode participar de geração compartilhada ou de condomínio, previstas na Lei 14.300. O ganho ambiental é real, mas pequeno nessa escala: 0,68 kg de CO2 por ano por bike.
5. **A bateria não vai para o lixo comum.** Pela Lei 12.305/2010, quem vende pilhas e baterias tem de recebê-las de volta, e o consumidor deve devolvê-las ao comerciante ou distribuidor. O Manual CEPEL/CRESESB também alerta: "As baterias de Li-íon podem explodir ou incendiar".

**Coerência com o assistente:** a orientação 23 repete os números desta seção (R$ 12 por ano na bike e R$ 13 no patinete, R$ 0,59 e R$ 0,21 por carga, 0,7 kg de CO2 por ano, menos de R$ 2 de economia na Tarifa Branca, R$ 28 e 2,4 a 5 anos para a parcela solar, até 7 nos cenários mais caros), cita as referências, avisa que são estimativas e aponta para este repositório. A 18 traz o valor por carga com a perda no carregador, e a 20 traz a escala do Fio B. A 24 vem da recomendação 5.

## Limitações

- **Tarifas sem tributos.** Usamos a tarifa homologada pela ANEEL, publicada pela Enel sem ICMS, PIS e COFINS. Não achamos fonte oficial com a alíquota efetiva para a conta residencial em São Paulo, então não estimamos o valor com tributos. A sensibilidade mostra que, mesmo dobrando a conta, a conclusão não muda.
- **Fio B desconhecido.** A Enel não publica o Fio B separado na tabela, então a alternativa solar sai como faixa entre pior e melhor caso. A partir de 2029 a lei remete ao art. 17, ainda sem cálculo da ANEEL; no pior caso usamos 100% da TUSD.
- **Preço solar de mercado.** O R$ 2,45/Wp é média nacional de um levantamento privado, não um preço oficial; São Paulo não está entre os 10 estados mais baratos. O cálculo é proporcional e não inclui custos fixos.
- **Consumo de fabricante.** A autonomia da bike é a do nível 1 de assistência e a do patinete é o alcance máximo informado, ambas em condições de teste do fabricante; subida, peso e velocidade maior gastam mais. A sensibilidade de distância cobre parte disso.
- **Eficiência do carregador estimada.** Sem medição própria; usamos 85% e testamos de 75% a 95%.
- **Emissão só da operação.** Não calculamos a emissão de fabricar painéis, baterias ou a bike.
- **Horários da Tarifa Branca.** A página da Enel não informa os horários de ponta; a pessoa deve consultar a distribuidora.
- **Estimativas, não garantias.** Nenhum valor desta análise é garantido: dependem do uso, da conta da casa e das regras em vigor.

## Testes com usuários

O teste foi feito em 18/11/2026, presencial, com 3 pessoas de fora da equipe usando o assistente. Duas perguntas de energia foram feitas e as duas foram encontradas e ajudaram. A partir delas, a orientação 18 passou a mostrar o valor por carga, e não só a tarifa. Situações, comentários, ajustes e limitações do teste em [`docs/testes-com-usuarios.md`](docs/testes-com-usuarios.md).

## Referências

Trechos de cada fonte em [`docs/fontes.md`](docs/fontes.md).

- Enel SP, tarifas de energia elétrica: https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html
- ANEEL, bandeiras tarifárias: https://www.gov.br/aneel/pt-br/assuntos/tarifas/bandeiras-tarifarias
- ANEEL, Tarifa Branca: https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-branca
- ANEEL, geração distribuída: https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida
- Lei 14.300/2022: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm
- Lei 12.305/2010 (Política Nacional de Resíduos Sólidos): https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12305.htm
- CRESESB/CEPEL, SunData v3.0: https://cresesb.cepel.br/index.php?section=sundata
- CEPEL/CRESESB, Manual de Engenharia para Sistemas Fotovoltaicos (2014): https://cresesb.cepel.br/publicacoes/download/Manual_de_Engenharia_FV_2014.pdf
- MCTI, fatores de emissão de CO2 do SIN: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
- Caloi, E-Vibe Explorer SUV: https://caloi.com/?p=44373
- Xiaomi, Electric Scooter 4 Lite (2ª geração): https://www.mi.com/es/support/faq/details/KA-321368/
- Agência Cenário Energia, preço do watt-pico residencial (09/06/2026): https://cenarioenergia.com.br/2026/06/09/preco-do-watt-pico-residencial-recua-7-em-um-ano-e-abre-janela-de-oportunidade-na-mmgd/
- Resolução Contran 996/2023: https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao9962023.pdf/@@display-file/file
- Prefeitura de São Paulo, velocidade em ciclovias: https://prefeitura.sp.gov.br/w/prefeitura-limita-velocidade-de-bicicletas-el%C3%A9tricas-e-patinetes-a-20-km/h-em-ciclovias

## Vídeo técnico

*O link será adicionado após a gravação.*
