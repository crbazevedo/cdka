# Um orçamento comum muda o valor da informação

**15 de novembro de 2026 · SB · R11/R14.** Extensão executada da planta
recorrente v18, com um único recurso por trajetória e reutilização do banco
físico de NANDs. Síntese exata em uma biblioteca finita; preços ilustrativos,
sem alegação de medição de energia ou construção de hardware real.

[Laboratório](../lab/shared_budget.html) ·
[Contrato](../strategy/shared-budget-contract.md) ·
[Varredura exata](../data/shared-budget-results.json) ·
[Controles](../data/shared-budget-controls.json) ·
[Prova dos resíduos](../results/shared-budget-continuation.md) ·
[Revisão independente](../results/shared-budget-review.md).

## Pergunta e resultado

Determinar se a aquisição seletiva continua vantajosa quando seleção, serviço,
trabalho e escrita disputam a mesma reserva, e identificar quais certificados
de continuação sobrevivem a essa mudança.

O resultado principal é negativo e delimitado: **nos 16 pontos com preço
positivo por NAND, acrescentar um circuito de enable não melhora a máxima
probabilidade de completar oito tarefas ou oito ciclos**. Uma regra de
serviço que consulta apenas recursos, sem ler o diagnóstico, já atinge esses
ótimos. Ela está dentro da biblioteca original comparada. O custo mínimo nas
quatro tolerâncias de sobrevivência declaradas também é atingido sem NANDs
de enable nesses pontos.

Há dois ganhos estritos na grade, ambos com execução de NAND gratuita e
aquisição a seis quanta. Esses casos permanecem no resultado. Eles não
sustentam uma vantagem com execução paga. Também não se conclui que todo
circuito adicional seja dominado em toda a fronteira ou que informação seja
inútil em outros contratos.

## Motivação e continuidade

O [v18](../results/T4S-priced-selective-acquisition.md) já implementava um
enable falível e contabilizava sua instalação, invocação e escrita. Esses
custos pertenciam a uma segunda contabilidade esperada; o saldo operacional
não mudava quando uma escrita era omitida. Naquele contrato, a omissão ideal
após um serviço específico preservava sobrevivência em todo horizonte por
anulação das respostas de continuação.

Uma economia que altera o saldo pode mudar o próximo serviço admissível,
o momento de leitura do registro e a chance de completar o protocolo. O
próprio controle de reembolso do v18 já impedia transportar sua igualdade
sem nova prova. Esta etapa executa essa obrigação na mesma planta e audita
o resultado contra programas completos, inclusive os que dispensam
renovação e os que usam diretamente os sinais já disponíveis.

A distinção científica é entre três afirmações: uma operação pode ser
omitida sem alterar a tarefa; uma omissão pode melhorar um programa fixo;
um controlador que usa informação pode superar a melhor alternativa que
não a consulta. A primeira não implica a segunda sob outro orçamento, e a
segunda não estabelece a terceira.

## Definições mínimas e fronteira física

O estado reúne saúde oculta, três bits de diagnóstico e saldo inteiro.
O avaliador usa a simetria `(saúde, primeiro bit, soma dos outros dois, saldo)`,
com 1.164 rótulos para saldos de zero a 96. Essa é uma representação suficiente
do avaliador, sem prova de minimalidade e sem acesso gratuito do controlador
à saúde ou a uma distribuição posterior.

As probabilidades herdadas ficam fixas: erro de NAND saudável `1/1000`,
degradada `1/50`; erro de diagnóstico `3/20`; erro de sensor da tarefa
`1/50`; degradação `1/20`; restauração `4/5`; falha do procedimento `1/200`.
Cada tarefa tem uma nova fonte binária equiprovável. A retenção dos bits é
ideal dentro desta planta. Todas as taxas são hipóteses do modelo.

A preparação usa probabilidade inicial `1/2` para cada condição de saúde,
seguida do diagnóstico realmente adquirido sobre essa saúde. Os ótimos da
varredura são relativos a essa preparação fixa; não são garantias uniformes
sobre todas as leis iniciais de saúde e memória.

