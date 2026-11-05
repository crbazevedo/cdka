# Eliminar famílias de programas com um certificado

O domínio de quatro coordenadas do diagnóstico alcançável agora permite
eliminar famílias de programas antes de construir todos os seus membros. A
garantia preserva um programa comum ótimo, o valor minimax, o valor maximin e a
existência de uma solução para um requisito conjunto de perda e fidelidade.
O circuito, a aquisição, os kernels D/R/M e a observação disponível ao
controlador permanecem os mesmos.

No caso medido com 16 preparações e 2.560 programas legais, o custo completo
caiu de **3,813 s para 1,400 s**, um ganho de **2,72 vezes** sobre um enumerador
que recebe as mesmas melhorias algébricas e de cache. Casos pequenos empataram
ou apresentaram uma pequena perda. A decisão de adotar a poda é condicionada
ao trabalho que ela economiza.
[Dados exatos](../data/program-family-results.json) ·
[Medição completa](../data/program-family-benchmark.json)

## O problema que permaneceu após a redução dimensional

O resultado anterior substituiu uma avaliação de 32 estados conjuntos por
quatro coordenadas assinadas na fronteira de preparação. Ainda era necessário
gerar todos os históricos e programas: `2^h` preparações e `(K+2)2^K` programas
com exatamente K atualizações D/R e até uma manutenção M adicional. A nova
etapa atua sobre a quantidade de programas que precisam ser construídos.

A comparação mantém um único programa completo para toda a classe. O
controlador não recebe o histórico de preparação, o estado oculto de saúde ou
uma combinação gratuita de decisões de vários programas. Cada representante
usado na poda é um programa físico original que cabe na mesma reserva comum.

## A estrutura que torna a eliminação segura

Se E contém as quatro bases de contraste e `d=-x E`, a aquisição declarada
produz `x>=0`. Os transportes de D/R satisfazem exatamente

```
E K_a = A_a E,       A_a >= 0,       a em {D,R}.
```

Logo o cone permanece válido após qualquer histórico finito de preparação.
Para uma resposta `b(w)=-E K_w g`, a fidelidade é `1/2+x b(w)`. Se um programa
tem resposta maior ou igual em cada coordenada, ele é pelo menos tão bom em
toda a classe. A não negatividade de A permite transportar essa dominância por
qualquer prefixo D/R.

A implementação usa o sinal oposto, `q(w)=E K_w g`, para reaproveitar o
avaliador anterior. Nessa convenção a desigualdade de dominância é `q(p)<=q(w)`.
As duas formas dão os mesmos valores físicos.

Há uma família concreta já na primeira camada: **DM domina MD**. Assim, para
qualquer prefixo ordinário u, `uDM` domina `uMD`. Em K=8, os 128 programas
`uMD`, com sete atualizações em u, podem ser cobertos sem construir esses
programas. A contagem geral usa conjuntos de palavras distintas e incorpora
os sufixos sem M; ela evita somar famílias que se sobrepõem.

## Manutenção continua exigindo suas distinções próprias

M geralmente retira o estado do domínio fechado de quatro coordenadas. Por
isso, toda semente `Mv` usa a resposta **completa de 16 coordenadas** do sufixo
v. O produto é acelerado pela identidade verificada `B=E K_M`, em que B tem
dimensão **4×16**. Aplicar B à resposta completa calcula a contração física
exata; nenhuma transição de manutenção 4×4 é introduzida.

Em cada nível n, os candidatos são os filhos D/R dos representantes do nível
anterior e todas as sementes Mv com n atualizações ordinárias em v. O
certificado fornece um representante retido para cada candidato. O checker
confere as identidades e as desigualdades, e a indução cobre os programas
omitidos nos níveis anteriores. Ele dispensa uma nova busca pela fronteira.
[Prova](../results/program-family-proof.md) ·
[Implementação](../../cdka/program_families.py) ·
[Revisão independente](../results/program-family-review.md)

| K | Programas legais | Programas completos construídos | Nunca construídos | Representantes avaliados |
|---:|---:|---:|---:|---:|
| 4 | 96 | 44 | 52 | 10 |
| 6 | 512 | 146 | 366 | 11 |
| 8 | 2.560 | 542 | 2.018 | 17 |

Em K=8, os 542 nomes construídos incluem 256 sufixos sem manutenção e 286
candidatos finais. Ao longo de todas as camadas, são 650 candidatos de quatro
coordenadas contra 4.608 na ablação sem poda. Ambos os métodos ainda constroem
511 nós de sufixos sem M, incluindo os níveis intermediários.

## O que a decisão preserva

Para cada histórico h, o máximo informado `B_h=max_p V[h,p]` é o mesmo na
biblioteca completa e na fronteira. Se f domina p, então

```
max_h(B_h-V[h,f]) <= max_h(B_h-V[h,p]),
min_h V[h,f]      >= min_h V[h,p].
```

