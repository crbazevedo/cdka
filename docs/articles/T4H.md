# T4.H / T3.G — Quando o diagnóstico correto não pode ser utilizado

**Status científico:** modelo finito resolvido, resultado de instrumentos conhecidos; originalidade não estabelecida.

> Uma organização deve conhecer a própria condição para escolher como agir, mas pode precisar gastar os recursos necessários à ação apenas para descobrir essa condição.

## Intuição

Um controlador de memória redundante possui dois regimes ocultos: saudável e degradado. No regime saudável, obter uma nova observação é mais vantajoso; no degradado, o mesmo procedimento pode introduzir erros, então manter os dados é melhor. O sistema pode medir a saúde, mas só utilizar essa distinção se possuir um circuito que converta o diagnóstico em uma ação e recursos para executá-la.

## Por que isso importa?

Informação fisicamente armazenada não é equivalente à possibilidade de executar uma política diferente. Ao tornar a saúde oculta, removemos a última hipótese de que o controlador recebe gratuitamente a avaliação de suas próprias capacidades. É o começo de uma teoria operacional de autorregulação, sem pressupor intenção.

## Definições mínimas

- `H`: saúde do mecanismo, 0 ou 1, oculta ao controlador.
- `Y`: bit diagnóstico, armazenado após pagar pela medição.
- `η`: probabilidade de erro da medição.
- `ν`: probabilidade de a saúde mudar antes da ação.
- `B`: recursos físicos; `d` paga a medição e `c` instala uma regra contingente.
- `g`: benefício de atualizar quando o corretor está saudável.
- `ℓ`: prejuízo de atualizar quando está degradado.

## Formulação

Para estados de saúde inicialmente equiprováveis e duas ações relevantes, com orçamento suficiente:

\[
\eta_{\rm efetivo}=\eta+\nu-2\eta\nu,\qquad
\Delta V=\tfrac12\max\{0,g-(g+\ell)\eta_{\rm efetivo}\}.
\]

O limiar calculado para o mecanismo do CDKA v6 é `19,416%` de erro efetivo. Abaixo dele, um seletor financiado pode usar a leitura; acima, a ação ótima ignora a leitura.

## Exemplo concreto

Com sensor perfeito, saúde equiprovável e `B=4`, o sucesso de um ciclo aumenta de `88,3319%` para `90,8930%`. Com `B=3`, o diagnóstico pode ser adquirido, mas a atualização física fica inacessível depois dos gastos de diagnóstico e seletor: ganho zero. Se a saúde muda durante o atraso, o diagnóstico pode estar correto sobre o passado e ser inútil no presente.

## Papel no programa

Liga a estatística de decisão de B1 aos cortes temporais T3.C, ao custo das políticas inteiras em T3.E e à manutenção falível em T4.G. O próximo alvo é um diagnóstico que precisa sobreviver à manutenção e um seletor cuja própria saúde se modifica, com uma política de memória física limitada.

## O que está e não está provado

**Provado no modelo:** fórmula de valor de diagnóstico, limiar exato, efeito do orçamento, decaimento por atraso e lacuna contra um controlador que observa diretamente a saúde. O solver exato foi comparado com enumeração independente.

**Não provado:** originalidade geral, intencionalidade emergente, conversão de tokens em energia, autonomia constitutiva ou validade do modelo de custos para circuitos reais.

## Simulador

[Explorar o laboratório](../lab/diagnosis.html) (quando servido como site estático). Ele mostra a estrutura das políticas viáveis, o mapa de fases orçamento×erro e a perda de valor por idade da observação.

## Derivações e fontes

- [Prova completa T4.H](../results/T4H-hidden-health-diagnosis.md).
- [Custo de seletor T3.G](../results/T3G-physical-selector-cost.md).
- [Lin, Song & Pozzi (2022), Value of Information](https://doi.org/10.1016/j.ress.2021.107944).
- [Winterer et al. (2024), Strong Simple Policies for POMDPs](https://doi.org/10.1007/s10009-024-00747-0).
