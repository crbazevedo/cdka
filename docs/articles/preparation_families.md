# Históricos certificados e uma decisão comum executável

**5 de novembro de 2026 · R11/R14.** O compilador agora reduz os dois lados
da decisão: os históricos físicos compatíveis com a preparação e os programas
completos permitidos. A composição conserva arrependimento, fidelidade e
viabilidade conjunta, com testemunhas verificáveis. O controlador continua
executando um mesmo programa para toda a classe, sem receber a identidade do histórico oculto.

No maior caso medido, com 65.536 históricos e quatro atualizações obrigatórias
de continuação, o tempo completo caiu de **39,4172 s para 3,2447 s**: razão de
**12,1482** entre as medianas. O comparador percorre os históricos em fluxo,
recebe a mesma melhoria aritmética e produz as mesmas saídas compactas. A
prova cresce de 19.683 para 1.261.965 bytes. Os casos pequenos continuam
favorecendo a solução simples. [Medições](../data/preparation-family-benchmark.json)

## Motivação

As construções anteriores já reduziam os programas por dominância e os
sufixos pelos contextos ainda possíveis. Permaneciam todos os `2^h`
históricos de preparação. Uma representação de quatro coordenadas tornava
cada avaliação barata, mas não dispensava a enumeração.

A questão desta etapa foi preservar a decisão sobre toda a classe de
preparações sem construir cada histórico e sem exigir uma lista exponencial
de resultados informados. Isso exigiu uma garantia sobre a família inteira
e uma saída adequada: extremos por programa, escolhas comuns, testemunhas
físicas e consultas informadas individuais.
[Obrigação anterior](../strategy/suffix-context-integration.md)

## Contrato físico

O modelo mantém 16 estados físicos: saúde oculta do substrato e três células.
A aquisição usa uma única saída ruidosa de sensor, compartilhada pelas três
escritas. D atualiza as células por difusão; R executa o votador físico de seis
NANDs e reescreve seu resultado; M usa esse mesmo mecanismo falível para
acionar uma tentativa de manutenção pré-paga. A fonte H permanece oculta.

Após h operações de preparação D/R, um programa fixo realiza exatamente K
operações D/R e no máximo um M adicional. A tarefa é reproduzir H na leitura
terminal. A reserva comum de recursos e a fronteira de observação são as
herdadas. As coordenadas do avaliador, os históricos usados como testemunhas
e os pesos da prova não se tornam entradas do controlador.
[Contrato herdado](reachable_diagnosis.md)

## Definições e construção

O contraste das submedidas da fonte é `mu_1-mu_0=-x E`, com `x>=0`. As
operações ordinárias satisfazem identidades exatas `E K_a=A_a E`, com
transportes não negativos. Assim, acrescentar a operação a à direita de um
histórico atualiza sua assinatura por `x -> x A_a`.

Se P_t é o fecho convexo de todas as assinaturas alcançáveis após t passos,

\[
P_{t+1}=\operatorname{conv}(P_t A_D\cup P_t A_R).
\]

Em cada nível, o compilador gera somente os filhos D/R dos históricos
retidos. Para descartar um candidato x, fornece históricos efetivamente
gerados com assinaturas x_j e uma identidade

\[
x=\sum_j\alpha_jx_j,\qquad \alpha_j\ge0,\qquad\sum_j\alpha_j=1.
\]

A linearidade propaga essas identidades para o nível seguinte. A indução
prova que o fecho convexo retido é exatamente o original, inclusive para
descendentes que nunca foram enumerados. Cada testemunha pode usar até cinco
pontos em quatro coordenadas; isso não limita o número total de pontos
extremos ou o tamanho dos racionais.

A igualdade é entre assinaturas suficientes para a tarefa. Ela não afirma
igualdade entre as leis físicas completas. A prova também não cria misturas
de controladores: cada programa retido é uma palavra original executável.
[Prova](../results/preparation-family-proof.md)

## Por que a decisão é preservada

Para cada programa p, a fidelidade é afim na preparação:

\[
V_x(p)=\tfrac12-xq(p).
\]

Sua fidelidade mínima é, portanto, atingida em uma preparação retida. O
arrependimento compara o programa e seu melhor concorrente na **mesma**
preparação:

\[
R(p)=\max_x\max_q\bigl[V_x(q)-V_x(p)\bigr].
\]

Para cada par fixo p,q, a diferença também é afim. Trocar a ordem dos dois
máximos permite calcular o arrependimento apenas nos históricos retidos.
Isso conserva o melhor programa minimax, o melhor programa maximin e a
existência de pelo menos um programa comum que satisfaça simultaneamente um limite de
arrependimento e um piso de fidelidade.

O valor informado `B(x)=max_q V_x(q)` exige cuidado: ele é um máximo de funções
afins e, em geral, não é afim. Uma consulta propaga o histórico pedido e
avalia a fronteira certificada de programas. Ela não interpola máximos de
outros históricos.

O verificador composto começa pelos dados físicos. Confere a cobertura dos
programas, a cobertura das preparações, os limites universais de cada
programa retido e as histórias que atingem esses limites. Uma testemunha de
pior caso, isoladamente, não demonstra que outro programa não seja melhor.
[Implementação](../../cdka/preparation_pipeline.py)

## Redução de trabalho e resultados preservados

As contagens de candidatos abaixo são do nível final; incluem os candidatos
descartados nesse nível.

| h | Históricos originais | Filhos gerados | Históricos retidos |
|---:|---:|---:|---:|
| 4 | 16 | 16 | 13 |
| 8 | 256 | 70 | 45 |
| 12 | 4.096 | 182 | 107 |
| 16 | 65.536 | 348 | 199 |

