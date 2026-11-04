# T4.P — Corrigir também muda o que precisamos saber

**Contribuição:** uma interface estocástica reduzida e verificável para duas atualizações físicas, e uma comparação de redundância com manutenção paga.

## Intuição

Uma maioria lógica trata três votos igualmente. Um circuito concreto pode não tratá-los igualmente quando suas portas falham. O mecanismo que usamos para corrigir também determina quais diferenças precisamos conservar para prever sua continuação.

## Definições mínimas

O registro tem três bits a,b,c. Z é uma condição física oculta que altera o ruído das portas. Uma atualização pode deixar cada célula sofrer ruído, ou votar, replicar o resultado e reescrever as células. O avaliador conhece a lei de Z; a política não recebe seu valor.

## Formulação

Para o votador de seis NANDs estudado:

    P(saída=1 | 011) − P(saída=1 | 101)
      = 2gamma(1−gamma)(1−2gamma)^2.

As entradas têm a mesma maioria, mas são diferentes para o hardware falível. O resumo (Z,a+b+c) funciona para uma primitiva abstrata simétrica. No circuito físico, a interface exata precisa preservar (Z,a,b+c):16 estados físicos tornam-se12 classes que preservam todas as composições da gramática declarada.

## Exemplo e mecanismo

Três seletores de quatro portas e um votador de seis custam18 NANDs. Com erro de2% por porta, o conjunto perde para o comando fixo. Uma manutenção paga que recupera o votador com80% de chance o torna útil. Mas manter diretamente o seletor simples, com quatro portas, funciona melhor neste mesmo caso.

Não basta perguntar se a redundância corrige erros. Precisamos perguntar quanto custa manter o processo que decide qual resultado utilizar.

## O que habilita em seguida?

Uma política recorrente que decide quando operar e quando manter seu próprio seletor, usando somente registro físico e sinais disponíveis. A interface reduzida fornece a estrutura para evitar expandir todas as trajetórias.

## Simulador e limites

[Laboratório interativo](../lab/boundary_voting.html). A comparação cobre seis projetos, não todos os circuitos de18 portas. Os experimentos de redução e de controle compartilham o votador, mas ainda não constituem uma única organização recorrente completamente automantida.

## Provas e antecedentes

[Resultado técnico](../results/T4P-realized-correction-interfaces.md). Matrizes de transferência probabilísticas e agregação por simetria são os instrumentos; a adaptação ao contrato físico, a certificação e os contraexemplos compõem o avanço desta rodada.
