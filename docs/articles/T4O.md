# T4.O — A falha também tem uma arquitetura

**Estado:** resultados exatos de síntese e comparação física; contribuição metodológica e aplicada com condições explícitas.

> Dois circuitos com a mesma tabela lógica e o mesmo número de portas podem transformar o mesmo conhecimento em riscos diferentes.

## Motivação

A v13 construiu um circuito para atualizar conhecimento. Agora as próprias portas podem falhar. Importa não só o erro de cada peça, mas quais sinais compartilham uma falha e onde ela muda a decisão futura.

## Definições mínimas

|Símbolo|Interpretação|
|---|---|
|p|Erro por bit na memória anterior|
|gamma|Inversão na saída de cada NAND|
|q|Erro da nova célula de comando|
|K|Capacidade de0 a4 portas|
|Lei conjunta|Probabilidades de todas as combinações dos sinais acessíveis|

## Formulação

```text
P(saída=1 | x) = soma_k N[x,k] gamma^k (1-gamma)^(d-k).
```

N[x,k] conta exatamente os padrões com k falhas que produzem saída1 na entrada x. A síntese combina o código e a rede usando o valor físico das continuações, não a quantidade de linhas lógicas corretas.

## Exemplo

Com p=gamma=1%, dois circuitos de quatro NANDs computam a mesma função ideal. Um produz sobrevivência80,8821%, pior que o comando fixo80,9178%. O outro chega a80,9194%. O ganho é pequeno; a separação é estrita e não acrescenta portas ou dados.

Os rastros mostram que duas falhas intermediárias muito prejudiciais no primeiro circuito têm consequências menores no segundo. A sensibilidade total em ruído zero muda de−0,064656 para−0,025822.

## O que foi demonstrado

Enumeramos12.395 netlists,611 leis completas por custo e39.104 pares código/canal sem reutilizar a poda por função ideal. Um circuito é globalmente ótimo em p=1% e gamma entre0 e1%;8.854 desigualdades exatas certificam todo o intervalo.

Fora dele, os controles exploram a biblioteca completa em ponto flutuante; o Python verifica parâmetros racionais exatamente. Não há alegação de certificado contínuo de toda a superfície2D.

## O que habilita depois?

Preservar a lei conjunta das portas acessíveis permite compor corretamente novos estágios. O próximo alvo é reduzir essa assinatura conforme as continuações relevantes e cobrar pela manutenção dos mecanismos compartilhados.

## Limite físico

Acima de um limiar de erro independente na última porta, nenhuma melhoria só na lógica anterior supera o comando fixo neste contrato. Para p=1%, o limiar é aproximadamente1,1824%. Votação, saídas adicionais ou um mecanismo fail-silent alteram a hipótese e precisam ser implementados e custeados.

## Simulador e referências

[Laboratório](../lab/faulty_update.html) · [Provas](../results/T4O-stochastic-physical-boundaries.md) · [Consolidação v9–v14](../synthesis/finite-core-v9-v14.md).

O instrumento antecedente mais direto são as matrizes de transferência probabilísticas de Krishnaswamy, Viamontes, Markov e Hayes. A adaptação CDKA integra essa semântica à síntese física ponderada pelas consequências das decisões.
