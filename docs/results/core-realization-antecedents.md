# Auditoria de antecedentes: realização física e renovação

**5 de novembro de 2026.** Escopo: o núcleo de interfaces realizáveis e
renováveis, o processo recorrente v16 e a extensão v17. Esta auditoria lê duas
fontes primárias próximas e os mecanismos implementados; não é uma revisão
exaustiva de prioridade. Não acrescenta modelos, medições ou testes.

## 1. Conclusão para o manuscrito

A contribuição defensável é uma **adaptação construtiva, com certificados,
para um circuito estocástico e uma gramática declarados**. Sintetizar um
controlador finito sob observação parcial, coordenar manutenção e aquisição
de informação, e atualizar probabilidades após observações têm antecedentes
diretos [J, O]. Esses instrumentos não diminuem a contribuição da adaptação,
mas delimitam o objeto cuja prioridade deve ser avaliada.

O CDKA fornece um caso executável em que seleção, execução, manutenção,
recursos e memória participam da mesma lei conjunta. Nesse caso, a renovação
estabelece uma família de emissão que fecha sob o ciclo; a retenção permite
que os resultados de atuação selecionem os registros e invalidem aquela
família. Há um testemunho exato dessa falha, uma redução alternativa
certificada e uma comparação completa dentro de uma biblioteca finita.

“Físico” significa aqui **um modelo explícito de estados, portas, falhas e
recursos, implementado computacionalmente**. Os resultados não incluem
fabricação de hardware, calibração experimental das taxas nem uma medida
termodinâmica dos tokens.

## 2. Fontes primárias e evidência localizável

### [J] Controladores finitos sob observação parcial

Junges, S.; Jansen, N.; Wimmer, R.; Quatmann, T.; Winterer, L.; Katoen, J.-P.;
Becker, B. (2018). *Finite-State Controllers of POMDPs using Parameter
Synthesis*. UAI 2018; registro PMLR R16, pp. 518–528.

- Registro: <https://proceedings.mlr.press/r16/junges18a.html>.
- Artigo da conferência: <https://auai.org/uai2018/proceedings/papers/195.pdf>.
  O PDF usa “via Parameter Synthesis” no título.
- Evidência: PDF pp. 3–5, §2.2, Definições 6–8 e §3, Teorema 1.

A Definição 6 exige consistência com as observações disponíveis. A Definição
7 separa a escolha de ação da atualização da memória finita; esta pode
depender da ação tomada. A Definição 8 constrói a cadeia parametrizada no
produto entre estado do processo e memória. A redução do §3 transforma a
síntese do controlador em síntese de parâmetros. A garantia é relativa ao
modelo e à especificação, não uma implementação automática de portas,
memória ou atuadores físicos.

### [O] Manutenção conjunta de sistema e sensor deteriorante

van Oosterom, C.; Maillart, L. M.; Kharoufeh, J. P. (2017). *Optimal maintenance
policies for a safety-critical system and its deteriorating sensor*. Naval
Research Logistics 64(5), 399–417. DOI: **10.1002/nav.21763**.

- Editora: <https://doi.org/10.1002/nav.21763>.
- Versão aceita dos autores: <https://pure.tue.nl/ws/files/76488809/deteriorating_sensor_accepted.pdf>.
- Evidência: manuscrito pp. 6–8, §2, incluindo a regra de Bayes e a equação
  (1); pp. 10–11, §3.3, Teorema 2. O PDF institucional acrescenta uma capa:
  essas localizações são, respectivamente, PDF pp. 7–9 e 11–12.

O modelo combina observações gratuitas imperfeitas, inspeção perfeita
onerosa e substituição do sensor. O estado informacional contém crença
atualizada por Bayes e idade conhecida do sensor. A política escolhe operação,
inspeção e substituição para minimizar custo esperado descontado; o Teorema
2 caracteriza sua estrutura. Portanto, selecionar observação adicional e
coordenar manutenção com qualidade informacional já são problemas explícitos
nesse antecedente. O modelo não constrói um atualizador de crenças com portas
falíveis e memória material limitada.

## 3. O que foi efetivamente implementado

A leitura foi feita nas versões fixadas pelo commit
`9b7dbd15d63531dc0fa873c6f80a74e3a763120a`:

