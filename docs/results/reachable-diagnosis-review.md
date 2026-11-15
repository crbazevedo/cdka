# Revisão independente — diagnóstico alcançável e plano comum

**Data:** 4 de novembro de 2026.  
**Escopo:** protocolo físico de aquisição, classe de preparações, certificado
de respostas/regret, restrição por alcançabilidade e controles negativos.

## Parecer

O resultado principal foi reproduzido: entre os 96 planos completos do
contrato, `DRDDM` é o único plano de menor regret máximo para as quatro
preparações alcançáveis. Ele não é ótimo para nenhuma preparação individual.
Todas as **384 respostas** coincidiram exatamente com o oracle que transporta
o estado conjunto `(H,Z,bits)`. Os **34 testes** dos três módulos novos
passaram nesta revisão.

Não há bloqueador científico identificado no contrato declarado. As
conclusões dependem da aquisição compartilhada, do trabalho obrigatório,
do conjunto completo de planos e da ausência de acesso ao histórico. A
restrições de oito massas de órbita e quatro coordenadas de contraste são
válidas na fronteira de entrada; tratá-las como um quociente Markov depois
da manutenção perde dependências verificáveis.

Fontes verificadas: [protocolo físico](../../cdka/reachable_diagnosis.py),
[certificador de classes](../../cdka/reachable_interfaces.py),
[restrição de entrada](../../cdka/reachable_restriction.py),
[provas](reachable-interfaces-proof.md) e
[dados canônicos](../data/reachable-diagnosis-results.json).

## 1. O protocolo preserva a causa sensorial comum

A fonte `H` é justa, constante e independente da saúde inicial. O sensor
faz **uma** observação `Y=H xor E`, com erro `eta=1/10`. O mesmo `Y` alimenta
três escritas com erros independentes `1/50`; a saúde inicialmente saudável
passa por um intervalo `HEALTH` após a aquisição. Os históricos `DD`, `DR`,
`RD` e `RR` têm dois intervalos e partem desse mesmo protocolo.

O código de aquisição foi confrontado com os eventos de fonte, saúde,
falha sensorial única, três falhas de escrita e degradação. Em particular,
a probabilidade de as três células estarem erradas é

\[
\eta(1-e)^3+(1-\eta)e^3,
\]

que difere do cubo do erro marginal de uma célula. Isso detecta a substituição
indevida de uma leitura compartilhada por três leituras independentes.

O alvo terminal é `voto=H`. A identidade

\[
V_\eta=\eta+(1-2\eta)V_0
\]

foi conferida para os 384 pares preparação/plano. Ela decorre da fonte justa
e do acesso posterior apenas ao sinal adquirido e ao estado físico. Nenhum
plano pode ultrapassar a fidelidade sensorial `1-eta=0,9` neste contrato.
O sensor é um canal físico declarado e contado separadamente; não foi
identificado com um circuito NAND sintetizado nesta rodada.

O histórico é metadado do avaliador. O controlador não recebe `H`, `Z`, o
resultado do reparo ou o identificador `DD/DR/RD/RR`. Sua escolha é um plano
completo comum, que contém a seleção física falível já implementada em M.
O fecho convexo das preparações amplia o domínio de incerteza do avaliador;
ele não instala um randomizador ou um leitor de histórico.

## 2. Reprodução da decisão principal

Cada plano executa exatamente quatro atualizações D/R e até uma manutenção
adicional. Há `2^4 + 5*2^4 = 96` planos. A leitura terminal é implícita e
contada nos custos.

| Preparação | Ótimo individual | Fidelidade ótima | Fidelidade de DRDDM | Regret de DRDDM |
|---|---|---:|---:|---:|
| DD | RDDDM | 0,854394749347 | 0,852489895917 | 0,001904853430 |
| DR | DDDDM | 0,854255094664 | 0,851722898546 | 0,002532196118 |
| RD | RDDDM | 0,852940833567 | 0,852164674749 | 0,000776158819 |
| RR | DDDDM | 0,851501183411 | 0,849183448952 | 0,002317734459 |

Os números exibidos são arredondados; as comparações foram feitas com
frações exatas. O regret mínimo máximo é

\[
R_* = 0,0025321961178476887\ldots,
\]

ou aproximadamente **0,253219612 ponto percentual**. O testemunho que atinge
esse limite é a preparação `DR`, comparada com seu plano ótimo `DDDDM`.

A decisão é um compromisso entre preparações, não a seleção de um dos
ótimos individuais. O certificado também separa o objetivo de menor regret
do objetivo de maior fidelidade mínima. A exigência conjunta de regret no
máximo `0,003` e fidelidade mínima `0,85` é inviável entre esses 96 planos,
embora cada condição isolada possa ser atendida. Ambas precisam valer para
o mesmo plano.

