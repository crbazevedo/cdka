# T3.F / T4.E–F — Reparar, sobreviver e conseguir mudar de arquitetura

**Status:** resultados exatos de modelos finitos, com ferramentas clássicas; originalidade não estabelecida.

> O sistema precisa melhorar a precisão para sempre ou pode pagar para instalar uma organização que tolera seus erros?

## Motivação

No modelo anterior cada erro de ação encerrava a trajetória. Agora distinguimos reduzir erros de torná-los recuperáveis. Mudar a organização é uma intervenção custosa e arriscada, financiada apenas por recursos realmente disponíveis.

## Definições mínimas

| Conceito | Significado |
|---|---|
| Suporte de falhas | Transições com probabilidade positiva, por menor que seja |
| Classe segura | Estados que uma política mantém vivos em toda transição permitida |
| Vida média | Tempo esperado até falha; pode ser alto com sobrevivência infinita zero |
| b, C, h | Recurso atual, capacidade e coleta após acerto |
| K, s | Custo e sucesso da reconfiguração |
| q_N | Confiabilidade por ciclo da arquitetura instalada |

## Formulação

    V_0(b)=1
    V_n(b)=max{q_j V_(n-1)(min(C,b-j+h)), s q_N^(n-1) se b>=K}
    q_j=1-2^-j+0.5*4^-j

A política escolhe como gastar hoje e quando instalar, mas nunca usa recursos ainda não obtidos ou informação oculta sobre W.

## Exemplos e resultados

Dois erros XOR em cascata podem cancelar. Com marginais de 10%, erros independentes dão 18% de erro final e erros perfeitamente compartilhados dão zero nesse circuito. Entretanto, três cópias com votação majoritária falham 2,8% sob erros independentes de 10% e 10% sob falha compartilhada. Arquitetura e evento de falha determinam o efeito da correlação.

Em um sistema com dois componentes e reparo, 1% de dano independente e reparo perfeito do estado degradado dão vida média de 10.198 ciclos, contra 100 para um componente. A falha simultânea continua possível e a sobrevivência infinita é zero.

No exemplo de instalação com capacidade/custo de 8 tokens, coleta de 5 e instalação 90% confiável, o caminho ótimo é:

    b=0 -> gastar 0 -> b=5
    b=5 -> gastar 3 -> b=7
    b=7 -> gastar 4 -> b=8
    b=8 -> instalar.

O sucesso global é 37,3212%; instalar no primeiro momento possível daria 35,1563%. Vale sobreviver melhor antes de instalar, mesmo adiando uma época, nesta configuração específica.

## Limites

Uma arquitetura de três bits, correção ideal e no máximo uma inversão por época tem suporte lógico seguro. Se erros múltiplos voltam a ter probabilidade positiva, o suporte deixa de ser seguro. O resultado não demonstra perfeição sob todo ruído físico. A instalação só oferece uma chance de atingir a organização segura: falhar antes ou durante ela continua possível.

## Papel no CDKA e o que habilita

A pergunta passa de 'qual precisão comprar?' para 'qual transformação torna uma política antes impossível realizável?'. O próximo modelo deve incluir o corretor falível, seu custo de manutenção, um mundo mutável e observações novas custosas. A regra de controle pode mudar, mas seu suporte material não pode desaparecer da análise.

## Simulador

[Laboratório de reconfiguração](../lab/reconfiguration.html): mapa de política por recurso/horizonte, sobrevivência finita e indefinida, trajetória financeira, dependência de erros e vida média com recuperação.

## Provas e antecedentes

[T3.F](../results/T3F-dependence-and-error-topology.md) · [T4.E](../results/T4E-recoverable-faults-and-support.md) · [T4.F](../results/T4F-financed-reconfiguration.md) · [Estratégia v5](../strategy/proof-engine-v5.md).

Hamming (1950), controladores finitos de POMDPs e processos de decisão com consumo/reabastecimento são antecedentes diretos, não invenções atribuídas ao CDKA.
