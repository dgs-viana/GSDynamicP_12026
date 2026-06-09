# SpaceMed - Global Solution

## Integrantes

* Felipe Rodrigues — RM 565341
* Felipe Bonilha — RM 562356
* Joan Campos — RM 562913

## Sobre o projeto

O SpaceMed é um sistema em Python feito para simular uma solução de telemedicina via satélite em comunidades isoladas.

A ideia do projeto é representar uma situação onde pacientes de regiões remotas precisam passar por uma triagem médica, mas o acesso até hospitais ou profissionais de saúde é limitado. Por isso, o sistema organiza os atendimentos em uma fila e permite consultar os dados dos pacientes.

Além disso, o projeto também consulta dados climáticos da API NASA POWER, usando a latitude e longitude da comunidade do paciente. Esses dados ajudam a entender se chuva, calor ou umidade podem dificultar o atendimento ou deslocamento de uma equipe médica.

## Relação com o tema da Global Solution

O tema da Global Solution é ligado à indústria espacial e ao uso de tecnologias espaciais para resolver problemas reais.

O SpaceMed se encaixa nesse tema porque usa o conceito de conectividade via satélite para apoiar atendimentos médicos em regiões isoladas. A API da NASA também foi usada para trazer dados reais sobre o clima das comunidades cadastradas.

## Como o sistema funciona

O sistema carrega os pacientes a partir de um arquivo JSON chamado:

```text
triagens_spacemed.json
```

Cada registro possui informações como:

```text
id, paciente, idade, comunidade, latitude, longitude, sintoma, risco, conexao e status
```

Depois que os dados são carregados, o programa permite:

* ver um resumo do sistema;
* listar todos os pacientes;
* visualizar a fila de atendimento;
* atender o próximo paciente da fila;
* buscar um paciente pelo ID;
* consultar o clima de uma comunidade.

## Estruturas e algoritmos usados

### Fila

Foi usada uma fila para organizar os atendimentos médicos.

A fila funciona no modelo FIFO, ou seja, o primeiro paciente que entra na fila é o primeiro a ser chamado para atendimento.

No código, a fila foi implementada com:

```python
deque
```

### Busca binária

O sistema permite buscar um paciente pelo ID.

Para isso, os registros são ordenados pelo ID e depois é aplicada uma busca binária.

### Recursividade

A busca binária foi implementada usando recursividade. A função vai dividindo a lista ao meio até encontrar o paciente ou até confirmar que ele não existe.

## API utilizada

O projeto usa a API pública NASA POWER para consultar dados climáticos da região do paciente.

Os dados consultados são:

* temperatura média;
* umidade relativa;
* chuva registrada.

Caso a API não responda, o sistema continua funcionando normalmente com os dados do arquivo JSON.

## Arquivos do projeto

```text
Programa_Spacemed.py
triagens_spacemed.json
README.md
```

## Como executar

Para rodar o projeto, abra a pasta no PyCharm ou em outro editor Python e execute o arquivo:

```bash
python Programa_Spacemed.py
```

## Menu do sistema

Ao executar o programa, o menu exibido é:

```text
1. Resumo do sistema
2. Listar pacientes
3. Ver fila de atendimento
4. Atender próximo paciente
5. Buscar paciente por ID
6. Consultar clima por comunidade
0. Sair
```

## Observação

Os dados dos pacientes são fictícios e foram criados apenas para simular o funcionamento do sistema. Os dados climáticos vêm da API NASA POWER.
