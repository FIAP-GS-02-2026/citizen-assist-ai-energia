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

## Limitações do teste

- Só 2 perguntas de energia, de 2 das 3 pessoas.
- As perguntas foram sugeridas pela equipe.
- As orientações 23 (resultado desta análise) e 24 (descarte) foram criadas depois do teste e ainda não foram testadas com usuários.

## Medição da busca (antes e depois do teste)

- **Orientações 18 a 22:** em 10 perguntas novas, escritas depois da escolha das palavras-chave, a busca acertou 8 (80%). As 2 falhas ("carregando" e "tirar carteira") viraram palavras-chave.
- **Orientações 23 e 24:** em 6 perguntas novas, a busca acertou 2 antes do ajuste. As formulações que falharam viraram palavras-chave. A palavra "estragou" sozinha não entrou, porque faria "meu bilhete estragou" cair no descarte de bateria; entraram "patinete estragou" e "bike estragou".
- **Bateria inteira do assistente** (perguntas de ônibus e de energia): 121 de 123. As 2 falhas são de ônibus.
