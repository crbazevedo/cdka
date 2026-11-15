# O valor do diagnóstico depois de permitir sua ausência

**15 de novembro de 2026 · OS · R11/R14.** Extensão aditiva do orçamento
comum SB, com a mesma planta, preços, circuitos e horizontes. O novo direito
físico é dispensar a aquisição inicial quando o programa completo nunca lê
o registro diagnóstico. Dois controles analíticos separam conteúdo do
relatório, custo de aquisição e fase do saldo.

[Dados exatos](../data/optional-startup-results.json) ·
[Oráculo independente](../data/optional-startup-independent.json) ·
[Formulação e prova](../results/optional-startup-formal.md) ·
[Revisão independente](../results/optional-startup-review.md) ·
[Laboratório](../lab/shared_budget.html) ·
[Registro](../../registry/optional-startup-addendum.json).

## Motivação

A síntese anterior encontrou uma regra de manutenção cega que igualava o
ótimo em 20 dos 24 pontos da grade, incluindo todos os 16 pontos com
execução NAND paga. Entretanto, essa regra ainda pagava a preparação
diagnóstica comum. Seu registro nunca era lido. Essa assimetria precisava
ser removida antes de atribuir valor operacional à informação adquirida.

A ampliação é deliberadamente pequena: mantém todos os 336 programas com
preparação paga e acrescenta 84 programas cegos que podem começar sem
adquirir o diagnóstico. A opção paga permanece disponível. Isso importa
porque um saldo inicial maior pode mudar a decisão de uma tabela fixa e
piorar sua trajetória; o ótimo do conjunto ampliado não piora por inclusão, não por
uma suposta monotonicidade de cada programa.

O resultado restringe mais a tese. A referência cega sem aquisição inicial
atinge o ótimo em **22 dos 24 pontos**, nos dois endpoints. Os únicos dois
pontos com vantagem diagnóstica têm execução NAND e escrita gratuitas,
com os dois preços de instalação já presentes na grade. O circuito ótimo
nesses pontos não tem NAND adicional de enable, portanto a instalação
também não produz débito.

A ablação causal, reotimizada sobre a mesma família, conserva exatamente
essa vantagem limitada. Ela não sustenta ganho de sobrevivência máxima por
informação paga nos 22 pontos restantes.

## Definições mínimas

**Cego** significa que as duas entradas instaladas da tabela de manutenção
escolhem somente pular ou solicitar serviço. A tarefa continua usando seus
sensores físicos e seu circuito majoritário. Nenhum resultado deste estudo
afirma que o agente age sem qualquer informação.

**Preparação paga** é a sequência anterior: capital bruto 96, comissionamento
24, instalação de roteamento de custo \(ki\), aquisição inicial de custo
\(w\). Seu saldo operacional é \(72-ki-w\).

**Preparação omitida** paga os mesmos comissionamento e roteamento, começa
com saldo \(72-ki\), não executa aquisição inicial e só é admitida para as
quatro tabelas cegas. Não fornece células correlacionadas gratuitamente.
Coordenadas arbitrárias de registro usadas pelo avaliador são etiquetas
sem acesso físico. A prova de projeção mostra que elas não alteram saúde,
saldo, falhas ou custos de nenhuma continuação cega.

O enable continua podendo solicitar aquisições reais depois de tarefas
bem-sucedidas. Elas são cobradas e falham se não houver saldo. Como nenhum
programa dessa subfamília lê o diagnóstico, a lei dos bits adquiridos pode
ser somada antes da propagação sobre saúde e saldo.

**Intervenção inicial** mantém o preço e o saldo da preparação paga, mas
substitui a lei conjunta da saúde e do relatório por um produto de
marginais. As aquisições posteriores permanecem informativas.

**Intervenção em todas as aquisições** usa, em cada aquisição paga, a mesma
lei marginal do relatório calculada com o prior inicial. O relatório
recém-adquirido independe da saúde que o produziu. O restante do mecanismo
físico permanece igual. Esse é um contrafactual analítico; não é um sensor
alternativo instalado nem uma fonte gratuita de aleatoriedade.

## Formulação

### A família física e o contrato preservado

