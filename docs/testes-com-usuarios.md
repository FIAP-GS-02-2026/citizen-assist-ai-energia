# Testes com usuários: orientações de energia

O teste foi feito junto com o teste do assistente de Python: cada pessoa de fora da equipe usou o Citizen Assist AI no terminal e fez pelo menos uma pergunta de energia. Nenhum nome, telefone, e-mail ou endereço foi registrado; cada pessoa aparece só como P1, P2, P3.

## Situações testadas

| # | Situação apresentada à pessoa | Pergunta que ela digitou (exata) | Orientação mostrada | Entendeu? | Ajudou? (s/n) |
| --- | --- | --- | --- | --- | --- |
| 1 | Você comprou um patinete elétrico e quer saber quanto vai gastar de luz. | | | | |
| 2 | Pensa em pôr placa solar em casa e quer saber se compensa para carregar a bike. | | | | |
| 3 | A bateria da bike estragou e você não sabe onde jogar. | | | | |
| 4 | Quer saber se precisa de CNH ou placa para andar de bike elétrica. | | | | |
| 5 | Quer saber se pode andar de patinete na calçada. | | | | |

Coluna "Entendeu?": a pessoa conseguiu explicar com as próprias palavras o que a resposta disse (sim, em parte, não).

## Comentários recebidos

- P1:
- P2:
- P3:

## Ajustes realizados a partir do teste

| Problema observado | Ajuste feito | Onde |
| --- | --- | --- |
| | | |

## Ajustes feitos antes do teste (medição da busca)

- Orientações 18 a 22: em 10 perguntas novas, escritas depois da escolha das palavras-chave, a busca acertou 8 (80%). As 2 falhas ("carregando" e "tirar carteira") viraram palavras-chave.
- Orientações 23 e 24: em 6 perguntas novas, a busca acertou 2 (33%). Três falhas vieram de palavras que a pessoa usa e a base não tinha ("encher a bateria", "sai mais barato", "estragou"); uma veio de "recarga", que também é palavra-chave da recarga do Bilhete Único. As formulações viraram palavras-chave, e as 14 perguntas de energia passaram a ser encontradas sem tirar acerto das perguntas de ônibus (107 de 109 na bateria do assistente, igual a antes).