## 3. O certificado mantém as dependências necessárias

Para a matriz exata `V[h,p]`, o regret de um plano comum p é

\[
R_p=\max_h\left(\max_q V_{h,q}-V_{h,p}\right).
\]

Esse valor é simultaneamente o extremo sobre os geradores alcançáveis e
sobre seu fecho convexo. O comparador usa a mesma biblioteca de planos;
nenhum estado oculto é entregue à política comum. A diferença é calculada
no **mesmo histórico**, preservando a dependência que se perderia ao
subtrair extremos de envelopes marginais distintos.

Foram inspecionados os seguintes controles adversariais implementados nos
testes:

- Planos com a mesma primeira ação e sufixos incompatíveis.
- Compatibilidade entre todos os pares de preparações, sem plano ótimo
  comum à classe inteira.
- Um plano que domina ponto a ponto, embora a subtração de envelopes
  independentes produza um regret positivo fictício.
- Um minimax de regret que não é ótimo em nenhuma preparação e difere do
  maximin de fidelidade.
- Centro coordenada a coordenada que não corresponde a uma lei física.
- Adulteração de extremos, testemunhos, planos, valores e contrato.

O exemplo de centro incompatível usa as três leis pontuais `e1,e2,e3` e
consultas indicadoras. O centro livre `(1/2,1/2,1/2)` tem raio `1/2`, mas
massa `3/2`; o centro físico uniforme tem raio `2/3`. O módulo distingue
esses objetos e não propaga o centro livre como uma distribuição.

A verificação usa desigualdades e testemunhos que atingem os limites. Os
testes desabilitam os auxiliares de otimização durante a leitura de um
certificado serializado. A vinculação SHA-256 inclui tabela, identidades
ordenadas e contrato; a correção física da tabela permanece uma obrigação
separada, atendida pelos oracles e controles do experimento.

## 4. A redução por alcançabilidade tem uma fronteira precisa

Antes de M, cada submedida condicionada em H é exchangeável nas três
células. O domínio inteiro é descrito pelas oito órbitas `(Z,contagem)`.
D e R preservam esse domínio de distribuições, mesmo que o votador
individual distinga suas portas. As respostas antigas restritas têm rank
oito, incluindo massa; o certificado de uma matriz inversa foi verificado
sem repetir a descoberta da base.

Esse rank diz respeito a **todo o domínio exchangeável**, não a uma
minimalidade da coleção particular de quatro preparações. A assinatura da
fidelidade guarda oito entradas de contraste e um deslocamento de massa;
na fixture, o deslocamento é conhecido (`1/2`) e o contraste tem soma zero.

### Quatro coordenadas para o contraste da fonte

O contraste `d=mu_1-mu_0` satisfaz ainda `d(z,bits)=-d(z,complemento(bits))`.
Por saúde, suas massas orbitais têm a forma `(a,b,-b,-a)`, restando duas
coordenadas por Z e **quatro no total**. A aquisição compartilhada satisfaz
essa propriedade. D comuta com permutações e complemento; HEALTH mistura
os dois modos de saúde sem depender de H.

A preservação por R não exige que o votador seja simétrico. Como
`sum_bits d(z,bits)=0`, o termo comum de saída zero se cancela. Se `B0` e
`B1` são as distribuições das três escritas condicionadas ao voto, a nova
medida é proporcional a

\[
\left(\sum_{bits}d(z,bits)f_z(bits)\right)(B_1-B_0),
\]

que volta a ser exchangeável e antissimétrica. Isso verifica a invariância
antes da manutenção por uma razão independente da igualdade de suas portas.

As respostas antigas restritas separam as quatro coordenadas; o certificado
da matriz inversa de ordem quatro passou pelo verificador independente. As
384 respostas da fixture também foram recalculadas com a representação de
quatro coordenadas, com igualdade racional exata.

Essas coordenadas representam uma medida assinada do avaliador, com o
deslocamento de massa conhecido separadamente. Não constituem quatro estados
Markov físicos. M pode gerar massa de contraste não nula em cada modo Z,
embora a massa global continue zero, e rompe o domínio antissimétrico. As
consultas com M são propagadas na física completa antes de projetar suas
respostas sobre o domínio inicial de quatro coordenadas.

Se Q expande uma massa de órbita uniformemente e A agrega estados físicos,
vale `Q K = Q K A Q` para D e R. A manutenção quebra essa identidade:
seu pedido de reparo depende do votador assimétrico e modifica a associação
entre saúde e configuração das células.

O uso correto calcula `Q K_w g` com a continuação física completa, antes
de restringir a resposta à fronteira inicial. O substituto que propaga
`Q K A` depois de toda operação perde uma dependência real.

