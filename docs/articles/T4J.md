# T4.J — A mesma ação não significa o mesmo futuro

**Estado científico:** resultado exato para um modelo finito, usando ferramentas conhecidas de controle parcialmente observável. Não há reivindicação de originalidade.

## Pergunta

Quais diferenças um controlador precisa guardar quando duas situações pedem a mesma ação agora, mas podem exigir decisões distintas depois?

## Motivação

Na v8, um bit que separava vantagens positivas e negativas era suficiente para uma decisão. Nesta etapa usamos o mesmo mecanismo físico, mas examinamos duas operações sucessivas. Não basta que a compressão acerte a primeira resposta: ela precisa permitir a continuação.

## Definições mínimas

Um **diagnóstico** é um sinal real sobre saúde oculta. Um **código** é o estado físico em que esse sinal é armazenado. Um **plano de continuação** especifica a ação inicial e o que fazer após cada sinal físico observado no passo seguinte. A **perda de compressão** compara a sobrevivência com e sem agrupar diagnósticos no mesmo código.

O controlador observa seu código, a discordância das células, o recurso e o relógio. Ele não recebe a saúde oculta nem um posterior calculado pelo pesquisador.

## Resultado e exemplo

Enumeramos os 64 planos de duas etapas do modelo existente. Apenas três aparecem na envoltória ótima. Dois começam com manutenção do corretor, mas, se o registro seguinte estiver unânime, um mantém a informação e o outro a atualiza. Guardar apenas a ação inicial apagaria essa diferença.

No diagnóstico de referência, a sobrevivência ótima é 80,9178% com um estado de código, 82,0409% com dois e 82,0690% com três. Três estados são necessários para preservar exatamente o ótimo, mas o terceiro melhora o resultado em apenas **0,0281 ponto percentual**. Não concluímos que compense seu custo físico.

## Formulação

```text
Valor completo = soma_sinal máximo_plano valor(sinal, plano)
Valor comprimido = soma_código máximo_plano soma_sinais_no_código valor(sinal, plano)
Perda = Valor completo − Valor comprimido
```

A perda é zero exatamente quando todos os sinais agrupados admitem pelo menos um **mesmo plano completo ótimo**. Compartilhar a primeira ação não basta.

## O horizonte pode exigir menos memória

Em outro diagnóstico do mesmo sistema, duas classes são necessárias para o melhor desempenho de uma etapa, mas uma única classe basta para duas: todas as situações passam a favorecer o mesmo plano de manutenção. Isso não significa melhora do conhecimento ou que observar menos ajuda; o objetivo otimizado mudou. Preservar todos os objetivos anteriores seria outro requisito.

## A atualização também precisa ser possível

Se duas histórias foram comprimidas no mesmo código, recebem a mesma ação e o mesmo sinal novo, uma atualização determinística não pode recriar dois códigos diferentes. Guardar a diferença antes ou medi-la novamente são soluções físicas; consultar a história que já foi apagada não é.

## Papel no programa

Esta etapa liga representação mínima à implementação de uma sequência de decisões. A auditoria encontrou antecedentes diretos em compressão de POMDPs orientada a valor, estados informacionais aproximados e síntese de controladores finitos. O resultado é um instrumento verificável e um contraexemplo, não uma nova teoria geral.

## O que habilita em seguida

Calcular a capacidade e o custo mínimos de um registrador e de seu circuito de atualização para preservar uma tolerância de perda ao longo de várias manutenções. Primeiro é necessário restringir a biblioteca de programas fisicamente executáveis: memória disponível não cria um decodificador inexistente.

## Simulador e limites

[Laboratório interativo](../lab/continuation.html): envoltória dos planos, fronteira valor–memória e mapa horizonte–diagnóstico. O mapa usa números de um cálculo racional exato; os controles do navegador usam ponto flutuante. A memória diagnóstica é retida e o decodificador pertence à biblioteca declarada; seu custo energético e degradação não foram resolvidos aqui.

[Prova completa](../results/T4J-continuation-sufficient-interfaces.md) · [Plano v9](../strategy/proof-engine-v9.md)
