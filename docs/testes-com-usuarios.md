# Testes com usuários: orientações de energia

**Quando e como:** 18/11/2026, presencial, junto com o teste do assistente de Python. Três pessoas de fora da equipe usaram o Citizen Assist AI no terminal, cada uma numa sessão própria. Os atendimentos estão em `data/historico.json` do repositório [citizen-assist-ai](https://github.com/FIAP-GS-02-2026/citizen-assist-ai). Nenhum nome, telefone, e-mail ou endereço foi registrado; cada pessoa aparece só como P1, P2 e P3.

**Como as perguntas foram feitas:** a equipe sugeriu as primeiras perguntas de cada pessoa, que as digitou no assistente; a última pergunta de cada uma foi livre. Por isso o teste mede mais a utilidade e a compreensão das respostas do que a capacidade da busca de entender frases novas, que foi medida à parte (seção final).

## Situações de energia testadas

| Pessoa | Pergunta digitada (exata) | Orientação mostrada | Confiança | Ajudou? | Nota de facilidade da sessão |
| --- | --- | --- | --- | --- | --- |
| P1 | quanto gasta de luz pra carregar patinete elétrico? | 18. Quanto custa carregar bike ou patinete elétrico na tomada | ALTA (7 pontos) | sim | 4 de 5 |
| P2 | patinete elétrico precisa de placa? | 21. Bicicleta elétrica e patinete: precisa de placa ou CNH? | ALTA (6 pontos) | sim | 3 de 5 |
| P3 | (não fez pergunta de energia) | | | | 4 de 5 |

## Comentários recebidos

Nenhum comentário espontâneo foi registrado sobre as respostas de energia: as duas pessoas responderam que a orientação ajudou ("sim") e seguiram para a próxima pergunta. Como não houve comentário, os ajustes abaixo partiram da observação da equipe sobre a resposta exibida, não de fala dos participantes.

## Ajustes realizados a partir do teste

| Problema observado | Ajuste feito | Onde |
| --- | --- | --- |
| A resposta à pergunta de P1 ("quanto gasta de luz pra carregar patinete") trazia só a tarifa em R$ por MWh: a pessoa ainda teria de fazer a conta para saber quanto gasta. | A orientação 18 passou a dizer o valor de uma carga completa (cerca de R$ 0,59 na bike e R$ 0,21 no patinete) e que perto de 15% da energia vira calor no carregador. Foi criada a orientação 23, com o resultado da comparação tomada × Tarifa Branca × solar, e a 24, sobre descarte da bateria. | `data/base_conhecimento.json` do assistente, orientações 18, 23 e 24 |

## Segunda rodada: 19/11/2026

**Quando e como:** presencial, com 2 pessoas de fora da equipe, numa cópia do assistente com histórico vazio (para não misturar com os 11 atendimentos do teste de Python). As duas usaram a mesma sessão. A equipe mostrou 6 situações ("quero saber quanto pesa na conta carregar o patinete", "a bateria da bike morreu" etc.) e as pessoas digitaram as frases como foram mostradas: as perguntas são sugeridas pela equipe, não livres. Notas de facilidade: 5 (registrada pelo assistente ao sair) e 4 (dada de viva voz pela segunda pessoa). Nenhum comentário além das notas foi registrado.

| Pergunta digitada (exata) | Antes do ajuste | Ajudou? | Depois do ajuste |
| --- | --- | --- | --- |
| Quero saber quanto pesa na conta de luz carregar o patinete todo dia. | 18, ALTA (6 pontos) | sim | sem mudança |
| Estou pensando em pôr placa solar só para carregar a bike. Compensa? | 20 (créditos solares), ALTA (7); a 23 só como alternativa | sim | 23, ALTA (10 pontos) |
| A bateria da bike morreu. O que eu faço com ela? | não encontrou | não | 24, MÉDIA (5 pontos) |
| Ouvi falar de Tarifa Branca. Vale a pena para carregar a bike de noite? | **17, Rede Noturno de ônibus**, ALTA (6): resposta errada, marcada como "ajudou" | sim | 23, ALTA (11 pontos) |
| A conta de luz ficou mais cara este mês por causa da bandeira. Isso muda o custo da recarga? | 19, MÉDIA (5 pontos) | sim | sem mudança |
| Tenho placa solar em casa. Como funcionam os créditos na conta? | 20, ALTA (10 pontos) | sim | sem mudança |

**Ajustes feitos a partir desta rodada** (palavras-chave em `data/base_conhecimento.json` do assistente e em `integracao/orientacoes_novas.json`):

- Orientação 23: "so para carregar", "so pra carregar", "placa solar so", "vale a pena para carregar", "carregar a bike de noite" e "carregar o patinete de noite". A palavra "noite" puxava a Rede Noturno de ônibus; agora a pergunta sobre Tarifa Branca cai na análise.
- Orientação 24: "bateria morreu", "bateria da bike morreu", "bateria do patinete morreu" e "bateria da bicicleta morreu".
- As pontuações das perguntas usadas nos vídeos de Python e de SERS não mudaram, e os testes automatizados dos dois repositórios passam.

**O que esta rodada mostra:** a pessoa marcou "ajudou" numa resposta errada (Rede Noturno). A pergunta "ajudou?" sozinha não garante acerto; por isso a equipe conferiu cada resposta.

## Limitações do teste

- Só 2 perguntas de energia, de 2 das 3 pessoas.
- As perguntas foram sugeridas pela equipe.
- As orientações 23 (resultado desta análise) e 24 (descarte) foram criadas depois da primeira rodada e testadas na segunda (19/11/2026), com perguntas sugeridas pela equipe.

## Medição da busca (antes e depois do teste)

- **Orientações 18 a 22:** em 10 perguntas novas, escritas depois da escolha das palavras-chave, a busca acertou 8 (80%). As 2 falhas ("carregando" e "tirar carteira") viraram palavras-chave.
- **Orientações 23 e 24:** em 6 perguntas novas, a busca acertou 2 antes do ajuste. As formulações que falharam viraram palavras-chave. A palavra "estragou" sozinha não entrou, porque faria "meu bilhete estragou" cair no descarte de bateria; entraram "patinete estragou" e "bike estragou".
- **Bateria inteira do assistente** (perguntas de ônibus e de energia): 121 de 123. As 2 falhas são de ônibus.
