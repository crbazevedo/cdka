# T4.L — O que as estatísticas finais escondem

**Contribuição:** inspeção exata de rastros de controladores e três separações mecanísticas verificadas no CDKA.

## Motivação

Dois controladores podem terminar uma tarefa com o mesmo placar e deixar organizações diferentes para o próximo problema. Uma melhoria média pode ocultar prejuízo num contexto e vantagem maior em outro. Precisamos observar processos, não apenas outcomes.

## Definições mínimas

Rastro é a sequência de estados, sinais acessíveis, ações, recursos, falhas e pesos probabilísticos. A visão do controlador contém apenas sinais fisicamente disponíveis; a do pesquisador inclui estados ocultos sem entregá-los à política. Uma continuação é um programa executável depois do ponto observado. Massa viva conserva a probabilidade original; falhas nunca saem do denominador.

## Formulação

Dois programas Q_A,Q_B podem obedecer μQ_A1=μQ_B1, mas μQ_Av≠μQ_Bv para uma continuação executável v. Igualdade de um placar não implica equivalência de mecanismos ou futuras capacidades.

## Exemplos

Manutenção→manter e manutenção→manutenção sobrevivem às duas etapas com a mesma probabilidade: 78,6594%. O segundo deixa menos recurso, mas mais massa viva saudável. Ambos ainda pagam a mesma próxima observação; na terceira etapa atingem 73,7351% versus 71,0981%.

O diagnóstico intermediário era escrito em 01; uma inversão específica produzia 11 e selecionava o plano C. Escrevê-lo em 00 exige duas inversões para a mesma confusão. A rota passa de p(1−p) para p²: em p=10%, de 9% para 1%. Isso explica exatamente o ganho líquido de 0,40328 ponto percentual da v10.

O ganho é +0,45324 ponto no contexto degradado e −0,04996 ponto no saudável, ponderados por suas probabilidades. Não é uma melhoria uniforme.

## O que habilita em seguida

Descobrir assinaturas de continuação suficientes, distâncias físicas ponderadas pelo dano às decisões e os pontos exatos onde memória deixa de sustentar o futuro. O próximo compilador deve otimizar representação e atualização com esses certificados e com circuitos realizáveis.

## Limites

As intervenções preservam modelo e evento. Atribuir a uma trajetória individual a condição de 'salva' exige um acoplamento causal entre mundos, não identificado por marginais. As etiquetas de falha mostram a primeira verificação que falhou, não uma causa única.

## Simulador

[Inspecionar os 984 rastros completos](../lab/trace_explorer.html). Dataset congelado em p=10%; o controle de ruído modifica somente a análise algébrica identificada. Exportação dos rastros filtrados conserva probabilidades exatas e falhas.

[Provas](../results/T4L-trace-guided-discovery.md) · [Estratégia](../strategy/proof-engine-v11.md).