Sejam \(\mathcal P\) os 336 representantes anteriores e \(\mathcal B\) seus
84 representantes sintaticamente cegos. A família física ampliada é

\[
\mathcal F =
\{(\mathrm{paga},p):p\in\mathcal P\}
\cup
\{(\mathrm{omitida},p):p\in\mathcal B\}.
\]

São 420 representantes de 1.280 programas físicos brutos: 16 tabelas pagas
e quatro tabelas omitidas, cada uma combinada com os mesmos 64 netlists.
Os 21 representantes de custo/perfil continuam cobrindo esses netlists
sem identificar circuitos apenas por sua tabela-verdade ideal.

A grade continua sendo \(g\in\{0,1,2\}\), \(w\in\{0,6,12,24\}\) e
\(i\in\{0,6\}\). O prior de saúde degradada é \(1/2\). Serviço custa 48;
cada tarefa custa \(24+6g\); a colheita de 48 chega somente depois de um
ciclo completo. Capacidade e capital bruto são 96.

A seleção usa a saúde de entrada. Tarefa e enable compartilham a saúde
pós-serviço, com novos flags de falha condicionais a essa saúde. O guarda
de recursos, os sinais permitidos, a retenção ideal, o desgaste e a
restauração permanecem os de SB. Todos os débitos antecedem a operação
correspondente e permanecem registrados se uma etapa posterior falhar.

O endpoint primário é oito tarefas: sete ciclos completos e uma tarefa
terminal sem enable, aquisição, desgaste ou colheita finais. O secundário
é oito ciclos completos. A mesma definição se aplica a todos os candidatos
e controles.

### Conteúdo preservado, conteúdo removido

Escreva \(P(d\mid z)\) para a lei do relatório inteiro e \(\pi(z)\) para o
prior. A intervenção usa

\[
m(d)=\sum_z\pi(z)P(d\mid z),\qquad
\mu^\perp(z,d,b)=\pi(z)m(d)\mathbf1_{\{b=72-ki-w\}}.
\]

Isso preserva a lei conjunta das três células. Substituir o relatório por
três moedas independentes seria outro controle: com o prior \(1/2\), a
probabilidade de 000 é \(247/800\), não \(1/8\). As células compartilham a
saúde latente que originou a mistura.

Para um programa fixo e uma continuação \(v\), o efeito do conteúdo inicial
é exatamente \((\mu-\mu^\perp)v\). Não há diferença de preço ou de saldo
inicial nesse contraste. A formulação completa inclui o custo acumulado e
o limite terminal, sem inferir eficiência a partir de menor gasto quando
mais trajetórias morrem cedo.

Na intervenção em todas as aquisições, a lei \(m\) é congelada no prior
inicial. Ela não é recalculada a partir de uma população sobrevivente ou
de saúde oculta corrente. Portanto, marginais posteriores sob seleção
endógena não precisam coincidir com as do mundo original. A intervenção
retira o canal causal de aquisição especificado, sem prometer uma remoção
universal de informação sobre saúde: falhas dos NANDs ainda dependem dela.

### Três contrastes que respondem a perguntas distintas

| Contraste | Definição operacional | Interpretação |
|---|---|---|
| Vantagem sobre a referência cega | Melhor candidato físico menos melhor candidato cego, ambos com preparação opcional admissível | Ganho dentro da família completa declarada; inclui diferenças do mecanismo de decisão |
| Efeito sobre um programa fixo | Programa informativo menos o mesmo programa sob o canal intervindo | Dependência causal daquele programa em relação ao conteúdo removido |
| Efeito após reotimização | Melhor candidato físico menos melhor candidato no mundo com canal intervindo, mantendo a opção cega omitida | Vantagem que resiste à adaptação da referência à ausência daquele canal |

O primeiro contraste é não negativo por inclusão de famílias. Não há uma
regra geral de sinal para o terceiro em toda gramática restrita: a família
não oferece automaticamente qualquer política aleatória ou simulação de
canal. Cada sinal informado aqui foi calculado exatamente.

## Resultados

### A referência corrigida

A tabela usa o endpoint de oito tarefas. Os números decimais são apenas
projeções de frações exatas; os critérios de decisão usam as frações.