O recurso é fungível por hipótese; um token antigo corresponde a 24 quanta.

| Operação ou limite | Preço em quanta |
|---|---:|
| Capital inicial e capacidade | 96 |
| Comissionamento inicial | 24 |
| Trabalho obrigatório, antes do preço das portas | 24 |
| Serviço executado | 48 |
| Colheita após um ciclo completo | 48 |
| Cada NAND efetivamente invocada | `g` |
| Aquisição e escrita de um diagnóstico | `w` |
| Instalação de roteamento para `k` operações NAND | `k i` |

Todos os programas pagam preparação fresca. O saldo inicial disponível é
`72 − w − k i`. “Sem renovação” significa conservar esse registro inicial,
não recebê-lo gratuitamente. A comparação ainda não permite dispensar a
aquisição inicial quando um programa não usa o diagnóstico.

O mesmo banco de seis NANDs executa a seleção de manutenção, a tarefa e o
enable, sequencialmente. A seleção usa a saúde de entrada; trabalho e enable
usam a saúde posterior ao serviço. Novos erros são sorteados em cada
invocação, condicionados à saúde compartilhada. Um fanout reutiliza o mesmo
fio ruidoso. A lei conjunta preserva essas dependências.

Roteamento, relógio, taps, guarda de recursos, decodificador de saldo e
atuador de aquisição têm a fronteira idealizada explicitada no contrato.
O preço de instalação é de configuração dessa infraestrutura compartilhada;
não compra portas com saúde independente. O certificado algébrico não é uma
verificação de todos os componentes de um circuito eletrônico real.

## Eventos, acesso e término da tarefa

A tabela de manutenção usa três faixas, congeladas na entrada: abaixo de
72, omitir serviço; entre 72 e 95, aplicar `at3`; em 96, aplicar `at4`.
Cada uma das duas entradas programáveis escolhe entre omitir, servir,
votar e inverter o voto. O enable só recebe o serviço efetivamente executado
`r`, o sinal da faixa intermediária `x` e constantes zero e um.

A ordem é seleção paga, guarda de viabilidade, serviço e procedimento,
trabalho pago, enable pago, aquisição paga se solicitada, desgaste e
colheita. O guarda reserva serviço e trabalho. Ele não reserva uma escrita
hipotética nem transforma silenciosamente uma escrita impossível em retenção.
Uma etapa obrigatória sem recursos encerra o protocolo naquele ramo.

Para um ramo completo, com `n_s` portas de seleção, `k` portas de enable e
saída de enable `e`,

\[
b'=\min\{96,\ b-n_sg-48r-(24+6g)-kg-ew+48\}.
\]

Cada subtração deve ser viável antes da operação correspondente. A colheita
futura não pode financiar uma etapa anterior. Prefixos interrompidos conservam
seus gastos e recursos remanescentes. Em cada trajetória, e por agregação,

\[
\text{gasto}+\text{saldo final, inclusive em falhas}+\text{excedente descartado}
=96+\text{colheita}.
\]

Dois objetivos evitam um efeito artificial de término. O principal exige
sete ciclos completos e uma oitava tarefa, encerrando antes de enable,
aquisição, desgaste e colheita finais para **todos** os programas. O secundário
exige oito ciclos completos, incluindo sua fase final de aquisição ou
retenção. Nenhum deles representa uma agenda arbitrária de oito tarefas
com fallback ou omissões adicionais não previstas no programa.

## Cobertura exata e referências

A grade foi fixada antes dos resultados:

\[
g\in\{0,1,2\},\quad w\in\{0,6,12,24\},\quad i\in\{0,6\}.
\]

