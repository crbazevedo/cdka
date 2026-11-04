# Um plano comum para diagnósticos fisicamente alcançáveis

**Estado científico:** certificado exato de classe, redução construtiva e benchmark executado.  
**Ramos ativos:** R11/R14. Continuação do resultado de acesso à manutenção.

> Quando o diagnóstico foi adquirido e atualizado por um processo físico pago, quais distinções precisam permanecer no avaliador e qual plano completo pode servir a toda a classe sem ler gratuitamente o histórico?

## O avanço

A rodada anterior mostrou que uma nova capacidade de manutenção pode exigir mais coordenadas de resposta: 10→12 para a tarefa de produzir um voto terminal igual a um. O par que demonstrava essa necessidade era uma preparação admissível arbitrária.

Esta rodada constrói as preparações a partir de um único sensor e resolve o problema de decisão para a classe inteira. O resultado combina três afirmações: a aquisição restringe o domínio alcançável; esse domínio admite quatro coordenadas assinadas de avaliação; um plano comum tem perda ótima exatamente certificada, inclusive quando nenhum plano é ótimo para todos os históricos.

No exemplo principal, o plano minimax é **DRDDM**, embora não seja o melhor plano de nenhuma preparação individual. Sua perda máxima é **0,2532196 ponto percentual** em relação ao melhor plano para cada histórico.

## Aquisição, atualização e tarefa

Um bit justo e constante H é a fonte que o registrador deve preservar. Um sensor produz **uma única** observação Y, errada com probabilidade η=0,1. O mesmo Y alimenta três escritas, cada uma com erro 0,02. O substrato começa saudável e passa pelo canal de envelhecimento herdado ao fim da aquisição.

Em seguida, o pesquisador prepara o registrador por um histórico de duas atualizações: DD, DR, RD ou RR. D aplica difusão às células; R executa o votador falível de seis NANDs e reescreve as três células. Esses históricos geram quatro leis físicas, com a mesma duração e uma reserva comum de recursos.

Na fronteira de comparação, o controlador recebe somente seu registrador físico e o programa instalado. O identificador do histórico, H, a saúde do substrato e os resultados internos de reparo não são entradas disponíveis.

A tarefa exige **quatro novas atualizações D/R**, além de permitir até uma manutenção M em um intervalo adicional. A leitura terminal ocorre ao concluir esse trabalho. Existem 96 programas completos: 16 sem manutenção e 80 com manutenção. M reutiliza o votador para solicitar reparo e consome o crédito mesmo quando o voto não pede intervenção.

O objetivo agora é a **fidelidade ao bit-fonte: probabilidade de voto=H**. A alteração do evento terminal está explícita. No domínio global irrestrito, ela produz ranks 11→13; os antigos 10→12 continuam associados à tarefa voto=1.

## Da equivalência entre duas leis à garantia de classe

Se V[h,p] é a fidelidade do plano completo p no histórico h, defina o ótimo informado b[h]=max_q V[h,q]. Para um único plano p compartilhado por toda a classe, o regret uniforme é

\[
R(p)=\max_h\{b[h]-V[h,p]\}.
\]

Esse máximo também é exatamente o pior regret em todo o fecho convexo das preparações. A prova usa diferenças de respostas lineares e encontra um pior caso em um histórico realmente alcançável. Não é necessário instalar um randomizador que gere todas as misturas.

O certificado fornece um histórico e um plano concorrente para a pior perda de cada candidato. Depois de construir a matriz, o cálculo requer O(número de históricos × número de planos) operações racionais. O verificador confere os limites e os testemunhos sem executar novamente a seleção do melhor plano.

Uma classe admite um plano comum com perda zero precisamente quando a interseção dos conjuntos de planos ótimos de todos os históricos é não vazia. Compartilhar somente a primeira ação não basta.

## Resultado concreto

As fidelidades abaixo são probabilidades; todos os cálculos originais são racionais exatos.

