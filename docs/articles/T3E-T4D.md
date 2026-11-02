# T3.E / T4.D — O custo de conseguir escolher e continuar escolhendo

**Estado:** resultados exatos de um modelo explicitamente definido; instrumentos clássicos, originalidade não estabelecida.

## Pergunta e motivação

Um dispositivo pode executar duas ações e, mesmo assim, não conseguir escolher entre elas conforme a situação. E pode recuperar energia a cada acerto, mas perder sua chance de sobreviver depois de muitos ciclos. Queremos medir essas duas lacunas, não definir inteligência por uma recompensa conveniente.

## Definições mínimas

- **Política implementável:** uma regra inteira ligando estados legíveis a ações, realizável pelo mesmo mecanismo físico.
- **Seleção contingente:** diferença entre as probabilidades de escolher uma ação em dois estados; representada por sigma.
- **Fidelidade do reparo:** probabilidade de escrever o bit corretamente; o erro é p.
- **Viabilidade robusta:** garantia de sobrevivência para cada contexto, sem abandonar um deles para melhorar a média.
- **Esforço r:** recurso normalizado usado para tornar o seletor e a escrita mais confiáveis. Não significa automaticamente joules.

## Primeiro resultado: ações não são políticas

Dois aparelhos podem ter as ações 0 e 1 disponíveis em qualquer situação. Um só consegue manter um comando fixo; outro consegue executar 0 quando lê 0 e 1 quando lê 1. As possibilidades marginais são iguais, mas suas capacidades de regular o mundo são diferentes.

Sob uma restrição sigma na seleção e erro p na escrita, provamos a melhor sobrevivência robusta por ciclo:

    b = [1+(1-2p)sigma]/2.

O produto desses valores caracteriza o horizonte, na arquitetura declarada sem memória/aleatoriedade persistente adicional.

## Segundo resultado: precisão precisa ser produzida

No modelo, w unidades de esforço produzem sigma=1-exp(-w), e e unidades produzem p=.5exp(-e). Investir só em um dos dois mecanismos não melhora a garantia: ambos precisam funcionar. Para w+e=r, o ótimo de um ciclo divide r igualmente, resultando em

    q(r)=1-exp(-r/2)+.5exp(-r).

## Exemplo surpreendente: dividir pouco orçamento pode piorar

Com quatro ciclos e orçamento total R=1, distribuir 0,25 por ciclo resulta em sobrevivência de 6,60%. Concentrar o orçamento em um único ciclo resulta em 7,22%. Nenhuma das duas é uma boa garantia; a pergunta é qual escolha é melhor sob a escassez extrema.

Há uma prova, não apenas uma simulação: log q é convexo até r=1,06960. Quando todo o orçamento está nessa faixa, o máximo ocorre em um vértice do simplex — concentrar em um ciclo. Em regimes de alta confiabilidade, a concavidade inverte a conclusão e a divisão temporal uniforme é ótima.

## Terceiro resultado: recuperar recursos não elimina o risco acumulado

Se cada ação correta repõe h unidades, uma regra de reservatório pode alternar acumulação e ciclos bem financiados. Sua melhor taxa assintótica de sobrevivência é caracterizada pela envoltória côncava de log q. Para qualquer fluxo médio finito h, a probabilidade de sobreviver para sempre é zero nesta arquitetura com erros fatais.

Isso não é uma afirmação sobre toda vida ou agência. Redundância, erros toleráveis, reobservação, novos canais ou uma arquitetura de reparo diferente podem invalidar o modelo.

## Quanto custa uma garantia de 90%?

Para 10 ciclos, o mínimo é aproximadamente 91,06 unidades de esforço; para 100 ciclos, 1371,11. O crescimento assintótico é 2n log n para manter uma confiabilidade fixa. O coeficiente 2 reflete dois mecanismos igualmente calibrados — não é uma constante física universal.

## Papel no programa e próximo passo

T3.E formaliza a diferença entre comandos disponíveis e regras implementáveis. T4.D explicita o custo de tornar confiáveis as decisões repetidas. A próxima fronteira é permitir que a própria organização reconfigure seus canais de memória, seleção e reparo, mudando a arquitetura em vez de simplesmente gastar mais para melhorar uma arquitetura fixa.

## Simulador, provas e fontes

- [Laboratório interativo](../lab/implementability.html).
- [T3.E: hipóteses, prova e controles negativos](../results/T3E-implementable-prescriptions.md).
- [T4.D: recursos, envoltória e assintóticos](../results/T4D-produced-fidelity-budgets.md).
- [Estratégia de provas v4](../strategy/proof-engine-v4.md).
- [Polyanskiy e Wu: canais com restrições de custo](https://arxiv.org/abs/1405.3629).
- [Chatterjee e Varshney: energia e confiabilidade em circuitos](https://arxiv.org/abs/1607.03572).