Em cada um dos 24 pontos são avaliadas as 16 tabelas de manutenção e todos
os netlists causais, enraizados e com até duas NANDs de enable. Há quatro
saídas sem portas, dez circuitos de uma porta e cinquenta de duas portas:
64 circuitos físicos e 1.024 combinações brutas. A equivalência exata de
perfil de falhas, preservando número de portas, reduz a avaliação a
`4 + 5 + 12 = 21` canais e **336 programas** por ponto e objetivo.

O perfil é uma identidade polinomial na taxa de erro; continua válido nas
duas taxas de saúde. Não se agrupam apenas tabelas verdade sem ruído. As
16.128 avaliações de programa, preço e objetivo usam aritmética racional,
com propagação por numeradores inteiros. Nenhuma ordenação depende de float.
Os decimais da apresentação são projeções dessas frações.

Cada referência é otimizada dentro de sua subfamília: sempre adquirir;
nunca renovar; zero NAND de enable, permitindo `0`, `1`, `r` ou `x`; a
NAND de omissão do v18; e nenhuma manutenção. Uma auditoria adicional
enumerou as quatro tabelas que usam somente omitir/servir com os 21
enables em todos os preços: 2.016 avaliações exatas do objetivo principal.

## Resultados numéricos

Os valores abaixo são probabilidades de completar oito tarefas. Para todos
os pontos com `g>0`, ambos os preços de instalação dão o mesmo ótimo, pois
um representante vencedor não instala enable.

| `g` | `w` | `i` | Melhor valor da biblioteca | Melhor sempre adquirir | Representante vencedor |
|---:|---:|---:|---:|---:|---|
| 0 | 0 | 0 ou 6 | 0,917476790 | 0,917476790 | Votar e sempre adquirir |
| 0 | 6 | 0 | 0,888658103 | 0,857305443 | Votar e usar NAND(1, serviço) |
| 0 | 6 | 6 | 0,887556150 | 0,857305443 | Votar e usar NAND(1, serviço) |
| 0 | 12 | 0 ou 6 | 0,886370642 | 0,828860913 | Serviço por saldo; não renovar |
| 0 | 24 | 0 ou 6 | 0,886370642 | 0,732597149 | Serviço por saldo; não renovar |
| 1 | 0 | 0 ou 6 | 0,884375058 | 0,884375058 | Serviço por saldo; não renovar |
| 1 | 6 | 0 ou 6 | 0,881327509 | 0,826768107 | Serviço por saldo; não renovar |
| 1 | 12 | 0 ou 6 | 0,877816288 | 0,770122088 | Serviço por saldo; não renovar |
| 1 | 24 | 0 ou 6 | 0,856541499 | 0 | Serviço por saldo; não renovar |
| 2 | 0 | 0 ou 6 | 0,871479968 | 0,871479968 | Serviço por saldo; não renovar |
| 2 | 6 | 0 ou 6 | 0,850150860 | 0,788480597 | Serviço por saldo; não renovar |
| 2 | 12 | 0 ou 6 | 0,850150860 | 0,732597149 | Serviço por saldo; não renovar |
| 2 | 24 | 0 ou 6 | 0,826768107 | 0 | Serviço por saldo; não renovar |

Com `g=0,w=6`, a NAND vencedora calcula a negação de serviço, sujeita ao
ruído físico. Ela é diferente da NAND de omissão do v18, que recebe também
o sinal de saldo. Seus ganhos sobre a melhor família sem NAND de enable
são **0,228746147** e **0,118550883 pontos percentuais**, para instalação
zero e seis. Para oito ciclos completos, o circuito vencedor pode mudar;
a varredura mantém os dois endpoints separadamente.

Nos 16 pontos de execução paga, o ganho de sobrevivência da biblioteca
completa sobre a melhor família sem NAND adicional é **exatamente zero**
em ambos os endpoints. Os minimizadores de gasto para perdas máximas de
zero, 0,01, 0,1 e 1 ponto percentual também usam zero NAND de enable.
Isso não implica dominância de todos os circuitos adicionais em regiões
de sobrevivência muito inferior; alguns permanecem na fronteira completa.

