# T4.N — Uma distinção útil precisa de um circuito

**Contribuição:** síntese exata de uma atualização de memória que combina diagnóstico e nova observação, com limite explícito de portas lógicas e ruído na escrita.

> Saber que um bit basta para decidir não significa saber como produzir esse bit fisicamente.

## Motivação

O fechamento semântico da v12 dizia quais respostas futuras precisavam ser preservadas. Aqui construímos um mecanismo que utiliza a memória anterior e um sinal novo para escrever a próxima distinção, em vez de oferecer essa atualização gratuitamente ao controlador.

## Definições mínimas

A memória anterior possui dois bits. O sistema realiza uma manutenção e lê a discordância física das células. Uma rede de portas NAND combina esses três sinais e escreve um único bit: 0 solicita manter o registro; 1 solicita atualizar. Nenhuma saúde oculta nem diagnóstico original chega ao circuito.

O orçamento conta portas instaladas; não é energia. As portas são ideais no contrato principal, mas o registro anterior e a nova escrita sofrem erros explícitos. Um teste separado demonstra por que não podemos reutilizar a equivalência de circuitos ideais sob falhas internas de portas.

## Formulação

```text
Valor = baseline_hold + q·D + (1−2q)·soma das vantagens dos sinais
                                                  que o circuito transforma em 1.
```

O valor irrestrito escolhe cada linha da tabela separadamente. Um circuito físico precisa implementar a tabela inteira dentro do orçamento.

## Exemplo e resultado

Com erro de 1% por bit da memória antiga e escrita final perfeita, a melhor sobrevivência no mesmo recorte de duas etapas é:

| Portas disponíveis | Sobrevivência |
|---:|---:|
| 0 ou 1 | 80,9178% |
| 2 ou 3 | 80,9255% |
| 4 | 80,9451% |

Duas portas podem combinar um bit diagnóstico e a nova observação. Quatro portas utilizam os dois bits para proteger a distinção mais prejudicial de confundir. Com erro acima de 1,3778%, a biblioteca de duas ou três portas deixa de oferecer vantagem; a de quatro portas permanece útil até 10,5703%, no caso de escrita final perfeita.

## Por que importa no programa

A dimensão de uma descrição do pesquisador, a quantidade de células de memória e a complexidade do circuito de atualização são recursos distintos. A contribuição fecha um caso pequeno e rastreável de R11/R14: uma regra semanticamente suficiente recebe uma realização física e um certificado de custo mínimo.

## Como a busca foi reduzida

Duas construções parciais de portas que oferecem as mesmas funções e têm o mesmo custo admitem as mesmas extensões ideais. Por isso, o sintetizador conserva conjuntos de funções disponíveis, não todos os desenhos equivalentes. Ele mantém um circuito-testemunho para cada função alcançada.

## Limites e próxima prova

O ganho absoluto é pequeno neste sistema congelado. A síntese não cobre todas as ações iniciais, portas internamente falíveis nem manutenção recorrente do circuito. A próxima generalização precisa preservar a dependência estatística de sinais quando houver falhas de portas, em vez de tratá-los apenas por suas tabelas perfeitas.

## Simulador e visualização

[Abrir o circuito e a fronteira interativa](../lab/physical_update.html). Compare o número de portas, o ruído antigo e a falha de escrita. O diagrama mostra a regra de atualização real; a tabela de oito entradas permite inspecionar cada decisão.

[Prova completa e certificados](../results/T4N-noisy-physical-updates.md) · [Prompt metodológico geral](../methodology/prompt-fechamento-contextual.md).
