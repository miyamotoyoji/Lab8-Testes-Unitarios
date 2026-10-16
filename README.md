# Laboratório 8 — Testes Unitários

Implementação dos quatro exercícios da seção **8. Testes Unitários**. Os slides e o Moodle os numeram como **7.1, 7.2, 7.3 e 7.4**.

| Atividade no Moodle | Entrega |
|---|---|
| 7.1 — Teste Unitário | [Teste pytest com AAA](tests/test_frete_aaa.py) |
| 7.2 — Test Doubles | [Dummy, Stub e Mock](tests/test_logistica_doubles.py) |
| 7.3 — Execução dos Testes | [Capturas e registros](evidencias) |
| 7.4 — TDD | [Código atualizado](src/frete.py) e [testes regionais](tests/test_frete_regional_tdd.py) |

## Resultados

**45 testes aprovados**: 16 da aula anterior, 4 AAA, 2 de serviços isolados e 23 da nova regra regional. Nenhuma chamada real de rede é executada nos testes. Também foi executada no PyCharm a suíte bancária do laboratório 7: 21 métodos coletados; a interface contabiliza 35 resultados incluindo subtestes, todos aprovados, com saída 0.

## Regra de frete

| Subtotal | Norte/Nordeste | Demais regiões ou região omitida |
|---|---:|---:|
| Abaixo de R$250 | R$25 | R$15 |
| De R$250 a R$300, inclusive | R$10 | R$0 |
| Acima de R$300 | R$0 | R$0 |

A taxa de R$10 é somada à base, como pede o enunciado. A exceção usa **superior a 300**, portanto exatamente 300 ainda paga o adicional. A API anterior sem região permanece compatível. Entradas seguem o contrato da [especificação](specs/checkout_frete.md).

## Test doubles

Os três papéis estão definidos e identificados no próprio [arquivo de testes](tests/test_logistica_doubles.py):

| Papel | Implementação | Como aparece no teste |
|---|---|---|
| **Dummy** | Classe `SessaoDummy`, sem dados ou comportamento | `sessao_dummy = SessaoDummy()` preenche `usuario_sessao`; não participa do cálculo. |
| **Stub** | Classe `ServicoLogisticaStub` | `consultar_taxa()` retorna sempre **23.50**, substituindo a API sem rede. |
| **Mock** | `notificacao_mock`, criado com a interface `ServicoNotificacao` | `assert_called_once_with("PED-008")` verifica uma única chamada com o ID correto. |

O teste segue Arrange, Act e Assert, executa a função real `confirmar_frete` e verifica a taxa e a notificação. A lista de eventos comprova que a consulta termina antes da notificação. Um segundo cenário usa `ServicoLogisticaComFalhaStub` e verifica que não há notificação quando a consulta falha.

## TDD executado

1. Escritos os testes regionais antes de modificar o cálculo: [RED real — 23 falhas](evidencias/8.4_RED.txt), commit `3142343`.
2. Implementada a regra regional mínima e propagada a região ao total.
3. Suíte completa verde: [registro detalhado](evidencias/8.3_TODOS_GREEN.txt).
4. Código revisado para manter base única e compatibilidade com os testes anteriores.

## Executar no PyCharm

Abra esta pasta, selecione Python 3.14+ com pytest e execute a configuração **Todos os testes - Lab 8 e aula anterior** incluída em `.run/`. Alternativamente:

```console
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## Origem e histórico

Projeto derivado do [Lab6-SDD-Frete](https://github.com/miyamotoyoji/Lab6-SDD-Frete), preservando os testes anteriores e o histórico. Os relatórios `docs/6.*`, `audit_report.md` e as evidências `6.*` são registros históricos da aula anterior; as regras atuais estão na especificação e neste README. Trabalho feito com assistência de Codex; resultados e capturas são de execuções reais.
