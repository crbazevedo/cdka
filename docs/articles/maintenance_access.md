# Quando poder reparar muda o que precisamos distinguir

## Pergunta e estado científico

Uma representação que prevê corretamente todas as operações disponíveis continua suficiente quando o sistema ganha a capacidade de reparar o próprio mecanismo de decisão?

**Resultado demonstrado em um modelo finito.** Construímos uma condição necessária e suficiente, um algoritmo com certificado verificável e duas preparações que se tornam distinguíveis após uma manutenção paga. A contribuição conecta representação, capacidade de intervenção e realização física, reutilizando o registrador e o circuito da [v15](T4P.md).

## O problema concreto

Guardar todas as diferenças pode tornar uma investigação desnecessariamente cara. Guardar poucas exige saber quais consequências continuam preservadas. Uma capacidade nova pode mudar essa resposta: diferenças antes dispensáveis passam a determinar o efeito de uma intervenção.

O sistema tem três células binárias, uma saúde interna oculta — saudável ou degradada — e zero ou um crédito de manutenção. Um circuito de seis portas NAND calcula uma votação imperfeita das células. Sua própria saúde determina suas falhas.

Há três operações:

- **D:** evolução das células pelo canal de ruído existente.
- **R:** votação, seguida de gravação do resultado nas três células, também sujeita a erros.
- **M:** pagamento antecipado de um procedimento; o voto real solicita reparo quando vale um. O sucesso do reparo permanece oculto, as células são preservadas e a saúde evolui pelo processo já definido.

O crédito é consumido em todas as alternativas de M. Assim, o saldo posterior não revela o voto. As seis portas são reutilizadas no tempo; portas instaladas, avaliações, gravações, intervalos e créditos são custos distintos. Roteamento, relógio e reserva de crédito permanecem primitivas declaradas.

A tarefa é prever a probabilidade de uma **leitura terminal igual a um**. As operações intermediárias não devolvem observações a uma política externa. Não estamos medindo sobrevivência da planta completa. Sem crédito, M é indisponível.

## O critério que decide se podemos manter o resumo antigo

Chamamos de **resposta** a probabilidade do evento terminal para uma continuação. Uma **assinatura** reúne respostas suficientes para calcular todas as demais da biblioteca permitida.

Seja \(W_0\) o espaço gerado pelas respostas de todas as sequências finitas de D e R, incluindo massa. A assinatura antiga permanece suficiente com até uma manutenção exatamente quando

\[
MW_0\subseteq W_0.
\]

Isso significa que aplicar a manutenção antes de qualquer continuação antiga ainda produz uma resposta calculável com o resumo antigo. Se a condição falha, o algoritmo fornece uma continuação física que expõe a diferença perdida. Ele acrescenta apenas as coordenadas necessárias e verifica a inclusão das novas respostas.

O certificado contém palavras executáveis, identidades racionais e provas de independência. Um verificador separado confere esses objetos sem repetir a descoberta da representação.

## Duas preparações antes indistinguíveis

Considere saúde inicialmente degradada e as seguintes distribuições das células. Cada peso deve ser dividido por **1.458.626**; cada coluna soma esse denominador.

| Células | Preparação A | Preparação B |
|---|---:|---:|
| 000 | 0 | 30.625 |
| 001 | 0 | 736.513 |
| 011 | 0 | 691.488 |
| 100 | 736.513 | 0 |
| 101 | 722.113 | 0 |

As duas preparações produzem exatamente a mesma resposta para **toda sequência antiga de D/R**. Essa igualdade é certificada pelo fechamento da representação, além das verificações de sequências curtas.

Com sucesso de reparo de 80%, M seguido da leitura terminal produz:

| Continuação | Probabilidade em A | Probabilidade em B | Separação |
|---|---:|---:|---:|
| M → leitura | 53,417188% | 52,202982% | 1,214206 ponto percentual |
| D → M → R → leitura | 57,652564% | 56,632823% | 1,019740 ponto percentual |

É uma diferença entre preparações diante da mesma tarefa. O mecanismo é causal: o voto falível decide quais situações recebem uma tentativa de reparo; o reparo altera a confiabilidade das decisões seguintes. Essa dependência não estava preservada na assinatura antiga.