Em h=16, os níveis juntos geram 1.867 candidatos. A prova final evita a
construção de 65.188 históricos naquele nível. Em h=12,K=12, a composição
retém 107 preparações e 37 programas: 3.959 avaliações para construir a
decisão, contra 151.552 no comparador que já reduz os programas.
[Dados exatos](../data/preparation-family-results.json)

O caso principal conserva os 384 valores herdados e suas decisões:

| Critério | Programa | Resultado |
|---|---|---:|
| Menor arrependimento máximo | DRDDM | 0,0025321961178476887 |
| Fidelidade mínima desse programa | DRDDM | 0,8491834489516084 |
| Maior fidelidade mínima | DDDDM | 0,8500277369367224 |
| Arrependimento ≤0,003 e fidelidade ≥0,85 | Nenhum programa | Inviável |

As comparações usam frações exatas. Os decimais são apenas apresentação.

## Custo completo e comparador fortalecido

Uma especialização exata representa cada preparação concreta por duas
amplitudes de saúde e o número de operações D desde o último R. As identidades
físicas são verificadas antes de usar essa representação. A especialização
foi dada aos dois métodos, inclusive à geração dos históricos do comparador.
Modelos incompatíveis continuam usando quatro coordenadas. A família tem
dimensão afim quatro já em h=3; não surgiu um quociente linear global de duas
dimensões.

O comparador percorre os históricos em profundidade e mantém uma linha de
valores. Ambos produzem os mesmos extremos, programas e respostas a consultas.
Cada amostra começa em processo novo e inclui construção física, aquisição,
codificação, descoberta, inicialização das bibliotecas numéricas quando
necessárias, serialização, verificação independente e respostas finais.

| h / K | Fluxo: mediana completa | Cobertura: mediana completa | Fluxo / cobertura |
|---|---:|---:|---:|
| 2 / 4 | 0,190955 s | 0,194190 s | 0,983343 |
| 8 / 4 | 0,308165 s | 0,673511 s | 0,457550 |
| 12 / 4 | 2,303078 s | 1,374275 s | 1,675849 |
| 16 / 4 | 39,417228 s | 3,244689 s | 12,148229 |
| 12 / 12 | 11,629173 s | 3,087869 s | 3,766084 |

São três observações por método e caso, com ordem alternada. O primeiro caso
tem intervalos sobrepostos; o segundo mostra uma perda clara. Os ganhos
maiores não estabelecem um limiar universal. O arquivo de medições conserva
amostras, componentes, intervalos e a soma de medianas, separada da mediana
dos tempos completos. [Protocolo e amostras](../data/preparation-family-benchmark.json)

O preço inclui a prova: em h=16,K=4, o certificado completo ocupa 1.261.965
bytes, contra 19.683 no fluxo. A prova de preparação contém racionais de até
2.821 bits. Menos históricos avaliados não significa menos memória residente,
complexidade polinomial ou maior fidelidade física.

## Falhas conservadas como evidência

**Combinação cônica sem massa um.** No controle com saúde inicialmente
degradada, a assinatura de RR é um múltiplo positivo da de DR, com coeficiente
menor que um. Aceitar essa identidade como cobertura aumenta falsamente a
melhor fidelidade mínima de 0,75304333 para 0,78715596 e declara viável um piso
intermediário impossível. A soma dos pesos precisa ser exatamente um.

**Interpolação do valor informado.** DD e DR preferem programas diferentes.
A média de seus melhores valores excede o melhor valor no ponto médio em
0,0015262078. Os valores dos programas individuais interpolam exatamente;
seu máximo não.

**Pior caso sem comparação global.** DDDDM tem uma testemunha válida de
arrependimento 0,0043670124, mas perde para DRDDM, com 0,0025321961. Além disso,
subtrair extremos atingidos em históricos diferentes atribui a DRDDM o
arrependimento falso de 0,0052113004.
[Reprodução dos controles](../data/preparation-family-controls.json)

## O que este fechamento habilita

A relação entre representação e decisão ficou completa para o contrato
declarado: a incerteza pode ser coberta sem listar seus membros, os programas
podem ser cobertos sem enumerar toda a gramática, e o resultado conserva uma
ação comum fisicamente permitida. A descoberta propõe; o verificador exato
reconstrói as obrigações locais e suas consequências globais.

Durante a publicação deste incremento, o estado canônico avançou para
[v17](../results/T4R-renewal-and-selected-memory.md) e executou, em seu modelo
recorrente distinto de 64 estados, a comparação entre adquirir um relatório
novo e reter o antigo. A família de emissão fresca de doze fases deixa de
representar a memória retida após seleção por ações, recursos e sobrevivência.
Uma redução por simetria com 48 estados continua válida. Isso não demonstra
que toda interface de valores de doze dimensões seja impossível, nem que 48
seja mínimo.

A integração reúne dois resultados com funções diferentes: cobertura exata
da decisão em um contrato fixo e um contraexemplo físico à reutilização de
uma representação quando a gramática muda. O próximo passo foi atualizado
para consolidar e auditar o [núcleo do manuscrito](../strategy/realizable-renewable-core.md),
antes de ampliar o seletor físico de observações.
[Integração e continuidade](../strategy/preparation-family-integration.md)

## Reprodução

```bash
python -S -O -m experiments.preparation_family_sweep --check
python -S -O -m experiments.preparation_family_controls
python -S -O -m unittest discover -s tests -p 'test_preparation*.py'
python -m pip install -r requirements-suffix-discovery.txt
python -m experiments.preparation_family_sweep --write --check
python -m experiments.preparation_family_benchmark
```

O primeiro comando confere a biblioteca congelada sem solver, com enumeração
de referência até h=12 e verificação exata da cobertura e dos extremos em
h=16. A comparação integral com o fluxo em h=16 está nas execuções frescas do
benchmark. A descoberta numérica participa somente da construção da prova.