| Preço por NAND \(g\) | Escrita \(w\) | Melhor programa físico | Referência cega sem aquisição inicial | Vantagem física |
|---:|---:|---:|---:|---:|
| 0 | 0 | 91,747679% | 91,153177% | 0,594502 ponto percentual |
| 0 | 6, 12 ou 24 | 91,153177% | 91,153177% | 0 |
| 1 | 0, 6, 12 ou 24 | 88,437506% | 88,437506% | 0 |
| 2 | 0, 6, 12 ou 24 | 87,147997% | 87,147997% | 0 |

Cada linha vale para ambos os preços de instalação \(i=0,6\). A referência
é sempre serviço/serviço com RETAIN, sem NAND de enable, sem aquisição
inicial e sem aquisições posteriores. Consequentemente \(w\) e \(i\) não
entram em sua trajetória; \(g\) ainda paga os seis NANDs de cada tarefa.

Nos dois pontos gratuitos, voto/voto com aquisição sempre renovada atinge
o máximo. Nos outros 22 pontos a referência cega omitida atinge tanto a
sobrevivência máxima quanto o gasto escolhido entre os maximizadores.
Em empates de preço zero, o desempate lexical pode nomear outro programa
com a mesma resposta; não se infere uso diagnóstico de seu nome.

Nenhum dos 24 pontos tem ganho de sobrevivência por acrescentar NAND ao
enable sobre a melhor referência sem esse NAND na família ampliada.
Os dois ganhos anteriores em \(g=0,w=6\) continuam corretos para o contrato
antigo de preparação obrigatória, mas perdem para a referência agora
admissível. As fontes e os dados históricos foram conservados.

### Conteúdo causal e reotimização

Em \(g=0,w=0\), nos dois valores de instalação, o programa informativo
ótimo tem os seguintes resultados:

| Experimento | Mesmo voto/voto + FRESH | Melhor candidato no respectivo mundo |
|---|---:|---:|
| Canal original | 91,747679% | 91,747679% |
| Só o diagnóstico inicial independente | 90,715467% | 91,153177% |
| Todas as aquisições independentes | 88,537917% | 91,153177% |

O efeito de remover o conteúdo inicial do programa fixo é 1,032212 pontos
percentuais. O efeito de remover o conteúdo de todas as aquisições desse
mesmo programa é 3,209762 pontos. Depois de reotimizar a referência, ambos
os contrastes deixam uma vantagem de **0,594502 ponto percentual**.

Confundir esses números superestimaria o valor decisório do canal. O
programa que depende de um sinal pode piorar muito quando ele é removido,
enquanto outro programa resolve grande parte da tarefa sem esse sinal.

Nos 22 pontos com execução ou escrita pagas, os ótimos físicos, cegos e
contrafactuais reotimizados coincidem exatamente. Isso não significa que
todo programa ignore diagnósticos: programas particulares ainda podem
melhorar causalmente com o canal e mesmo assim perder para a referência
cega com os mesmos recursos.

## Exemplo: mais saldo pode derrubar uma regra fixa

Considere \(g=0,w=6,i=0\), serviço/serviço e enable igual ao sinal de serviço
executado, sem NAND adicional. Com diagnóstico inicial pago, a regra
começa com saldo 66, pula o primeiro serviço e atinge sobrevivência de
88,637064% em oito tarefas.

Se a mesma regra omite a preparação, começa com 72 e solicita serviço:

1. O serviço custa 48, deixando 24.
2. A tarefa custa 24, deixando zero.
3. O serviço executado faz o enable solicitar escrita de custo 6.
4. A escrita não pode ser paga. A colheita ainda não ocorreu.

A sobrevivência de oito tarefas é exatamente zero. Procedimento e tarefa
também podem falhar antes, com seus custos já incorridos. A despesa média
total é 95,88; esse valor baixo não representa eficiência.

O relatório nunca é lido em nenhuma dessas duas execuções. Pagar por ele
altera o momento do serviço ao consumir saldo; não há valor informacional
nesse efeito. A regra ótima omitida usa RETAIN e evita a escrita, atingindo
91,153177%. Por isso a opção paga é conservada e as decisões são feitas
sobre programas completos.

## O que habilita

O resultado fornece um teste executável mais exigente para atribuir valor
operacional a uma representação:

1. A ausência da aquisição deve ser uma opção fisicamente admissível
   quando a continuação não lê o registro.
2. Preços e saldo precisam ser mantidos no controle que remove somente
   o conteúdo. Omissão de aquisição e independência do relatório são
   intervenções diferentes.
3. A referência precisa ser reotimizada depois da intervenção. Um
   programa fragilizado pela ablação não constitui, sozinho, a melhor
   alternativa sem aquele canal.
4. A conclusão deve se referir às observações realmente admitidas, à
   família de programas, ao endpoint e aos recursos utilizados.

Aqui esses requisitos preservam uma vantagem causal no limite gratuito e
eliminam a evidência de ganho de sobrevivência máxima por aquisição paga
dentro da família testada. Esse
resultado negativo é parte da resposta à pergunta sobre conhecimento
operacional; não é corrigido por uma escolha posterior de preços.

## Verificação e limites

A varredura executa 52.416 avaliações exatas: 24 preços, dois endpoints e,
por ponto/endpoint, 336 preparações pagas, 84 omitidas e duas famílias de
336 intervenções analíticas. As 48 assinaturas completas dos programas
pagos coincidem com o certificado SB anterior.

Um segundo avaliador projeta diretamente sobre saúde e saldo e enumera
sensores e falhas NAND sem importar o novo compilador ou o compilador de
orçamento. Suas 4.032 respostas omitidas coincidem integralmente com a
varredura principal. Os 8.064 contrastes de programas cegos pagos contra
as duas intervenções mantêm custos, falhas, contagens, distribuição final
do saldo e curvas de sobrevivência, não somente a sobrevivência final.

Os testes incluem leis primitivas independentes, trajetórias curtas,
células não inicializadas sem acesso, falhas de preparação, horizonte
zero, identidade do canal com erro \(1/2\), limite terminal e a saúde
compartilhada que permanece na computação. A conservação exata é checada
em cada avaliação:

\[
\text{gasto}+\text{saldo restante}+\text{desperdício}
=96+\text{colheita recebida}.
\]

A família não inclui políticas que começam sem relatório e adiam sua
primeira leitura até uma aquisição posterior, controladores com memória
adicional, agendas arbitrárias ou um ótimo de POMDP sem custo de
implementação. A retenção e as interfaces confiáveis continuam idealizadas.
Os preços são quanta fungíveis ilustrativos; não há medição de energia.
O resultado não prova que todo circuito seja dominado em toda a fronteira
de baixo desempenho.

O limite seguinte é a admissibilidade física da primeira observação:
descrever uma continuação com aquisição adiada exige rastrear a validade
do registro e provar que nenhuma leitura precede uma aquisição real.
A validade pode ser um marcador apenas do verificador; qualquer teste
de validade executado pelo controlador exige observação e custo físicos
explícitos. O próximo teste conserva as 16 tabelas e os 21 canais existentes
e rejeita qualquer programa com leitura não inicializada de massa positiva.
Até essa obrigação ser certificada, a conclusão permanece no conjunto
de 420 programas aqui avaliado. Expandir circuitos ou buscar preços
favoráveis não resolve essa lacuna.

## Simulador e reprodução

O [laboratório](../lab/shared_budget.html) conserva a comparação histórica
de SB e acrescenta a família com preparação opcional. Os controles de
preço e endpoint mostram o ótimo pago, o ótimo físico ampliado, a melhor
referência cega e o contrafactual reotimizado. Os valores exibidos vêm dos
certificados exatos, sem interpolação de pontos não avaliados.

    python -S -O -m experiments.optional_startup_independent --check
    python -S -O -m experiments.optional_startup_sweep --check
    python -S -O -m unittest discover -s tests -p 'test_optional_startup.py' -v
    python -S -O -m unittest discover -s tests -p 'test_diagnostic_ablation.py' -v
    node --test tests/shared-budget-lab.test.mjs

Código físico: [preparação](../../cdka/optional_startup.py).
Controle causal: [ablação](../../cdka/diagnostic_ablation.py).
Síntese: [varredura](../../experiments/optional_startup_sweep.py).
Oráculo: [avaliação independente](../../experiments/optional_startup_independent.py).