### A retenção vencedora não demonstra uso de conhecimento

Em 20 dos 24 pontos, a regra `service/service` com enable constante zero
atinge o ótimo. Ela não consulta os bits. O representante lexical do scan
é frequentemente `service/inverse:e00`, mas sua faixa de saldo cheio não
é alcançada: a entrada `inverse` nunca é executada. A revisão verifica
invocações de seleção **exatamente zero**, além da igualdade com o
representante explicitamente cego `service/service:e00`.

Por exemplo, com `g=1,w=6`, o saldo ao longo de um prefixo vivo é
`66,84,54,72,90,60,78,48`; a tarefa final termina antes da colheita.
O programa só usa o guarda de recursos e serviço fixo. Ele ainda paga a
aquisição inicial, por restrição da preparação comum desta experiência.
Esse custo obrigatório não fornece evidência de utilidade do registro.

## Exemplo concreto: uma melhoria real que perde para a referência forte

Fixando `vote/vote`, `g=1,w=6,i=0`, trocar renovação constante pela NAND de
omissão aumenta a sobrevivência em oito tarefas de **0,4457942473** para
**0,8233193314**. O gasto esperado aumenta de **266,6024180** para
**347,4569881** quanta, porque mais trajetórias sobrevivem e continuam a
consumir recursos. Portanto, menos escritas locais não significa menor
gasto total por sistema inicial.

A política cega admissível alcança **0,8813275089** nas mesmas condições.
A melhoria do par fixo é correta; usá-la para afirmar superioridade
informacional ou vantagem global do enable seria incorreto.

Um ramo menor mostra a cobrança física. Em saldo 90, voto solicitando
serviço, procedimento e tarefa corretos, NAND sem inversão: a renovação
constante termina o ciclo com 48 quanta; a NAND de omissão, com 53. A
economia líquida é cinco quanta, pois a porta custou um e a escrita evitada
custaria seis. Em saldo 84, o serviço e o trabalho esgotam a reserva; a
primeira alternativa não consegue escrever e a segunda não consegue
executar o enable. A colheita ainda não chegou.

## Certificar a continuação reconstruída

Sejam `Q` e `T` os kernels vivos de referência e candidato no novo estado
físico, `D=T−Q`, e `c_Q,c_T` os custos esperados imediatos, incluindo
prefixos que falham. Para resposta terminal `g` e custo terminal `b`,

\[
v_k=Q^kg,\qquad C_0=b,\qquad C_{k+1}=c_Q+QC_k.
\]

As identidades finitas exatas são

\[
T^ng-Q^ng=\sum_{j=0}^{n-1}T^jD v_{n-1-j},
\]

\[
C_{T,n}-C_{Q,n}
=\sum_{j=0}^{n-1}T^j[(c_T-c_Q)+D C_{n-1-j}].
\]

Mudanças de preparação paga e de etapa terminal acrescentam seus termos
de fronteira, implementados explicitamente. Para oito tarefas, `g` é a
resposta da tarefa final e existem sete transições ordinárias anteriores.

Resíduos de valor nulos em todos os horizontes até o limite certificam
igualdade naquele domínio. Resíduos de valor não negativos e de custo não
positivos fornecem condições suficientes de melhoria. Uma condição local
falhar não rejeita o programa: a soma exata propagada pode compensar
resíduos de sinais opostos. Domínios iniciais restritos exigem testemunhas
alcançáveis, não uma linha arbitrária de uma matriz maior.

### A anulação antiga falha num estado realmente alcançado

Um controle com enable ideal, `g=0,w=6,i=0`, isola o efeito do recurso.
Depois do primeiro ciclo, o estado `(saúde degradada, bits 111, saldo 84)`
tem probabilidade positiva sob a preparação comum. Nesse estado,

\[
D\mathbf1=0,\qquad Dg=0,\qquad DQg=0,
\qquad DQ^2g\approx0{,}2309032280>0.
\]

