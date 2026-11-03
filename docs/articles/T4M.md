# T4.M — O que nenhuma continuação consegue distinguir

**Contribuição:** compilação exata de distinções necessárias, com provas de fechamento e rastros que demonstram por que uma redução falha.

> Não contar todos os caminhos. Construir apenas as diferenças que podem alterar alguma continuação permitida.

## Motivação

O espaço bruto de estados pode conter muitas variações irrelevantes. Mas não basta agrupar situações porque parecem semelhantes agora: uma intervenção futura pode expor a diferença. O problema é descobrir o que pode ser descartado **sem consultar essa diferença mais tarde**.

Não exigimos que uma propriedade permaneça constante. Exigimos que a descrição reduzida consiga **evoluir por conta própria**, mantendo as respostas das tarefas declaradas.

## Definições mínimas

| Objeto | Significado |
|---|---|
| Q_a | Transição física sob um comando permitido; falhas permanecem na conta |
| g | O que queremos avaliar, por exemplo sobrevivência |
| Q_w g | Valor de uma sequência de operações e observações |
| Assinatura | Respostas a uma base finita de testes de continuação |
| Fechamento | Nenhuma composição permitida produz uma nova distinção independente |

## Formulação

```text
V0 = span{observáveis relevantes}
V(k+1) = span(Vk, Q_a v para cada a e cada v de Vk)
Ao estabilizar: Q_a B = B C_a
Mesma assinatura: μB = νB
Então μ e ν coincidem em todas as continuações declaradas.
```

O algoritmo gera vetores apenas enquanto acrescentam uma distinção independente. Cada vetor guarda um rastro físico que explica sua origem. Um vetor redundante não precisa ter sua árvore de descendentes expandida.

## Resultado no CDKA

No mesmo processo físico das etapas anteriores:

- 80 estados concretos;
- somente manter: quatro direções e quatro classes, em cinco avaliações;
- quatro comandos: 20 direções e 20 classes, em 81 avaliações;
- progressão da dimensão: 1 → 5 → 16 → 20, depois estabilidade comprovada.

As 20 classes são estados do modelo do pesquisador, não uma observação gratuita da saúde oculta para o controlador.

## Exemplo que mostra o risco de comprimir cedo

Dois estados x,y sobrevivem igualmente a qualquer comando isolado. PREPARAR leva x a p e y a q. VERIFICAR preserva p e falha em q. Portanto PREPARAR→VERIFICAR distingue x de y, embora cada passo isolado não distinguisse. A ordem inversa não produz a mesma diferença.

O laboratório exibe o menor rastro separador, não apenas a diferença final.

## Outra surpresa

Dois sistemas podem ter as mesmas leis para todas as ações previamente fixadas. Se um sensor permite escolher a ação conforme a observação, os valores podem ser 100% e 50%. A equivalência depende do repertório de observações e intervenções: uma nova autoridade pode invalidar uma redução antiga.

## O que habilita em seguida?

Um compilador de interfaces: em vez de examinar todas as trajetórias, produz uma assinatura fechada e um certificado. Se a interface for alterada, ele retorna um teste que exige nova distinção. Isso pode apoiar controle e supervisão, desde que os monitores e os programas também sejam fisicamente realizáveis.

## Limites importantes

Dimensão linear não é quantidade de bits. Uma assinatura de duas coordenadas pode distinguir 17 estados. Igualdade de resultados de todas as palavras não é automaticamente uma cadeia de Markov reduzida: verificamos esse requisito separadamente. Algumas famílias não comprimem e precisam de todas as distinções. O ganho demonstrado não elimina a dificuldade de problemas de otimização gerais.

## Simulador

[Abrir o laboratório de fechamento semântico](../lab/semantic_closure.html). Compare o crescimento das palavras formais com o das distinções independentes, veja classes e rastros separadores, e ative os contraexemplos.

## Prova e fontes

[Enunciados e certificados completos](../results/T4M-context-closed-semantics.md). Os instrumentos principais são equivalência de autômatos probabilísticos (Tzeng), compressão orientada a valor (Poupart–Boutilier) e relações de equivalência sob observação parcial (Castro–Panangaden–Precup). O avanço CDKA está na construção, adaptação e avaliação conjunta sob seu contrato físico e operacional.
