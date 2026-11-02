# CDKA — Catálogo de abordagens e política de retomada v6

**Fonte canônica:** [research-options.json](research-options.json). Cada registro contém hipótese, estado, gatilho de retomada, teste mínimo, instrumentos, critério de saída, alternativas e proveniência. O laboratório [composition.html](../docs/lab/composition.html) oferece busca e filtros. São 32 abordagens identificadas no corpus disponível, não um levantamento exaustivo de toda a ciência relevante.

## Disciplina de execução

No máximo dois ramos ativos. Os próximos são **R11 — saúde oculta e diagnóstico pago** e **R14 — custo conjunto de implementar prescrições**. Um instrumento conhecido não é uma descoberta original; uma hipótese estacionada não foi esquecida.

Após dois modelos limitados sem nova implicação ou separação, congelar a expansão de funcionalidades e auditar anterioridade e hipóteses. Quando um teste falhar, registrar se houve contradição matemática, erro de implementação, hipótese física ausente, limite numérico, certificado vazio ou contribuição já conhecida. Só então seguir a alternativa nomeada, mantendo o mesmo problema causal.

## Mapa preservado

| ID | Abordagem / estado | Quando retomar ou reutilizar | Alternativas |
|---|---|---|---|
| R01 | Contrato causal — validado no escopo | Uma comparação altera estado inicial ou evento junto com a ação | R05, R20 |
| R02 | Suficiência para agir — instrumento | Precisamos do código mínimo de decisão sem erro | R03, R23 |
| R03 | Informação com erro tolerado — estacionado | Risco não nulo ou prior não uniforme muda o requisito | R04, R17 |
| R04 | Expoentes de confiabilidade — instrumento | Informação média oculta diferenças catastróficas | R08, R27 |
| R05 | Ação física com prazo — instrumento | Precisamos calibrar um evento real de reparo/escrita | R06, R07 |
| R06 | Escala crítica — estacionado | Aproximações falham perto da bifurcação | R07, R27 |
| R07 | Limites variacionais multidimensionais — estacionado | A quadratura escalar não se aplica | R05, R27 |
| R08 | Ruído correlacionado — instrumento | Independência produz benefício de redundância suspeito | R29, R30 |
| R09 | Corretor falível e manutenção — validado no escopo | Uma garantia depende de corretor ideal | R11, R18 |
| R10 | Mundo variável e memória obsoleta — validado no escopo | Preservar um bit estático é chamado de conhecimento continuado | R22, R11 |
| R11 | Saúde oculta e diagnóstico pago — ativo | A saúde legível permanece um supervisor ideal | R14, R28 |
| R12 | Certificado composicional aproximado — validado no escopo | Simetria exata falha, mas erro uniforme pode ser limitado | R13, R29 |
| R13 | Quociente exato e legível — validado no escopo | Muitos microestados ou uma estatística possivelmente onisciente | R12, R23 |
| R14 | Implementabilidade conjunta — ativo | Disponibilidade por linha inventa um seletor físico | R15, R28 |
| R15 | Sinalização por ações e recursos — instrumento | Um no-go ignora traços físicos da política | R11, R14 |
| R16 | Aleatoriedade persistente versus nova — instrumento | Uma mistura de políticas melhora a garantia robusta | R17, R14 |
| R17 | Perfis de contexto e massa sobrevivente — instrumento | Métrica média melhora apesar da perda de contextos | R18, R21 |
| R18 | Suporte e vida espectral — instrumento | Vida longa é confundida com segurança indefinida | R19, R30 |
| R19 | Coordenação e alternância — estacionado | Um resultado por modo é aplicado ao controlador composto | R14, R18 |
| R20 | Reconfiguração financiada — instrumento | Uma arquitetura melhor é concedida desde o início | R09, R14 |
| R21 | Projeto finito versus política indefinida — instrumento | Termos dominantes são usados para concluir viabilidade infinita | R18, R27 |
| R22 | Percepção ativa e controle dual — estacionado | Observar também muda o mundo ou observabilidade futura | R11, R14 |
| R23 | Topologia dinâmica de compatibilidade — estacionado | Classes de memória passam a unir três ou mais contextos | R02, R13 |
| R24 | Replicador e memória evolutiva — estacionado | Mecanismos reguladores passam a reproduzir-se ou ser selecionados | R25, R26 |
| R25 | Semântica e finalidade — estacionado | A ontologia excede o contrato de viabilidade | R26, R17 |
| R26 | Autonomia versus replay externo — estacionado | Um comportamento complexo é atribuído a automanutenção | R09, R25 |
| R27 | Calibração física e termodinâmica — estacionado | Bits, esforço, ação ou joules passam a ser equiparados | R05, R08 |
| R28 | Síntese formal escalável — estacionado | A enumeração de controladores deixa de ser viável | R13, R14 |
| R29 | Incerteza não retangular — na fila | Contratos locais permitem parâmetros compartilhados variarem arbitrariamente | R12, R08 |
| R30 | Erros não fatais e redundância — instrumento | Uma lei de arquitetura fatal é declarada universal | R09, R18 |
| R31 | Objetivos unificadores como concorrentes — estacionado | Entropia, empowerment ou energia livre substituem distinções causais | R25, R26 |
| R32 | Osciladores e realização contínua — estacionado | Um certificado finito está pronto para teste em dinâmica física | R05, R24 |

## Simplificações rejeitadas

| ID | Alegação tentadora | Por que não deve reaparecer sem novas condições |
|---|---|---|
| D01 | Comparar ações a partir de seus próprios equilíbrios | Muda simultaneamente a situação contrafactual |
| D02 | Compatibilidade aos pares basta | A interseção de um grupo pode ser vazia |
| D03 | Um bit inicial basta para sempre | Pode desaparecer ou ficar obsoleto |
| D04 | Modos isolados apagam, logo feedback apaga | A escolha do modo pode transmitir um bit |
| D05 | Precisão dos sobreviventes prova viabilidade | Normalizar elimina os mortos da análise |
| D06 | Toda mistura é aleatoriedade gratuita | Coordenação persistente precisa de estado físico |
| D07 | Distribuir recursos uniformemente é sempre ótimo | Complementaridade cria um regime convexo de escassez |
| D08 | Custo finito n log n decide duração infinita | Termos inferiores e disponibilidade temporal importam |
| D09 | Erros marginais determinam falha | Dependência e evento lógico alteram o resultado |
| D10 | Modos transientes implicam coordenação transiente | Produtos coordenados podem ter ciclos seguros |
| D11 | Instalar assim que possível é ótimo | O risco de financiar a mudança pode favorecer adiar |
| D12 | Código sob falhas limitadas prova segurança térmica | Suporte adicional muda a recorrência |
| D13 | Contagem basta com células heterogêneas | Contraexemplo v6: TV=513619/2000000 |
| D14 | Erro local pequeno prova segurança infinita | O limite de horizonte finito satura |

## Uso do catálogo em um dead-end

**Resíduo de agregação não nulo:** R13 para refinar uma partição fisicamente legível; R12 se um erro uniforme justificável ainda permite certificação. **Certificado vazio:** reduzir o horizonte certificado ou apertar o contrato; R29 se a perda vem de uma relaxação retangular excessiva. **Informação não legível:** R11/FSC, não um posterior gratuito. **Política irrealizável:** R14/R28. **Anterioridade equivalente:** conservar como instrumento e mudar a hipótese específica, sem inventar prioridade. **Física não calibrada:** R27/R05 antes de interpretar esforço como energia.

As entradas possuem critérios de saída e proveniência no JSON; testes verificam IDs únicos, alternativas existentes e o limite de trabalho ativo.