- [recurrent_maintenance.py](https://github.com/crbazevedo/cdka/blob/9b7dbd15d63531dc0fa873c6f80a74e3a763120a/cdka/recurrent_maintenance.py):
  `Policy.mode`, `gate_execution`, `select_probability`, `task_success`,
  `micro_to_phase`, `raw_row`, `emission` e `run_summary`.
- [memory_renewal.py](https://github.com/crbazevedo/cdka/blob/9b7dbd15d63531dc0fa873c6f80a74e3a763120a/cdka/memory_renewal.py):
  `Program.refresh`, `row`, `quotient_row`, `oracle_row`, `ranking` e
  `symmetry_defect`.

| Componente | Acoplamento implementado | Limite da interpretação |
|---|---|---|
| Seleção e trabalho | O mesmo banco de seis NAND implementa votação/inversão para selecionar serviço e processa a tarefa. A saúde persistente condiciona as taxas de falha. | Os sorteios internos de falha são novos em cada uso. Não se reutiliza o mesmo padrão de falhas realizado. |
| Observabilidade | O roteamento usa saldo e células de diagnóstico; a atualização lê o comando de serviço executado. | Saúde verdadeira, sucesso de restauração e posterior do avaliador não são sinais gratuitos do controlador. |
| Manutenção | O comando pode restaurar o banco; a saúde resultante determina o desempenho na tarefa e a distribuição do diagnóstico novo. | A restauração e a falha do procedimento são primitivas estocásticas especificadas, sem engenharia interna de autorreparo. |
| Recursos | O débito comum ocorre antes do trabalho; serviço custa dois tokens adicionais; apenas trabalho correto repõe dois, com capacidade quatro. | Guarda de recursos, roteamento e comandos constantes `skip/service` são confiáveis por hipótese. |
| Memória | Três bits físicos são retidos ou substituídos por um diagnóstico ruidoso. Quatro tabelas instaladas escolhem a atualização a partir do comando executado. | Retenção não tem corrupção; a tabela de aquisição é ideal. A taxa de erro do diagnóstico novo é fixa: renovar o registro não substitui um sensor deteriorante. |

A presença de `z` em `select_probability(p,z,bits,mode)` não fornece saúde
ao programa. A função avalia a distribuição física da saída de um circuito
cuja taxa de falhas depende de saúde oculta. O modo instalado é escolhido por
`Policy.mode(b)`. Confundir a dependência causal do kernel com uma observação
disponível criaria uma crítica incorreta de acesso privilegiado.

Como interpretação formal, esse acoplamento cabe em um processo parcialmente
observável que inclua o estado da implementação. O CDKA não demonstra que
POMDPs sejam incapazes de representá-lo. Sua contribuição está em especificar
o acoplamento, derivar seus kernels e certificar as consequências sob a
gramática concreta. As idealizações na tabela continuam fazendo parte desse
contrato; o resultado não fecha autonomamente toda a cadeia de implementação.

## 4. Separar as garantias e os comparadores

O [relatório T4.R](T4R-renewal-and-selected-memory.md), §§1–8, fornece a
evidência interna dos números e certificados abaixo. Esta auditoria os
localizou e confrontou com o código; não os recalculou.

**Realização fresca.** No v16, `K=A E`, `M=E A` e `E K=M E` preservam a lei
completa e sua massa viva nas composições admitidas, para preparações na
família de emissão. As doze fases são coordenadas do avaliador. Não são doze
estados observáveis concedidos ao circuito.

**Retenção selecionada.** No v17, o contraste de massas de `011` e `101`
separa a lei retida de toda mistura das emissões antigas, inclusive com
pesos livres por saúde final e saldo. O controle com saúde estática elimina
degradação como explicação necessária. Um segundo testemunho por suporte,
com seletor sem erro, elimina a assimetria do votador como explicação
necessária. Isso particulariza a obrigação geral de condicionar a
informação pelos eventos que selecionaram sua disponibilidade.

**Redução válida.** A simetria dos dois últimos portos produz um quociente
de 48 estados para os 64 programas. A identidade de kernels certifica sua
composição. A falha da família anterior não prova impossibilidade de toda
interface de valores com doze dimensões; 48 não foi demonstrado mínimo.

**Comparação de programas.** Para oito ciclos e saúde inicial uniforme:

| Regra | Roteamento fixo `vote/vote` | Melhor dos 16 roteamentos para a regra |
|---|---:|---:|
| Reter | 0,8958752016508781 | 0,9115317652171799 |
| Renovar | 0,9174767896493894 | 0,9174767896493894 |
| Renovar após serviço | 0,8874864374106240 | 0,9115512983110162 |
| Renovar após ausência de serviço | 0,9164918233322648 | 0,9164918233322648 |

O contraste fixo renovar–reter é 2,1601588 pontos percentuais; com cada regra
reotimizada, a diferença é cerca de 0,5945024 ponto. O primeiro identifica
uma intervenção mantendo o roteamento; o segundo evita atribuir à retenção
toda a perda de uma política pouco adaptada. O ótimo `vote/vote|renew` é
relativo aos 64 programas estacionários, ao horizonte, às taxas e ao prior
declarados. Não é ótimo entre todos os controladores finitos nem entre todas
as políticas dependentes da história.

**Preço.** Cada ciclo usa o mesmo pacote tarifado de operação/memória. Isso
controla o preço por primitiva; não iguala o gasto total esperado de programas
que sobrevivem e acionam serviço com frequências diferentes. Também não
demonstra igualdade energética entre guardar e adquirir. Preços diferentes
exigiriam outra comparação, conservando este controle como referência.

**Continuidade.** A possibilidade de repetir ciclos e repor saldo não implica
sobrevivência ilimitada: a cota `q_H^n`, com `q_H<1`, continua válida. A última
atualização não melhora a sobrevivência do horizonte encerrado, pois nenhuma
tarefa posterior a utiliza.

## 5. Enunciado central revisável

> Em um modelo finito de circuito cujo mesmo banco falível seleciona
> manutenção e executa trabalho, demonstramos que uma aquisição fresca
> estabelece uma família de leis preservada pelo ciclo, enquanto permitir a
> retenção dos registros pode invalidar essa família pela seleção induzida
> por ações e resultados. Fornecemos testemunhos exatos da falha, um quociente
> suficiente para a gramática ampliada e a síntese completa de 64 programas
> estacionários sob o mesmo contrato de recursos e aquisição. A comparação
> distingue o efeito da atualização com roteamento fixo do desempenho após
> reotimização. As garantias são internas ao modelo declarado e preservam a
> separação entre informação do avaliador e sinais acessíveis ao controlador.

Esse enunciado reivindica uma construção e uma integração verificáveis. Uma
alegação de primeira ocorrência histórica ainda exigiria pesquisa dirigida
ao enunciado inteiro. Tampouco esta auditoria sustenta prioridade para a
proposição convexa de decisão comum, para interfaces preditivas em geral ou
para informação semântica; esses antecedentes pertencem às auditorias
separadas do núcleo.
