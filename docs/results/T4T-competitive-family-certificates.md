# T4.T — Certificados de continuações comuns: piloto competitivo

**2026-11-05, São Paulo.** Execução remota em 2026-11-06 às 01:28–01:30 UTC, ainda 5 de novembro no fuso do usuário. Ramo experimental `research/competitive-family-v19`; a main permanece na v18.

## 1. Classe escolhida e resultado executado

Alvo: **verificação exata de famílias de implementações estocásticas com a mesma restrição de continuação de baixo rank**, especialmente horizontes longos. Aquisição seletiva, variantes de memória e rotas regenerativas são candidatos de aplicação. O método atual certifica uma propriedade terminal; não resolve arbitrariamente toda síntese de políticas POMDP.

O piloto executou Storm via Stormpy2.0.0 no mesmo processo/máquina que nosso protótipo. Usou uma representação da FAMÍLIA inteira como MDP, não a enumeração de cada implementação. Em oito instâncias sintéticas, o ganho incluindo a compilação foi1,86–2,94× no horizonte10mil e16,54–26,22× no horizonte100mil. Em todos os horizontes sintéticos curtos8/1000 e no pequeno caso CDKA, o tempo total do protótipo foi pior. Estado da arte geral NÃO foi estabelecido.

A contribuição candidata é uma especialização certificada e competitiva, não uma alegação de que ferramentas algébricas clássicas foram inventadas aqui. Ela poderá servir de pré-processador de ferramentas existentes.

## 2. Enunciado e prova

Para cada estado vivo i existe um conjunto finito R_i de linhas racionais subestocásticas. Massa ausente significa falha absorvente. A família retangular permite escolher qualquer linha disponível por estado, inclusive escolhas dependentes do tempo, histórico ou aleatórias.

Seja Q o sistema de referência que escolhe a primeira linha de cada estado e g o observável terminal. Construa

    V=span{g,Qg,Q²g,...}, B=base independente de V,
    QB=BC, g=Bc.

São equivalentes:

1. Todas as seleções permitidas têm o mesmo valor terminal para todo estado inicial e todo horizonte finito.
2. Para todo i e toda r em R_i, (r−Q_i)B=0.

**Suficiência:** por indução reversa, todo valor de continuação pertence a V e todas as linhas locais agem igualmente sobre V. Mínimo, máximo e escolhas adaptativas coincidem. O valor comum de horizonte H é BC^Hc.

**Necessidade:** escolher uma linha alternativa uma vez, no estado i, e depois aplicar Q por k passos produz a exigência (r−Q_i)Q^k g=0. Valer para todo k equivale a anular V. QED.

Sob políticas físicas acopladas ou observação parcial, a família retangular pode ser uma RELAXAÇÃO. Aceitação certifica o subconjunto realizável; rejeição não demonstra impossibilidade de uma biblioteca menor. Nenhuma saúde oculta ou coordenada do avaliador é dada ao controlador.

Custos e outras propriedades não são preservados automaticamente: precisam ser incluídos no contrato e recertificados.

## 3. Algoritmo, complexidade e saída

O compilador recebe as linhas físicas, não uma base pronta. Gera Q^k g e conserva somente vetores independentes. Ao fechar a base, testa cada linha alternativa. Uma falha devolve estado, alternativa, horizonte e discrepância exata. Um limite de rank devolve UNKNOWN, não equivalência falsa.

Se N é o número de estados explícitos, L o total de entradas não nulas de todas as alternativas e d a dimensão de V:

- descoberta/verificação: O(Ld+Nd²) operações escalares;
- memória: O(L+Nd+d²) escalares;
- consulta compilada para todos os estados: O(d³ log H+Nd) operações numéricas;
- iteração esparsa min/max de horizonte H: O(HL).

Custo de bits racionais, construção de uma entrada sucinta e precisão da avaliação numérica são custos adicionais. O resultado não é um limite inferior sobre todos os algoritmos concorrentes. Métodos de recorrência/Krylov podem explorar estruturas semelhantes.

Certificado algébrico é exato com Fractions. A avaliação longa cronometrada é uma projeção float, conferida com métodos independentes em tolerância absoluta1e−8; não é um certificado intervalar de arredondamento.

O número exponencial de variantes NÃO é a fonte alegada do speedup contra Storm: ele já analisa a família levantada sem enumerá-la.

## 4. Instâncias e controles negativos

### Família sintética construída

N par, duas alternativas esparsas por estado, rótulos permutados. Para uma permutação a_i de1..N:

    q_i=1−a_i/[(N+1)2^16], r=1−1/2^17.

Cada alternativa manda q_i/2 a dois sucessores cujos a_j somam N+1. As rotas são diferentes, mas Q1=q e Qq=rq. Rank2; valor q_i r^(H−1) para H≥1. Em H100mil, sobrevivência~0,466, não underflow.

Todos os q_i são distintos. Uma bisimulação probabilística forte que preserve a falha não pode fundir dois estados vivos: as probabilidades imediatas de falha já diferem. O ganho linear não vem simplesmente de agrupar duplicatas.

A classe é INTENCIONALMENTE construída para satisfazer a hipótese; randomizar suporte e rótulos não a transforma em dados naturais. Uma perturbação .5/.5→.51/.49 numa linha conserva a sobrevivência imediata, mas gera testemunho separador no horizonte2.

