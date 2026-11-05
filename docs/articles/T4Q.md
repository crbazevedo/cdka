# T4.Q — A máquina que decide quando se manter

**Contribuição:** um ciclo finito executável de diagnóstico, seleção falível de manutenção, recuperação, trabalho e financiamento da próxima operação; acompanhado de uma redução exata e de um limite de viabilidade.

> Como um mecanismo degradável escolhe a própria manutenção sem receber um diagnóstico perfeito ou recursos antecipados?

## Intuição e motivação

O seletor que interpreta um relatório de saúde também pode estar doente. Manter sempre desperdiça recursos e expõe equipamentos saudáveis ao risco de um procedimento. Nunca manter deixa a capacidade operacional se deteriorar. Precisamos avaliar a decisão, a implementação e os recursos no mesmo ciclo.

## Definições mínimas

Z é a saúde oculta de um banco de seis portas NAND. Três células guardam um diagnóstico ruidoso. b é o saldo de1 a4 tokens. Uma operação normal custa1; manutenção custa mais2. Somente uma tarefa correta retorna2 tokens. O banco que escolhe a manutenção também realiza a tarefa seguinte. O resultado do reparo não é revelado.

## Resultado

Em oito ciclos, na família declarada:

| Programa | Sobrevivência | Manutenções esperadas por sistema inicial |
|---|---:|---:|
| Sem manutenção |73,2597%|0|
| Manter sempre que houver recursos |91,1532%|3,8507|
| Usar o diagnóstico armazenado |**91,7477%**|**1,2734**|

Todos os16 programas estacionários da biblioteca foram comparados com frações exatas; a regra diagnóstica é a melhor nesse horizonte. Isso não é uma prova sobre todos os programas com memória ou todos os parâmetros.

## Por que funciona?

No caso estudado, manutenção prejudica a sobrevivência imediata de um banco saudável em0,4976 ponto percentual, por introduzir risco sem melhorar sua condição. Em um banco degradado, melhora-a em4,5523 pontos. O diagnóstico, embora falível e sujeito a obsolescência, permite reduzir serviços mal direcionados.

## A estrutura que evita enumerar cada trajetória

As atualizações escrevem uma nova família conhecida de distribuições de diagnóstico. Se E representa essa escrita e A_pi a operação antes dela, então

    K_pi=A_pi E,    M_pi=E A_pi,    E K_pi=M_pi E.

O processo físico de64 estados pode ser avaliado em12 fases. As fases preservam a dependência entre a saúde quando o diagnóstico foi escrito e a saúde atual. Não se tornam observações gratuitas para o agente.

## O que não segue do resultado

Recuperar recursos não garante sobrevivência infinita: toda tarefa ainda tem chance de erro fatal. Aqui, V_n≤0,9952703^n→0. O guardião de recursos e a interface de roteamento ainda são confiáveis por contrato. Não estamos demonstrando uma teoria universal de agência ou manutenção de toda a infraestrutura.

## Próximo passo

Comparar aquisição nova e retenção de memória sob o mesmo custo físico. Verificar quando o pequeno estado de avaliação continua fechado e retornar o menor rastro que força uma descrição maior.

## Simulador, prova e referências

[Laboratório](../lab/recurrent_maintenance.html) · [Prova completa](../results/T4Q-recurrent-maintenance-loop.md) · [Bússola dos aprendizados](../strategy/learning-compass-v16.md).

Antecedentes instrumentais: síntese de controladores finitos de POMDPs e inspeção/manutenção sob observação parcial. A adaptação executada incorpora a falibilidade do próprio seletor, um ciclo financiado por acertos e uma realização estocástica verificável.