| Histórico | DDDDM | RDDDM | DRDDM | Melhor plano individual |
|---|---:|---:|---:|---|
| DD | 0,850027737 | 0,854394749 | 0,852489896 | RDDDM |
| DR | 0,854255095 | 0,851202679 | 0,851722899 | DDDDM |
| RD | 0,852011829 | 0,852940834 | 0,852164675 | RDDDM |
| RR | 0,851501183 | 0,848672758 | 0,849183449 | DDDDM |

DRDDM é o minimax único entre os 96 candidatos. Seu pior regret ocorre em DR, enquanto sua menor fidelidade ocorre em RR. Os dois critérios avaliam consequências diferentes.

DDDDM maximiza a fidelidade mínima, de 85,002774%, e também maximiza o valor na preparação média. Seu regret máximo é maior: 0,4367012 p.p. DRDDM reduz esse regret para 0,2532196 p.p., com fidelidade mínima de 84,918345%.

O contrato pode impor simultaneamente perda relativa δ e piso absoluto τ:

| Perda máxima δ | Fidelidade mínima τ | Programas admissíveis |
|---|---:|---|
| 0,2 p.p. | 84% | Nenhum |
| 0,3 p.p. | 84% | Apenas DRDDM |
| 0,3 p.p. | 85% | Nenhum |
| 0,5 p.p. | 85% | Apenas DDDDM |

As impossibilidades abrangem toda a biblioteca declarada, com um único programa preinstalado. O ótimo informado por histórico é uma referência para medir a perda; sua informação adicional não é disponibilizada ao controlador.

## Quatro coordenadas e o lugar correto de comprimir

Separe a lei conjunta nas submedidas μ0 e μ1, correspondentes a H=0 e H=1. Para qualquer palavra legal w,

\[
V(w)=\operatorname{massa}(\mu_0)+(\mu_1-\mu_0)K_wg.
\]

Isso reutiliza os kernels de 16 estados da rodada anterior. A fonte H permanece fixa e oculta, sem duplicar o mecanismo físico de atualização.

Há uma redução adicional. O contraste d=μ1−μ0 é exchangeável nas células e antissimétrico por complemento: para cada saúde Z, a massa dos padrões com k uns é a negativa da massa com 3−k uns. A aquisição tem essa propriedade; D a preserva por simetria. Em R, a soma nula de d por Z elimina o termo comum da reescrita, restando um múltiplo da diferença entre escrever um e escrever zero. Esse argumento vale apesar da assimetria interna do votador.

Portanto, bastam as massas de contraste para k=0 e k=1 em cada Z: **quatro coordenadas**, para qualquer comprimento de histórico D/R. O offset é 1/2 na aquisição justa. Um certificado de inversa confirma que as respostas antigas já identificam esse domínio.

M geralmente quebra essa propriedade. A implementação calcula a resposta futura na física completa e só então a restringe à fronteira inicial. Propagar um quociente simétrico de oito estados através de M reinicializaria uma simetria perdida e produziria respostas incorretas. Esse erro foi reproduzido como controle negativo.

Quatro mede a dimensão desse espaço linear de contrastes do avaliador. A afirmação não estabelece quatro estados físicos, quatro bits de memória ou uma codificação mínima de toda classe finita normalizada.

## Prever, decidir e preservar fidelidade

O melhor vetor comum de previsões, sem exigir que corresponda a uma lei física, tem erro máximo de **0,2958693 p.p.** sobre as 96 consultas. Escolher o plano que maximiza esse vetor seleciona DDDDM, cujo regret é 0,4367012 p.p. Uma tolerância de previsão ε oferece a garantia geral 2ε para a decisão escolhida por essas previsões; conservar a mesma tolerância para a decisão exige checar as diferenças entre planos no mesmo histórico.

Centros coordenada a coordenada também podem não corresponder a uma preparação física. A prova separa esse centro livre do centro definido pela média das leis, cujo erro é medido diretamente.

Para o sensor único compartilhado, há uma identidade para todo η entre zero e 1/2:

\[
V_\eta=\tfrac12+(1-2\eta)(V_0-\tfrac12).
\]

Assim, as ordenações permanecem iguais para η<1/2; regrets e larguras de intervalos encolhem conforme o sensor piora. Ao mesmo tempo, toda fidelidade fica limitada por **1−η**. Em η=1/2 todos os planos têm regret zero e fidelidade 1/2. O piso absoluto impede que essa perda de informação seja interpretada como uma solução satisfatória.

## Custos e desempenho medido

A reserva comum inclui uma leitura sensorial, três células, seis NANDs reutilizadas, até 48 avaliações de NAND, 21 escritas, 21 oportunidades de atualização das células, um crédito de manutenção e nove intervalos. Para DRDDM, o consumo efetivo varia de 18 a 30 avaliações de NAND e de seis a doze escritas, conforme o histórico. As diferenças de consumo permanecem registradas.

O benchmark usa 64 preparações e 96 planos: 6.144 respostas exatas. Todos os métodos reutilizam consultas calculadas para trás, evitando favorecer a redução contra um baseline que repete desnecessariamente trajetórias.

| Avaliador | Compilar consultas | Lote de 6.144 respostas | Total de um lote, incluindo preparação e codificação | Cache serializado |
|---|---:|---:|---:|---:|
| Lei conjunta, 32 entradas | 0,508 s | 2,010 s | 2,824 s | 444.556 bytes |
| Contraste, 16 entradas | 0,252 s | 1,047 s | 1,620 s | 222.578 bytes |
| Fronteira exchangeável, 8 entradas | 0,271 s | 0,501 s | 1,100 s | 111.377 bytes |
| Contraste antissimétrico, 4 entradas | 0,272 s | 0,238 s | 0,829 s | 54.912 bytes |

São medianas de três execuções locais em Python 3.12.14, com Fraction. Construir o certificado de classe custou mais 0,180 s; verificá-lo, 0,173 s. Esse custo é separado e aplica-se à mesma matriz exata obtida por qualquer avaliador. O certificado serializado ocupa 197.517 bytes. Os tempos individuais, a codificação de preparações e os comprimentos dos racionais estão no artefato de benchmark.

A economia reduz a aritmética e o armazenamento das consultas. O experimento ainda enumera 2^h históricos e (K+2)2^K programas. A eliminação dessa enumeração é uma obrigação seguinte explícita.

## Controles, interpretação e reprodução

Permitindo atualizações opcionais com os mesmos parâmetros físicos, a leitura imediata I é ótima para todos os históricos. O compromisso DRDDM pertence à tarefa de quatro atualizações obrigatórias; esse requisito não deve desaparecer da interpretação.

Os 384 valores principais foram confrontados com o oráculo conjunto de eventos físicos. Também coincidem exatamente nas representações de 32, 16, oito e quatro entradas. A revisão independente reproduziu todos esses confrontos. Os testes incluem aquisição compartilhada, invariância, quebra por manutenção, orçamento, adulteração de certificados e falsa compatibilidade de planos.

O próximo ganho algorítmico deve vir de construir limites e refutações sobre famílias de históricos e planos antes de enumerá-las, preservando as diferenças correlacionadas de valor. A escolha de um resumo numérico passa a ter uma obrigação verificável: demonstrar que nenhum plano omitido viola os pisos e perdas autorizados.

[Laboratório](../lab/reachable_diagnosis.html) · [Prova de classe](../results/reachable-interfaces-proof.md) · [Prova do domínio alcançável](../results/reachable-domain-proof.md) · [Revisão independente](../results/reachable-diagnosis-review.md) · [Dados exatos](../data/reachable-diagnosis-results.json) · [Benchmark](../data/reachable-diagnosis-benchmark.json).

```sh
python -m experiments.reachable_diagnosis_sweep --write --check
python -m experiments.reachable_diagnosis_sweep --benchmark
python -m unittest discover -s tests -p 'test_reachable*.py' -v
node --test tests/reachable-diagnosis-lab.test.mjs
```
