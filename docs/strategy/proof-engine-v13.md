# Proof Engine v13 — Da assinatura à atualização realizável

**3 de novembro de 2026.** Dois resultados coordenados: uma metodologia reutilizável para problemas combinatórios e uma instanciação física certificada no CDKA.

## 1. A metodologia exportável

O [prompt](../methodology/prompt-fechamento-contextual.md) e o [manual](../methodology/manual-fechamento-contextual.md) generalizam o ciclo: contrato → família de continuações → redução apropriada → certificado → rastros independentes → realização concreta → refinamento.

A generalização distingue equivalência, contagem, dominância, controle adversarial, abstração aproximada, fatorização e espaços lineares. Não promete que toda instância possua um pequeno quociente nem usa álgebra de corpos onde só há um semiring.

## 2. O próximo enunciado foi escolhido antes de ampliar o sistema

R11 exigia uma atualização física entre decisões; R14, um único mecanismo que implementasse as escolhas de forma conjunta. Escolhemos o recorte SERVICE-first do processo existente porque v9/v11 já ofereciam um par de histórias cuja continuação muda com diagnóstico e síndrome.

O teste é: um circuito de K portas consegue atualizar a memória para conservar uma vantagem de continuação depois do ruído? O horizonte e o evento físico não mudaram. O recorte deliberadamente não reotimiza a primeira ação.

## 3. Etapa concluída

- A interface usa apenas dois bits recebidos e uma nova síndrome legível.
- O resultado da atualização é gravado em uma célula; somente ela chega à decisão terminal.
- O circuito inteiro pertence a uma biblioteca NAND com orçamento K.
- A busca funde construções parciais por equivalência de suas extensões ideais, preservando um netlist concreto.
- 64 encodings × 91 funções = 5.824 programas no maior orçamento.
- Fronteira exata em p e q para K=0..4, incluindo um bypass físico comum.
- O ótimo de duas/três portas usa um sinal diagnóstico; quatro portas podem explorar redundância de tarefa. Prova de mínimo e testemunho que o atinge.
- Um falsificador mostra que verdade lógica ideal não preserva confiabilidade quando o contrato passa a incluir falhas internas de portas.

## 4. Critério de conclusão do núcleo finito

A primeira fase do programa pode ser consolidada como uma contribuição coerente, em vez de continuar acrescentando versões sem síntese:

1. Formulação relacional: informação, ação, continuação e organização.
2. Contraexemplos que separam capacidades marginais e realização conjunta.
3. Compilação de continuações e testemunhos de distinção.
4. Síntese conjunta de representação, transporte, atualização e programa.
5. Certificados de perda e custo numa biblioteca física declarada.
6. Limites de transferência e um registro de falsificadores.

A v13 fecha o item 4/5 para um recorte finito, não a teoria geral de agência. O próximo trabalho deve consolidar os enunciados comuns e comparar os predecessores antes de expandir o hardware.

## 5. Dois ramos ativos, próximos testes delimitados

**R11 — atualização sob ruído estrutural:** comparar dois circuitos com a mesma função ideal e custos declarados, mas falhas internas compartilhadas ou independentes. Uma assinatura apenas de verdade lógica falha; buscar o menor refinamento que preserve o canal conjunto usado pela continuação. Teste mínimo: fio versus duas inversões, depois dois DAGs com fanout compartilhado. Não simular centenas de componentes antes de resolver o caso mínimo.

**R14 — custo comum de leitura/escrita/seleção:** otimizar código e rede de múltiplas saídas com subcircuitos compartilhados. Uma porta pode servir à memória e à seleção; não somar custos mínimos calculados em projetos separados. Resultado exigido: lacuna estrita, implementação atingível e certificado independente de limite inferior.

## 6. Política de mudança de direção

- Se o equivalente perfeito não preserva falhas: R43 rastros + R44 fechamento enriquecido pelo canal conjunto.
- Se a síntese física explode: fatorar por fronteiras de sinais e usar SAT/MILP com certificado; manter um oráculo pequeno independente.
- Se a assinatura fica inacessível: cobrar observação, transporte ou precisão; não fornecer estado oculto.
- Se a generalização coincide integralmente com síntese clássica: preservar a aplicação e o certificado, isolar a adaptação de recursos/continuidade ainda não respondida.
- Se duas execuções limitadas não produzirem nova separação, método ou redução: consolidar o núcleo finito e reavaliar a classe, em vez de acrescentar componentes.

## 7. Hipótese de maior fertilidade

A complexidade relevante tem pelo menos três camadas: dimensão das respostas que importam, geometria física de sua codificação e custo do mecanismo que atualiza/usa essas respostas. O novo experimento as separa com números exatos. Uma teoria útil deve fornecer relações entre essas camadas, não identificá-las por definição.

## Fontes e execução

[Prova T4.N](../results/T4N-noisy-physical-updates.md), `cdka/physical_update.py`, `tests/test_physical_update.py`, `experiments/physical_update_sweep.py`. As referências primárias estão nas notas e no manual. Correção, contribuição, prioridade e fertilidade permanecem eixos separados.