As distribuições são entradas admitidas na fronteira de comparação. O experimento não demonstra que sejam dois históricos alcançáveis a partir de um único sensor inicial.

## Quanto precisa ser acrescentado

| Biblioteca de continuações | Coordenadas sem M | Coordenadas com até uma M |
|---|---:|---:|
| Até duas atualizações D/R | 7 | 12 |
| Qualquer sequência finita D/R | 10 | 12 |

Portanto, a interface antiga já fechada precisa de **duas coordenadas lineares adicionais**. Na rodada curta, a comparação correta é 7→12. M ocupa um intervalo adicional às duas atualizações.

Com o crédito explícito, temos **32 microestados → 24 classes Markovianas → 22 coordenadas lineares de resposta**. A última redução usa dez coordenadas quando não resta manutenção e doze quando ela ainda está disponível. Depois de consumir o crédito, o certificado calcula a nova assinatura de dez coordenadas a partir da assinatura anterior de doze. A redução acompanha as capacidades restantes; não apaga gratuitamente uma observação que ainda será necessária.

Esses números incluem massa para medidas não normalizadas. Não são bits, células ou novos sinais acessíveis ao controlador. O registrador continua tendo três células; saldo e controle de fase também permanecem explícitos. A redução organiza o cálculo do avaliador.

## Exatidão e relevância operacional

Qualquer sucesso de reparo estritamente positivo exige as doze coordenadas no contrato exato. Com sucesso zero, bastam dez. Entretanto, a separação numérica cresce continuamente com a probabilidade de sucesso.

Nas **24 sequências declaradas**, com até duas atualizações e uma manutenção, o maior afastamento desse par ocorre em M → leitura. Um preditor que preserve a mesma assinatura para ambas as preparações terá erro máximo de pelo menos metade desse afastamento. A média das duas previsões atinge esse limite para o par.

Para tolerância de **0,005**, equivalente a **0,5 ponto percentual**, a distinção torna-se necessária quando o sucesso de reparo ultrapassa **65,886671%**. Esse limiar vale para esse par e essa família de consultas. Não é um ótimo global sobre todas as distribuições ou políticas.

## O controle que delimita a descoberta

Se a biblioteca antiga já devolvesse leituras intermediárias e permitisse condicionar consultas a elas, teria doze coordenadas neste exemplo. Uma sequência de duas leituras separaria o par mesmo sem manutenção.

O avanço estabelece, portanto, como **um novo uso causal do voto**, dentro de uma biblioteca explícita, altera as distinções necessárias. Isso fornece a ligação com F7: a representação depende das continuações que realmente podem ser executadas e deve ser recertificada quando essas possibilidades mudam.

Equivalência por respostas de continuações tem antecedentes em [Tzeng, 1992](https://epubs.siam.org/doi/10.1137/0221017); agregações que preservam propriedades de cadeias de Markov, em [Buchholz, 1994](https://doi.org/10.2307/3215235). A aplicação construída aqui acrescenta a realização do gatilho de manutenção, seu custo, a extensão mínima da assinatura e o separador verificável.

## Laboratório e próxima obrigação

O [laboratório](../lab/maintenance_access.html) permite variar o sucesso do reparo e comparar continuações. Observe a mudança exata de dimensão e a separação contínua das probabilidades. O gráfico não transforma a assinatura calculada em memória física.

A próxima obrigação é estender o certificado de tolerância a uma classe de preparações e políticas fisicamente alcançáveis, contabilizando aquisição e atualização do diagnóstico. Uma continuação permitida que mantenha a assinatura, mas exceda a perda autorizada, refuta a compressão proposta.

Os cálculos usam frações exatas, kernels físicos e oráculos de eventos independentes. [Prova](../results/maintenance-enabled-signatures-proof.md) · [Revisão crítica](../results/maintenance-access-review.md) · [Resultados completos](../data/maintenance-access-results.json).

```sh
python -m unittest discover -s tests -p 'test_maintenance*.py' -v
python -m experiments.maintenance_access_sweep --write --check
```
