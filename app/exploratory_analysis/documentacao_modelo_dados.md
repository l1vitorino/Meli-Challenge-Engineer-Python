
# Documentação do Modelo de Dados

## Descrição Geral

Este documento descreve o modelo de dados para um sistema de e-commerce, abrangendo as tabelas principais e suas relações. O modelo foi projetado para atender às necessidades de negócio, como o gerenciamento de clientes, itens, categorias e ordens de compra.

## Modelo Entidade-Relacionamento (DER)

Abaixo está o diagrama do modelo entidade-relacionamento que ilustra as tabelas e os relacionamentos do sistema:

![Diagrama do Modelo Entidade-Relacionamento](./der_diagram.png)

## Tabelas do Banco de Dados

### 1. Tabela `Customer`
Tabela responsável por armazenar os dados dos clientes (compradores e vendedores).

#### Estrutura:
- `customer_id`: Identificador único do cliente (PK).
- `name`: Nome do cliente.
- `last_name`: Sobrenome do cliente.
- `gender`: Gênero do cliente (`Male`, `Female`, `Other`).
- `birth_date`: Data de nascimento.
- `is_seller`: Indica se o cliente é um vendedor.
- `created_at`: Data de criação do registro.
- `updated_at`: Data de última atualização.

### 2. Tabela `Category`
Tabela que armazena as categorias dos itens no marketplace.

#### Estrutura:
- `category_id`: Identificador único da categoria (PK).
- `name`: Nome da categoria.
- `item_path`: Caminho da categoria (hierarquia).
- `date_created`: Data de criação da categoria.
- `last_updated`: Data de última atualização.

### 3. Tabela `Item`
Tabela que armazena os produtos disponíveis no marketplace.

#### Estrutura:
- `item_id`: Identificador único do item (PK).
- `name`: Nome do item.
- `category_id`: Referência à categoria (`Category.category_id` - FK).
- `price`: Preço do item.
- `base_price`: Preço base do item.
- `date_created`: Data de criação do item.
- `last_updated`: Data de última atualização do item.
- `is_enabled`: Indica se o item está ativo.

### 4. Tabela `Order`
Tabela que representa as transações realizadas no marketplace.

#### Estrutura:
- `order_id`: Identificador único da ordem (PK).
- `item_id`: Referência ao item comprado (`Item.item_id` - FK).
- `buyer_id`: Referência ao comprador (`Customer.customer_id` - FK).
- `seller_id`: Referência ao vendedor (`Customer.customer_id` - FK).
- `quantity`: Quantidade comprada.
- `price`: Valor total da ordem.
- `date_purchase`: Data da compra.
- `status`: Status da ordem (`Pending`, `Completed`, `Canceled`).
- `buyer_address`: Endereço do comprador.

### 5. Tabela `Daily_Item_State`
Tabela que armazena o estado diário dos itens (preço e ativação).

#### Estrutura:
- `item_id`: Referência ao item (`Item.item_id` - FK).
- `price`: Preço do item no final do dia.
- `is_enabled`: Indica se o item está ativo no final do dia.
- `snapshot_date`: Data do registro.

## Stored Procedure

### `Populate_Daily_Item_State`
Essa procedure insere ou atualiza os dados da tabela `Daily_Item_State`, garantindo que cada item tenha seu estado diário registrado.

#### Exemplo de Uso:
```sql
EXEC Populate_Daily_Item_State;
```

## Consultas SQL

### 1. Listar usuários que fazem aniversário hoje e realizaram mais de 1500 vendas em janeiro de 2020
```sql
SELECT 
    C.name,
    C.last_name,
    COUNT(O.order_id) AS total_sales
FROM Customer C
JOIN "Order" O ON C.customer_id = O.seller_id
WHERE 
    MONTH(C.birth_date) = MONTH(CURRENT_DATE) 
    AND DAY(C.birth_date) = DAY(CURRENT_DATE)
    AND MONTH(O.date_purchase) = 1
    AND YEAR(O.date_purchase) = 2020
GROUP BY C.customer_id, C.name, C.last_name
HAVING COUNT(O.order_id) > 1500;
```

### 2. Top 5 vendedores por mês em 2020 na categoria "Celulares"
```sql
SELECT 
    MONTH(O.date_purchase) AS month,
    YEAR(O.date_purchase) AS year,
    C.name,
    C.last_name,
    COUNT(O.order_id) AS total_sales,
    SUM(O.quantity) AS total_items_sold,
    SUM(O.price) AS total_revenue
FROM "Order" O
JOIN Customer C ON O.seller_id = C.customer_id
JOIN Item I ON O.item_id = I.item_id
JOIN Category CA ON I.category_id = CA.category_id
WHERE 
    YEAR(O.date_purchase) = 2020
    AND CA.name = 'Celulares'
GROUP BY 
    MONTH(O.date_purchase),
    YEAR(O.date_purchase),
    C.customer_id,
    C.name,
    C.last_name
ORDER BY month, total_revenue DESC
LIMIT 5;
```

### 3. Inserir dados na tabela `Daily_Item_State`
```sql
INSERT INTO Daily_Item_State (item_id, price, is_enabled, snapshot_date)
SELECT 
    item_id, 
    price, 
    is_enabled, 
    CAST(GETDATE() AS DATE)
FROM Item
WHERE is_enabled = TRUE;
```

---

## Observação

O diagrama `der_diagram.png` deve ser substituído pela imagem correspondente ao DER. Para renderizar corretamente, insira o arquivo no mesmo diretório deste documento.