O exemplo envolve cinco tarefas totais: uma de preparação do estado
alcançado, a transição comparada e três tarefas restantes. A operação
atual e as continuações mais curtas não revelam a diferença; o recurso
altera a resposta posterior. Esse é um controle idealizado para o
mecanismo, distinto da biblioteca principal com saúde compartilhada.

No par físico compartilhado `g=1,w=6`, existe também um resíduo adverso
alcançável em horizonte curto, embora o candidato melhore o par em oito
tarefas. A evidência inclui respostas e custos de cada horizonte de um a
oito, conferidos por propagação direta independente da decomposição.

## O que esta etapa habilita e o que continua aberto

O orçamento comum fecha uma obrigação de realização: cada operação paga
seu custo antes da execução e a economia muda o estado futuro. A integração
formal identifica exatamente o erro de transportar uma interface antiga
para recursos novos. Ela também mostra por que gastos em falhas, término
da tarefa e preparação não podem ser detalhes externos ao certificado.

O resultado da síntese restringe a tese informacional. Nesta grade e classe,
a extensão paga de aquisição não supera um controle cego de recursos.
A existência de diagnóstico armazenado ou de auto-manutenção não basta
para atribuir valor operacional ao conhecimento.

**Próxima obrigação:** permitir explicitamente que uma preparação cega
dispense a aquisição inicial, cobrando o mesmo capital bruto, e medir o
valor causal do diagnóstico contra essa referência. O teste deve separar
observação útil, viabilidade por saldo e desperdício imposto pelo protocolo.
Expansão de circuitos e busca de preços favoráveis ficam suspensas até essa
comparação. O alvo é uma vantagem de decisão certificada contra uma
alternativa forte, não uma porcentagem obtida pela escolha de um comparador.

## Limites, antecedentes e reprodução

Resíduos telescópicos, subespaços invariantes e contabilidade por recompensas
são instrumentos estabelecidos; a contribuição desta etapa é sua adaptação
verificada ao contrato físico e aos contraexemplos concretos. Não há
alegação de prioridade de um teorema geral, ganho computacional, dimensão
mínima ou conclusão termodinâmica. Um controle algébrico separado mostra
que uma atualização de posto um pode ampliar uma interface de dimensão
dois até dimensão `N`; baixo posto inicial não garante fechamento pequeno.

A crítica é finita: taxas conhecidas, retenção ideal, preço fungível, guarda
e interfaces confiáveis, preparação inicial obrigatória, 16 tabelas
estacionárias, até duas NANDs de enable, oito etapas e 24 pontos discretos.
Outros preços, políticas com relógio, leitura mais rica de saldo, mudanças
de tarefa, limites de tempo ou custos de retenção exigem novos kernels e
comparações. Os resultados do modelo de fidelidade de 16 estados e dos
outros ramos computacionais do projeto conservam seus próprios contratos.

O [laboratório](../lab/shared_budget.html) permite mudar somente preços já
calculados, alternar endpoints e inspecionar uma trajetória de recursos.
Ele não interpola uma política, não sorteia evidência e não prova hardware.
O núcleo Python usa frações e o núcleo de apresentação usa inteiros para
o recurso; os gráficos são projeções de resultados certificados.

```bash
python -S -O -m experiments.shared_budget_sweep --check
python -S -O -m experiments.shared_budget_controls --check
python -S -O -m unittest discover -s tests -p 'test_shared_budget.py' -v
python -S -O -m unittest discover -s tests -p 'test_budget_continuation.py' -v
node --test tests/shared-budget-lab.test.mjs
```

A cobertura independente inclui enumeração de flags e células sem reutilizar
o compilador otimizado, trajetórias curtas com recursos em ramos interrompidos,
o limite gratuito de todos os 16 programas, a dependência de saúde, flags
novos por invocação, fronteiras de viabilidade, custos de instalação e a
justiça da etapa final. Os arquivos de dados guardam frações e hashes;
as condições e quantificadores acompanham cada conclusão.