### Separador independente do quociente ingênuo

Para a órbita degradada com duas células iguais a um,

\[
(QMRg-QMAQRg)_{(1,2)}
=-\frac{16632935920161845258704109382094533}
        {93132257461547851562500000000000000000}
\approx-0,000178594789533897.
\]

Na fixture inteira de quatro preparações e 96 planos, o maior erro do
modelo que reaplica o quociente ingênuo ocorre em `DD` seguido de `DDDDM`:

| Avaliação | Fidelidade |
|---|---:|
| Física exata | 0,8500277369367224 |
| Quociente ingênuo | 0,8500339030002646 |
| Erro absoluto | 0,000006166063542229 |

O erro é pequeno nesse caso e estritamente diferente de zero. Sua existência
refuta a exatidão do quociente; não é arredondamento ou erro de amostragem.
Mesmo uma M final exige calcular a resposta física antes da projeção.

Separadamente, a mudança do alvo para `voto=H` foi conferida em um modelo
irrestrito de 32 estados. Os ranks globais são **11 e 13**, para a biblioteca
antiga e a biblioteca com uma M. Isso evita transportar os números 10/12
da tarefa anterior sem considerar a mudança do evento terminal.

## 5. Os controles impedem atribuir o compromisso ao cenário errado

Com atualizações opcionais, a leitura imediata `I` é o único ótimo comum
na fixture saudável. O dado canônico usa de zero a duas atualizações
(24 planos); a revisão também verificou de zero a quatro (160 planos),
com o mesmo resultado. O compromisso `DRDDM` pertence ao problema com
quatro atualizações obrigatórias. Essa obrigação foi declarada na definição
do trabalho e não pode ser omitida ao interpretar a descoberta.

Com sucesso de reparo zero, a manutenção deixa de aparecer no plano
minimax selecionado (`DRDD`). Com sensor não informativo (`eta=1/2`), todas
as fidelidades são `1/2`, os envelopes colapsam e o regret é zero. Isso
mostra por que regret baixo precisa ser combinado com um piso absoluto de
desempenho: a ausência de informação também pode eliminar diferenças entre
decisões.

## 6. Custos físicos e computacionais

A reserva comum admite qualquer histórico e qualquer plano do contrato:
um sensor, seis NANDs instaladas, três células, **48 avaliações de NAND**,
**21 escritas**, **21 atualizações de canais de células**, um crédito de
manutenção e nove intervalos. Essa reserva foi conferida para todas as
384 combinações. Os custos executados são reportados separadamente.

Por exemplo, `DD` seguido de `DRDDM` executa 18 avaliações de NAND e seis
escritas; `RR` seguido do mesmo plano executa 30 avaliações e doze escritas.
Ambos permanecem dentro da mesma reserva. Difusão não é contada como
reescrita, e a aquisição custa uma leitura sensorial e três escritas.

O certificado da tabela usa `O(|H||P|)` operações racionais, mas construir
os históricos e planos continua podendo crescer exponencialmente com o
horizonte. A medição deve separar preparação comum, conversão da entrada
por método, compilação do cache, consultas e verificação. Esta revisão
valida igualdade e escopo das respostas; números de runtime pertencem ao
artefato de benchmark e não são constantes científicas.

## 7. Reprodução desta revisão

Os 34 testes foram executados com:

```sh
python -m unittest discover -s tests -p 'test_reachable*.py' -v
```

A comparação independente de todas as 384 respostas pode ser repetida com:

```sh
python - <<'PY'
from cdka.maintenance_access import base_operators, base_probes
from cdka.reachable_diagnosis import (
    preparation_laws, plan_words, response_table, joint_oracle, word_id,
)
from cdka.reachable_restriction import (
    query_cache, contrast_signature, contrast_value,
)
cohort = preparation_laws(h=2)
words = plan_words(k=4)
table = response_table(cohort, words)
queries = query_cache(base_operators(), base_probes()['readout'], words)
checked = 0
for history, row in table.items():
    signature = contrast_signature(*cohort[history])
    for word, column in zip(words, queries['contrast']):
        assert row[word_id(word)] == joint_oracle(history, word)
        assert row[word_id(word)] == contrast_value(signature, column)
        checked += 1
assert checked == 384
print('384 exact joint-oracle and four-coordinate comparisons passed')
PY
```

Esse oracle transporta H explicitamente e não usa a identidade de contraste,
a assinatura restrita ou a otimização do certificado. Ele reutiliza os
kernels físicos brutos herdados, cuja realização por eventos já é
verificada pelos testes das rodadas anteriores. Assim, a independência
declarada concerne à nova aquisição, ao transporte de H e ao caminho de
avaliação, sem inventar uma segunda implementação de toda a física.
