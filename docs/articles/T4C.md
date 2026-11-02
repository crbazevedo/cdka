# T4.C — Sobreviver em média não é proteger todas as situações

**Status:** modelo finito resolvido exatamente e verificado; utiliza teoria clássica de controle parcialmente observável. Não há reivindicação de um teorema original da agência.

## Motivação

Não basta reparar a memória uma vez. Um controlador precisa agir, recuperar recursos, reparar novamente e continuar escolhendo intervenções adequadas. O horizonte muda o problema: uma política que parece inteligente no curto prazo pode ser abandonada por um otimizador de desempenho médio no longo prazo.

## Organização mínima

O ambiente possui dois contextos, 0 ou 1, e exige a ação correspondente. O sistema sabe o contexto inicialmente. Em cada ciclo:

1. Escolhe um modo de reparo com base na memória que possui.
2. O reparo restaura o atuador e reescreve o bit, mas pode invertê-lo com probabilidade p.
3. Executa uma ação. Se acertar, recebe do ambiente o recurso para o próximo reparo; o comando fica fisicamente registrado. Se errar, falha definitivamente.

O controlador não recebe uma cópia invisível do mundo, do histórico ou de uma semente aleatória persistente.

## Resultado exato

Depois de n ciclos, a melhor garantia válida para **ambos** os contextos é `(1-p)^n`. Já a melhor sobrevivência **média** sobre contextos equiprováveis é `max(1/2,(1-p)^n)`.

Com 10% de erro por reparo, em seis ciclos ainda é melhor preservar a distinção: 53,14% de sobrevivência para cada contexto. Em sete ciclos essa probabilidade cai a 47,83%. Um otimizador da média passa a preferir sempre a mesma ação: protege um contexto perfeitamente e abandona o outro, obtendo média de 50%.

## O que estava oculto

O resultado não mostra que o sistema desenvolveu uma intenção de abandonar alguém. Mostra que a função de avaliação atribui o mesmo valor a distribuições de sucesso muito diferentes. A teoria precisa conservar o **perfil de viabilidade por contexto** antes de reduzi-lo a um número médio.

Também há um viés de seleção: entre os sobreviventes da política simétrica, a memória continua correta, com um bit. Mesmo assim, a probabilidade de sobreviver tende a zero. Memória correta entre sobreviventes não é evidência de continuidade organizacional.

## Recursos informacionais que não são equivalentes

Uma semente aleatória independente, mas fisicamente persistente, permite escolher uma vez qual contexto proteger para sempre. Isso pode elevar a garantia mínima para 50%. Moedas aleatórias novas a cada passo não fazem o mesmo. Um bit protegido que possa armazenar o próprio contexto seria ainda mais poderoso.

Portanto, quantos bits existem é apenas parte da pergunta. Importam também durabilidade, leitura, escrita e o momento em que cada variável pode influenciar as ações.

## Comportamento assintótico

No regime de reparos muito confiáveis e muitos ciclos, a escala relevante é `tau=n p`. A sobrevivência robusta aproxima `exp(-tau)`. A mudança da política média acontece perto de `tau=ln(2)`.

Para manter risco total abaixo de alpha, o modelo exige `p ≤ 1-(1-alpha)^(1/n)`. A capacidade física de produzir essa confiabilidade precisa entrar no modelo; não pode ser gratuita.

## O que habilita depois

Já temos uma ferramenta exata para procurar políticas que respeitem a memória física. A próxima investigação é deixar o controlador escolher quanto investir na confiabilidade do reparo, em novas observações ou em novos suportes de memória, com recursos que ele próprio precisa recuperar.

[Simulador e fronteira de viabilidade](../lab/policy_cuts.html#renewal) · [Formulação, provas e restrições](../results/T4C-recursive-physical-viability.md).