### Caso físico CDKA v18

No avaliador de48 estados, oferecer as linhas de renovação integral ou omissão comprovadamente segura cria12 decisões locais,4096 variantes estacionárias. A base comum descoberta possui rank7. O certificado cobre todos os horizontes e padrões de seleção permitidos. Esse caso é uma referência de corretude: a compilação custou~112ms e perdeu em tempo total para Storm nos horizontes executados.

Outros testes: novas propriedades quebrando o certificado antigo; cadeia de falha de rankN; limite de rank que recusa sem falsa prova; comparação com enumeração completa e Bellman exato.

## 5. Protocolo externo executado

Commit do experimento: c5c3bd93cad67af7829254ef5c4981b4e066898c.
Run42144067036, job127651172185: completed/success.
Artefato13469786050 inclui35 casos com três amostras por componente, CPU e requisitos.
SHA256 do ZIP:11797ec13332f82206bedba120361c9eb4a0a054eb9c4c14d4e6af51ceb14574.

Stormpy2.0.0, NumPy2.3.5, SciPy1.16.3, Python3.12.16. BLAS/OpenMP limitados a uma thread. O metadata não conseguiu recuperar o número da biblioteca C++ por `stormpy.info`; a distribuição/interface Python é a versão explicitamente fixada. A comparação identifica a configuração esparsa, não todos os motores do Storm.

Instâncias: N16,64,512,4096 × sementes23/71; um caso CDKA48. Horizonte sintético8,1000,10000,100000; CDKA8,100,1000. Total35 consultas. Construção/compilação e consultas medidas separadamente, no mesmo processo. Duas consultas Storm: probabilidade mínima e máxima de falha limitada por H; o retorno é convertido em sobrevivência.

Tempos abaixo são SOMAS DAS MEDIANAS dos componentes, não medianas de uma execução pareada inteira. Ambos partem da mesma entrada explícita. Importação, instalação e geração comum da entrada são excluídas; a geração é registrada separadamente no JSON bruto. Sem claim de memória por método: RSS observado é o pico agregado do processo.

### Resultados representativos, semente23

| Estados | H | CDKA compilação+consulta (ms) | Storm construção+min/max (ms) | Storm/CDKA |
|---:|---:|---:|---:|---:|
|16|100000|1,0521|27,5910|26,22×|
|64|100000|5,2724|87,2309|16,54×|
|512|10000|28,5298|68,4517|2,40×|
|512|100000|28,5282|635,2994|22,27×|
|4096|8|242,9735|43,6932|0,18×|
|4096|1000|242,8742|95,0276|0,39×|
|4096|10000|242,9070|562,2668|2,31×|
|4096|100000|243,2378|5185,6524|21,32×|
|48 CDKA|8|112,6489|2,2852|0,0203×|
|48 CDKA|1000|112,6852|3,3973|0,0301×|

Na maior instância/H100mil:~240,245ms para descobrir/verificar;~2,993ms para consultar. Storm:~41,085ms para construir e~5144,567ms para min/max. A razão~21,32× inclui esses custos. O ganho só da consulta seria muito maior, mas não é a reivindicação principal.

Diferença numérica máxima reportada entre Storm e resultado compilado:7,953082636902309e−13. Todas as verificações de tolerância passaram.

Nos casos pequenos/curtos o custo da prova não se paga. No CDKA48,H8, somos~49× mais lentos. As perdas são parte obrigatória do resultado, não removidas da tabela.

## 6. Critério para estado da arte

Já existe evidência competitiva positiva contra uma ferramenta forte realmente executada, num regime matematicamente identificável. Não existe ainda evidência suficiente de SOTA geral ou de liderança numa coleção pública.

Faltam: comparador algébrico direto (Krylov/recorrência + verificação de linhas), PAYNT/PRISM/APEX relevantes, motores simbólicos adequados, dados QVBS/PRISM independentes e medições por método de memória. Um método algébrico genérico pode reproduzir grande parte do ganho; essa é uma ablação obrigatória, não um detalhe a omitir.

Próxima decisão: pré-processador com limite de rank/tempo que aceita apenas certificados e encaminha o restante a um solver geral. Variar rank independentemente de N e H; publicar falsos candidatos e custo de recusa. Conceder aos baselines reutilização legítima entre horizontes. Não alegar speedup exponencial sobre solver de famílias pela contagem de variantes.

## 7. Contribuição e próximos instrumentos

O enunciado, aplicação a alterações físicas, testemunho de rejeição e protocolo competitivo compõem uma contribuição concreta. A matemática de espaços invariantes e equivalência probabilística possui antecedentes fortes. Correção, contribuição, prioridade e fertilidade são avaliações separadas.

Fontes primárias: Tzeng1992, DOI10.1137/0221017; Storm, DOI10.1007/s10009-021-00633-z e https://www.stormchecker.org/documentation/background/engines.html; APEX https://apex.mpi-sws.org/apex/publications.html; QVBS https://qcomp.org/benchmarks/about.html; Heck et al.,AAAI2026, https://arxiv.org/abs/2511.08078 . Fontes descrevem instrumentos/comparadores; não são evidência dos tempos novos, que vêm do run e seu artefato.
