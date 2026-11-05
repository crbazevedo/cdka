# T4.S — Quando vale a pena deixar de escrever?

**Resultado:** seletor físico construído, prova de omissão sem perda no regime ideal, custo comparado e ruído tolerável certificado.

## Por que estudar isso?

Uma organização precisa de informação para decidir, mas adquirir e escrever informação também usa recursos. Às vezes o próximo passo já é imposto pelo orçamento. Se o dado será substituído antes de qualquer decisão que possa utilizá-lo, atualizá-lo agora pode ser trabalho dispensável.

## O menor caso

O sistema possui três células com um diagnóstico sobre sua própria saúde. Um reparo realizado a partir do saldo3 deixa saldo2. No ciclo seguinte, outra manutenção é impossível; depois de trabalhar corretamente, a organização atualiza o diagnóstico. O registro intermediário não decide nada nesse intervalo.

A regra física é `escrever = NAND(reparou, saldo_anterior_era_3)`. Ela precisa de uma porta, recebe somente sinais já disponíveis e não conhece a saúde oculta.

## A garantia

A diferença D entre escrever e reter satisfaz `D1=0` e `DQ=0`. A primeira identidade preserva a sobrevivência imediata; a segunda diz que a próxima transição elimina a diferença antes de ela ser usada. Isso prova igualdade de sobrevivência para todos os horizontes finitos, dentro do contrato declarado.

## O custo que faltava

Em oito ciclos, a média cai de8,5875 para7,8891 escritas por sistema inicialmente operante. Entretanto, a porta adicional é instalada e executada. O projeto compensa apenas se o preço das escritas poupadas ultrapassar o custo desse seletor.

Com preços ilustrativos de uma unidade por escrita,0,01 por execução de NAND e0,10 de instalação, o custo esperado cai6,0846%. Esses preços não são energia medida, nem alteram o saldo operacional do dispositivo.

## Falha não é uma categoria única

Um erro que provoca uma escrita extra numa ocasião dispensável gasta trabalho. Um erro que impede uma escrita necessária pode comprometer a próxima manutenção. Os rastros distinguem os dois.

Com0,5% de erro na NAND, a sobrevivência cai de91,74768% para91,74163%: perda de0,00605 ponto percentual. É menor que uma tolerância declarada de0,01 ponto. O custo esperado do exemplo cai6,4967%.

A fronteira exata desse limite é aproximadamente0,8252248% de erro por invocação, para o horizonte e o prior utilizados. A prova usa coeficientes racionais, não uma leitura do gráfico.

## O insight menos óbvio

Devolver ao saldo o recurso de uma escrita evitada pode mudar a ação seguinte. Então o dado anteriormente irrelevante pode voltar a importar. Economizar e usar a economia não são a mesma intervenção. A política precisa ser recompilada sob o novo saldo.

## Próximo resultado

Um compilador de trabalho necessário: selecionar aquisição, retenção, manutenção e o circuito que as coordena, preservando uma garantia explícita e pagando por toda a implementação.

[Provas e limites](../results/T4S-priced-selective-acquisition.md) · [Laboratório](../lab/selective_acquisition.html) · [Direção científica](../strategy/direction-v18.md).
