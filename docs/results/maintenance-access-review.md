# Revisão independente — manutenção e distinções de continuação

**4 de novembro de 2026.** Revisão de [`maintenance_access.py`](../../cdka/maintenance_access.py), extensão do CDKA v15 na base `2eb1da7b635da2165e3b767440371a69583df3d0`. Foram executados cálculos racionais independentes dos testes da entrega.

## Parecer

O resultado é válido para a biblioteca declarada: duas leis indistinguíveis por todas as palavras de difusão/regeneração e um readout terminal deixam de ser equivalentes quando se admite manutenção acionada pelo voter físico. A assinatura depende das continuações realizáveis.

O avanço demonstrado é de **representação e avaliação de um mecanismo finito**. O evento terminal é a emissão do bit 1 pelo voter. Ele não mede, por si só, sobrevivência da planta, manutenção indefinida ou emergência de agência.

## Verificações executadas

| Controle | Resultado exato ou consequência |
|---|---|
| Biblioteca antiga `{D,R}` | Rank 10; as duas leis fornecidas têm assinaturas idênticas |
| Readout inicial das duas leis | `468805981/911641250` em ambos os casos |
| Manutenção condicionada, sucesso `4/5` | Diferença direita menos esquerda: `-21619539012817056454767961911/1780549316406250000000000000000` |
| Gramática com saldo físico 0/1 | Rank 22; identidades de fechamento verificadas |
| Acrescentar máscaras de leitura do saldo | Rank permanece 22 |
| Manutenção com sucesso zero | Rank permanece 10; diferença do testemunho é zero |
| Sucesso `1/10`, `4/5`, `1` | Rank 12 no setor com uma manutenção; diferença proporcional ao sucesso |
| Reparo incondicional, mesma evolução de saúde | Também produz rank 12 e separa as leis |

O último controle impede atribuir a necessidade de refinamento exclusivamente ao feedback. Na rotina escolhida, o produto `f_1(f_0-f_1)` explica a interação entre seleção falível e reparo; outras formas de alterar a saúde também podem ampliar a biblioteca de distinções.

## Obrigação observacional decisiva

A biblioteca antiga oferece somente `D`, `R` e **uma leitura terminal**. O voto usado dentro de `M` aciona fisicamente o reparo, mas não é devolvido como observação intermediária ao controlador.

Ao acrescentar leitura intermediária com instrumentos `diag(f)` e `diag(1-f)`, o rank sobe de 10 para 12. Isso também ocorre com evolução `HEALTH` após a leitura. A continuação `read1 → readout` separa as leis, com diferença

```
1014707502017298432 / 69552707672119140625.
```

Portanto, a equivalência não pode ser anunciada para qualquer política que consiga consultar o voter ou os bits brutos. Uma nova porta observável, flag ou histórico exige recertificação. O saldo da rotina pré-paga é diferente: é consumido em todos os ramos e não revela o voto ou o sucesso do reparo.

## Causalidade e custos

O seletor é avaliado antes do reparo, usando a saúde anterior. O resultado oculto altera a saúde compartilhada das utilizações seguintes. As células são retidas; em seguida ocorre a transição `HEALTH`. Essa ordem evita reparar retroativamente a decisão que solicitou manutenção.

Os seis NANDs são reutilizados no tempo. Número de chamadas, portas instaladas, canais de célula, intervalos e slots de serviço são recursos distintos. A implementação deve descrever a difusão herdada como passagem pelos canais das células; denominá-la escrita exige uma interpretação física adicional. A contagem de recursos não constitui um custo energético universal nem torna falíveis os componentes de fase e reserva tratados como infraestrutura ideal declarada.

## Minimalidade e parâmetros

Os ranks 10, 12 e 22 limitam **assinaturas lineares exatas de medidas não normalizadas**, incluindo massa. Para uma distribuição normalizada num setor conhecido, a coordenada de massa já é conhecida. Esses números não são bits de memória, estados físicos mínimos nem limites para codificações não lineares arbitrárias.

O fecho de horizonte arbitrário e a gramática limitada a duas atualizações devem ter certificados distintos. A expansão deve permitir no máximo uma manutenção, e não usar silenciosamente o fecho livre com vários reparos.

O certificado paramétrico é `M_s=M_0+sΔ`, com `M_0 W_0 ⊆ W_0`. Na gramática de uma manutenção, o espaço ampliado é o mesmo para todo `0<s≤1`; em `s=0` volta ao espaço antigo. Rank exato e tamanho do efeito são avaliações distintas. O contrato precisa registrar o parâmetro usado nas varreduras.

## Alcance computacional

A construção produz uma base e identidades verificáveis em uma arena finita já disponível. Reduzir o rank não prova economia de bits, tempo de descoberta ou complexidade do problema que gerou essa arena. Esses custos devem ser medidos separadamente. O certificado explica quais diferenças podem ser adiadas e qual nova capacidade obriga a recuperá-las.
