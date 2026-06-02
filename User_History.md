# 📑 Documento de Especificação: Core-Banking

**Versão:** 1.0  
**Linguagem:** Python 3.11+ (FastAPI)  
**Banco de Dados:** PostgreSQL  

---

## 👤 Epopeia 1: Gestão de Contas Correntes
**Objetivo:** Permitir que novos clientes entrem na plataforma e que o sistema gerencie seus identificadores de forma única e segura.

### 🔹 História de Usuário 1: Criação de Conta
**Como** um sistema cliente (API Gateway / Frontend)  
**Eu quero** registrar uma nova conta informando o documento do cliente  
**Para que** o cliente possa receber depósitos e realizar transações financeiras na plataforma.

* **Critérios de Aceitação:**
    * **Cenário 1: Criação com sucesso**
        * **Dado** que eu envie uma requisição `POST /v1/accounts`
        * **E** o corpo da requisição contenha um `document_number` válido e que não exista no banco
        * **Quando** a requisição for processada
        * **Então** o sistema deve retornar o status `201 Created`
        * **E** o corpo da resposta deve conter o `account_id` gerado e o `document_number`.
    * **Cenário 2: Documento duplicado**
        * **Dado** que eu envie um `document_number` que já está cadastrado no sistema
        * **Quando** a requisição for processada
        * **Então** o sistema deve rejeitar a criação e retornar o status `409 Conflict` com uma mensagem de erro clara.
    * **Cenário 3: Payload inválido**
        * **Dado** que o campo `document_number` esteja vazio, mal formatado ou ausente
        * **Quando** a requisição for enviada
        * **Então** o sistema deve retornar o status `422 Unprocessable Entity` detalhando o erro de validação.

---

### 🔹 História de Usuário 2: Consulta de Saldo e Dados da Conta
**Como** um correntista ou sistema de auditoria  
**Eu quero** consultar os dados de uma conta específica através do seu identificador  
**Para que** eu possa verificar o número do documento associado e o saldo consolidado atual da conta.

* **Critérios de Aceitação:**
    * **Cenário 1: Conta localizada**
        * **Dado** que eu envie uma requisição `GET /v1/accounts/{accountId}`
        * **E** o `{accountId}` exista na base de dados
        * **Quando** a requisição for processada
        * **Então** o sistema deve retornar o status `200 OK`
        * **E** retornar o `account_id`, `document_number` e o `balance` (saldo em tempo real recalculado ou armazenado de forma segura).
    * **Cenário 2: Conta inexistente**
        * **Dado** que o `{accountId}` informado não exista
        * **Quando** a consulta for executada
        * **Então** o sistema deve retornar o status `404 Not Found` com a mensagem `"Account not found"`.

---

## 💸 Epopeia 2: Processamento Base de Transações (Ledger)
**Objetivo:** Garantir a integridade financeira, aplicando regras estritas de negócio para débitos (valores negativos) e créditos (valores positivos), prevenindo fraudes e estouro de saldo.

### 🔹 História de Usuário 3: Movimentação Financeira Assíncrona/Síncrona Segura
**Como** o sistema de core-banking  
**Eu quero** processar uma requisição de transação validando o tipo de operação, o saldo do cliente e chaves de idempotência  
**Para que** o saldo da conta reflita a realidade sem permitir duplicidade de cliques ou saldo negativo não autorizado.

* **Dicionário de Operações:**
    * `1` - PURCHASE (Débito/Armazenado como valor Negativo)
    * `2` - INSTALLMENT PURCHASE (Débito/Armazenado como valor Negativo)
    * `3` - WITHDRAWAL (Débito/Armazenado como valor Negativo)
    * `4` - PAYMENT (Crédito/Armazenado como valor Positivo)

* **Critérios de Aceitação:**
    * **Cenário 1: Transação de Crédito (PAYMENT) com sucesso**
        * **Dado** uma requisição `POST /v1/transactions` com `account_id`, `operation_type_id: 4` e `amount: 100.00`
        * **Quando** processada
        * **Então** o sistema deve salvar o valor como **positivo** (`100.00`)
        * **E** somar o valor ao saldo atual da conta
        * **E** retornar status `201 Created` com os dados da transação.
    * **Cenário 2: Transação de Débito com saldo suficiente**
        * **Dado** que a conta possui `$150.00` de saldo
        * **E** a requisição pede um `PURCHASE` (ID 1) no valor de `$50.00`
        * **Quando** processada
        * **Então** o sistema deve salvar o valor como **negativo** (`-50.00`) no banco de dados
        * **E** o saldo final da conta deve passar a ser `$100.00`
        * **E** retornar status `201 Created`.
    * **Cenário 3: Transação de Débito Negada (Saldo Insuficiente)**
        * **Dado** que a conta possui `$30.00` de saldo
        * **E** a requisição pede um `WITHDRAWAL` (ID 3) no valor de `$50.00`
        * **Quando** processada
        * **Então** o sistema deve abortar a operação (impedindo a escrita no banco)
        * **E** retornar o status `422 Unprocessable Entity` com a mensagem `"Insufficient funds for this operation"`.
    * **Cenário 4: Proteção contra Duplo Clique (Idempotência Mecânica)**
        * **Dado** que uma requisição idêntica envie o cabeçalho `X-Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000`
        * **Quando** o sistema receber essa chave pela segunda vez dentro de um intervalo de segurança de 5 minutos
        * **Então** ele não deve reprocessar o débito/crédito financeiro, apenas retornar o mesmo resultado original armazenado em cache/banco.