A mesma substituição melhora as duas garantias. Isso preserva o valor minimax,
o valor maximin e a existência de um programa que cumpra simultaneamente um
limite de regret e um piso de fidelidade. O certificado compacto prova os
máximos informados e os dois ótimos. A viabilidade conjunta é conferida por
uma varredura adicional da matriz reduzida; ela não se deduz apenas dos dois
programas ótimos.

No caso principal anterior, DRDDM continua minimax, com perda máxima de
0,2532196 ponto percentual e fidelidade mínima de 84,9183449%. DDDDM continua
maximin. O requisito de perda até 0,3 ponto percentual e fidelidade de pelo
menos 85% continua impossível nessa biblioteca.

## O custo foi medido contra uma alternativa melhorada

Os dois métodos usam compartilhamento de sufixos, transporte D/R em quatro
coordenadas, a ponte M de dimensão 4×16 e o mesmo certificado compacto de
decisão. A ablação apenas mantém todos os candidatos. Ela recebe gratuitamente
a cobertura da sua enumeração; somente o método podado paga pelo certificado
adicional de famílias e por seu checker físico.

O total soma medianas de três execuções por componente: construção fria dos
kernels, preparações, codificação, compilação, consultas, serialização e
verificação dos certificados. Os caches dos canais físicos são limpos antes
de cada amostra de inicialização. A leitura dos certificados está incluída na
verificação. A exportação opcional do cache de consultas é medida separadamente
e excluída dos dois totais, pois a saída solicitada é a decisão.

O certificado de famílias pode ser reutilizado com outras preparações no mesmo
cone quando kernels, observação terminal e K permanecem fixos. Cada nova classe
ainda paga sua codificação, avaliação e certificado de decisão. A comparação
publicada cobra a construção e a verificação da família em uma única utilização.

| Preparações | K | Enumerador melhorado | Fronteira certificada | Razão dos custos |
|---:|---:|---:|---:|---:|
| 4 | 4 | 0,229 s | 0,227 s | 1,01×; empate operacional |
| 16 | 4 | 0,329 s | 0,271 s | 1,21× |
| 4 | 6 | 0,431 s | 0,434 s | 0,99×; pequena perda |
| 16 | 6 | 0,817 s | 0,482 s | 1,69× |
| 4 | 8 | 1,865 s | 1,350 s | 1,38× |
| 16 | 8 | 3,813 s | 1,400 s | 2,72× |

No último caso, a compilação da fronteira custa 0,596 s e sua verificação
0,590 s. Esse preço está incluído no ganho. As consultas caem de 1,819 s para
0,00982 s. O cache final serializado passa de 2.477.392 para 11.078 bytes;
esse número descreve o artefato de respostas, sem medir a memória residente
necessária para gerar os sufixos. As frações exatas e as amostras individuais
estão no [benchmark](../data/program-family-benchmark.json).

## Os caminhos rejeitados permanecem como evidência

Três limites de Bellman também podaram famílias: um limite físico em 32
estados, um limite de contraste em 16 e uma versão que usa quatro coordenadas
antes de M. Todos preservaram os ótimos exatos, mas perderam no custo total
dos controles executados. Em K=6, as duas versões mais fortes evitaram 439
dos 512 programas e ainda gastaram mais que o enumerador com sufixos
compartilhados. A economia de folhas não pagou a propagação de prefixos e a
verificação dos limites.
[Controles rejeitados e reprodução](../results/program-family-bounds-rejected.md)

Outra simplificação falhou por correção. Após a preparação DDDD, no mesmo
modelo físico, o programa MR supera RM em `0,00029617207399432015...` de
fidelidade. O fato de vários ótimos terminarem em M não permite mover toda
manutenção para o final. Esse contraexemplo é agora um teste de regressão.

## Validação e continuidade

A reprodução exata confere 3.192 relações de cobertura, 53 respostas retidas
contra a propagação física completa e as 384 respostas do caso principal
anterior. Onze testes exercitam a fronteira, os checkers, a rejeição de dados
adulterados, o domínio da preparação, reparo nulo, sensor sem informação e a
ponte de manutenção.

Persistem a enumeração de `2^K` sufixos sem M, a geração de `2^h` preparações
e a possibilidade de uma fronteira grande. A garantia preserva um ótimo;
empates completos, envelopes de previsão e objetivos adicionais de custo
executado exigem outras obrigações. A próxima etapa registrada procura uma
ordem ou um limite para os sufixos que continue válido após `E K_M`, com preço
de construção e verificação explícito.
[Memória de pesquisa](../strategy/research-memory.md) ·
[Decisão e próximo gate](../strategy/program-family-integration.md)

```bash
python -m experiments.program_family_sweep --write --check
python -m experiments.program_family_sweep --benchmark
python -m unittest discover -s tests -p 'test_program_families.py' -v
python -m experiments.program_family_bound_controls --h 2 --k 6
```
