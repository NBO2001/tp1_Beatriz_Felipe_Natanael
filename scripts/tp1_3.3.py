import psycopg2
class Connect:

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
        host="localhost",
        port= 5432,
        database="postgres",
        user="postgres",
        password="db123")

        
    def exec_query(self, query: list, is_select: bool=False, debugger: bool = False) -> list:
        results = []
        try:
            with self.conn:
                with self.conn.cursor() as curs:
                    curs.execute(*query)

                    if debugger:
                        print(curs.query.decode("utf-8").strip())
                    
                    if is_select:
                        results = curs.fetchall()
                    
        except psycopg2.Error as e:
            print(f"ERROR: {e}")

        finally:
            return results


    def close(self,):
        self.conn.close()

conn = Connect()

ID_PRODUCT = 2

sql_question_a = f"""
(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = {ID_PRODUCT}
ORDER BY helpful DESC, rating DESC
LIMIT 5)

UNION ALL

(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = {ID_PRODUCT}
ORDER BY helpful DESC, rating ASC
LIMIT 5)
"""

sql_question_b = """
SELECT p2.product_id, p2.asin, p2.title, p2.salesrank
FROM products p1
JOIN productproduct pp ON pp.product_id_fk = p1.product_id
JOIN products p2 ON p2.asin = pp.reference_asin
WHERE p1.product_id = %s AND p2.salesrank < p1.salesrank
order by p2.salesrank;
"""

sql_question_c = """
SELECT
  date,
  AVG(rating) 
  OVER (PARTITION BY product_id_fk ORDER BY date) AS average_rating_before
FROM
  reviews
WHERE
  product_id_fk = %s
ORDER BY
  date;
"""

sql_question_d = """
SELECT product_id, title, salesrank, name_group
FROM (
    SELECT product_id, title, salesrank, group_id_fk, gp.name as name_group, ROW_NUMBER() OVER (PARTITION BY group_id_fk ORDER BY salesrank) AS group_index
    FROM products
    JOIN groups gp 
    ON gp.group_id = products.group_id_fk
    WHERE salesrank >= 0
)
WHERE group_index <= 10;
"""

sql_question_e = """
SELECT table_help.product_id_fk, pdc.asin, pdc.title, AVG(table_help.rating) AS mean_rating
FROM (
  SELECT rating, product_id_fk
  FROM reviews
  WHERE helpful > 0
) AS table_help
JOIN products pdc ON pdc.product_id = table_help.product_id_fk
GROUP BY table_help.product_id_fk, pdc.asin, pdc.title
ORDER BY mean_rating DESC
LIMIT 10;
"""

sql_question_f = """
WITH RECURSIVE category_tree AS (
    (SELECT ct.category_id, ct.name, ct.parent_id
    FROM category ct
    JOIN productscategories ON ct.category_id = category_id_fk
    JOIN products ON product_id = product_id_fk
    JOIN reviews ON reviews.product_id_fk = product_id
    GROUP BY ct.category_id, product_id
    HAVING AVG(CASE WHEN helpful > 0 THEN rating ELSE NULL END) IS NOT NULL AND AVG(CASE WHEN helpful > 0 THEN helpful ELSE NULL END) IS NOT NULL
    ORDER BY AVG(CASE WHEN helpful > 0 THEN rating ELSE NULL END) DESC, AVG(CASE WHEN helpful > 0 THEN helpful ELSE NULL END) DESC
    LIMIT 5)

    UNION ALL

    SELECT c.category_id, c.name, c.parent_id
    FROM category c
    JOIN category_tree ct ON c.category_id = ct.parent_id
) SELECT *
FROM category_tree;
"""

sql_question_g = """
WITH RankedCustomers AS (
  SELECT
    r.customer_id,
    p.group_id_fk,
    COUNT(*) AS comment_count,
    RANK() OVER (PARTITION BY p.group_id_fk ORDER BY COUNT(*) DESC) AS customer_rank
  FROM
    reviews r
  JOIN
    products p ON r.product_id_fk = p.product_id
  GROUP BY
    r.customer_id, p.group_id_fk
)

SELECT
  rc.customer_rank,
  rc.customer_id,
  g.name
FROM
  RankedCustomers rc
JOIN
  groups g ON rc.group_id_fk = g.group_id
WHERE
  rc.customer_rank <= 10;
"""

results_question_a = conn.exec_query(query=[sql_question_a], is_select=True)
results_question_b = conn.exec_query(query=[sql_question_b, (ID_PRODUCT, )], is_select=True)
results_question_c = conn.exec_query(query=[sql_question_c, (ID_PRODUCT, )], is_select=True)
results_question_d = conn.exec_query(query=[sql_question_d], is_select=True)
results_question_e = conn.exec_query(query=[sql_question_e], is_select=True)
results_question_f = conn.exec_query(query=[sql_question_f], is_select=True)
results_question_g = conn.exec_query(query=[sql_question_g], is_select=True)

conn.close()

a_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} | {a[3]} | {a[4]} |" for a in results_question_a])
b_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} | {a[3]} |" for a in results_question_b])
c_str = "\n".join([ f"| {a[0]} | {a[1]} |" for a in results_question_c])
d_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} | {a[3]} |" for a in results_question_d])
e_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} | {a[3]} |" for a in results_question_e])
f_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} |" for a in results_question_f])
g_str = "\n".join([ f"| {a[0]} | {a[1]} | {a[2]} |" for a in results_question_g])

arq_out = f"""
# Trabalho 1 de Banco de dados

**Alunos:** Beatriz Braga, Felipe Fraxe e Natanael Bezerra.

## (a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.

-> Query
```sql
{sql_question_a}
```

-> Saida
| date | rating | votes | helpful | customer_id |
| ---- | ------ | ----- | ------- | ----------- |
{ a_str }

## (b) Dado um produto, listar os produtos similares com maiores vendas do que ele.

-> Query
```sql
{sql_question_b}
```

-> Saida
| product_id | asin | title | salesrank |
| ---------- | ---- | ----- | --------- |
{ b_str }

## (c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada.

-> Query
```sql
{sql_question_c}
```

-> Saida
| date | average_rating |
| ---- | -------------- |
{ c_str }

## (d) Listar os 10 produtos líderes de venda em cada grupo de produtos.

-> Query
```sql
{sql_question_d}
```

-> Saida
| product_id | title | salesrank | group |
| ---------- | ----- | --------- | ----- |
{ d_str }

## (e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.

-> Query
```sql
{sql_question_e}
```

-> Saida
| product_id | asin | title | mean_rating |
| ---------- | ---- | ----- | ----------- |
{ e_str }

## (f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto.

-> Query
```sql
{sql_question_f}
```

-> Saida
| category_id | name | parent_id | 
| ----------- | ---- | --------- |
{ f_str }

## (g) Listar os 10 clientes que mais fizeram comentários por grupo de produto.

-> Query
```sql
{sql_question_g}
```

-> Saida
| customer_rank | customer_id | name | 
| ------------- | ----------- | ---- |
{ g_str }

"""

with open("output.md", 'w') as f:
    f.write(arq_out)