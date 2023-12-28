
# Trabalho 1 de Banco de dados

**Alunos:** Beatriz Braga, Felipe Fraxe e Natanael Bezerra.

## (a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.

-> Query
```sql

(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = 2
ORDER BY helpful DESC, rating DESC
LIMIT 5)

UNION ALL

(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = 2
ORDER BY helpful DESC, rating ASC
LIMIT 5)

```

-> Saida
| date | rating | votes | helpful | customer_id |
| ---- | ------ | ----- | ------- | ----------- |
| 2002-02-06 | 4 | 16 | 16 | A2P6KAWXJ16234  |
| 2004-02-11 | 1 | 13 | 9 | A1CP26N8RHYVVO  |
| 2002-01-24 | 5 | 8 | 8 | A13SG9ACZ9O5IM  |
| 2002-05-23 | 5 | 8 | 8 | A1GIL64QK68WKL  |
| 2002-03-23 | 4 | 6 | 6 | A3GO7UV9XX14D8  |
| 2002-02-06 | 4 | 16 | 16 | A2P6KAWXJ16234  |
| 2004-02-11 | 1 | 13 | 9 | A1CP26N8RHYVVO  |
| 2002-01-24 | 5 | 8 | 8 | A13SG9ACZ9O5IM  |
| 2002-05-23 | 5 | 8 | 8 | A1GIL64QK68WKL  |
| 2002-03-23 | 4 | 6 | 6 | A3GO7UV9XX14D8  |

## (b) Dado um produto, listar os produtos similares com maiores vendas do que ele.

-> Query
```sql

SELECT p2.product_id, p2.asin, p2.title, p2.salesrank
FROM products p1
JOIN productproduct pp ON pp.product_id_fk = p1.product_id
JOIN products p2 ON p2.asin = pp.referenc_asin
WHERE p1.product_id = %s AND p2.salesrank < p1.salesrank
order by p2.salesrank;

```

-> Saida
| product_id | asin | title | salesrank |
| ---------- | ---- | ----- | --------- |
| 299250 | 0738700940 | Lammas | 58836 |
| 62291 | 1567184960 | Yule: A Celebration of Light and Warmth | 103012 |
| 170507 | 0738700525 | Midsummer: Magical Celebrations of the Summer Solstice | 159277 |

## (c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada.

-> Query
```sql

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

```

-> Saida
| date | average_rating |
| ---- | -------------- |
| 2001-12-16 | 5.0000000000000000 |
| 2002-01-07 | 4.5000000000000000 |
| 2002-01-24 | 4.6666666666666667 |
| 2002-01-28 | 4.7500000000000000 |
| 2002-02-06 | 4.6000000000000000 |
| 2002-02-14 | 4.5000000000000000 |
| 2002-03-23 | 4.4285714285714286 |
| 2002-05-23 | 4.5000000000000000 |
| 2003-02-25 | 4.5555555555555556 |
| 2003-11-25 | 4.6000000000000000 |
| 2004-02-11 | 4.2727272727272727 |
| 2005-02-07 | 4.3333333333333333 |

## (d) Listar os 10 produtos líderes de venda em cada grupo de produtos.

-> Query
```sql

SELECT product_id, title, salesrank, name_group
FROM (
    SELECT product_id, title, salesrank, group_id_fk, gp.name as name_group, ROW_NUMBER() OVER (PARTITION BY group_id_fk ORDER BY salesrank) AS group_index
    FROM products
    JOIN groups gp 
    ON gp.group_id = products.group_id_fk
    WHERE salesrank >= 0
)
WHERE group_index <= 10;

```

-> Saida
| product_id | title | salesrank | group |
| ---------- | ----- | --------- | ----- |
| 296 | The Da Vinci Code | 19 | Book |
| 390452 | Sisterhood of the Traveling Pants (Sisterhood of Traveling Pants) | 21 | Book |
| 89000 | The Tipping Point: How Little Things Can Make a Big Difference | 23 | Book |
| 337971 | The Secret Life of Bees | 26 | Book |
| 154855 | Good to Great: Why Some Companies Make the Leap... and Others Don't | 29 | Book |
| 376858 | Angels & Demons | 31 | Book |
| 312527 | The Purpose-Driven Life: What on Earth Am I Here For? | 32 | Book |
| 162283 | Rich Dad, Poor Dad: What the Rich Teach Their Kids About Money--That the Poor and Middle Class Do Not! | 37 | Book |
| 11638 | The South Beach Diet: The Delicious, Doctor-Designed, Foolproof Plan for Fast and Healthy Weight Loss | 38 | Book |
| 62424 | Life of Pi | 42 | Book |
| 370604 | Buzz Buzz | 27 | Music |
| 187690 | Come Away with Me | 46 | Music |
| 175533 | Songs About Jane | 53 | Music |
| 124898 | Facing Future | 55 | Music |
| 370600 | Victor Vito | 62 | Music |
| 270546 | On And On | 68 | Music |
| 54420 | The Beatles 1 | 69 | Music |
| 14861 | Brushfire Fairytales | 75 | Music |
| 327081 | "Creedence Clearwater Revival - Chronicle, Vol. 1: The 20 Greatest Hits" | 87 | Music |
| 352312 | The Hit Singles Collection | 87 | Music |
| 193107 | Star Wars - Episode I, The Phantom Menace (Widescreen Edition) | 28 | DVD |
| 137401 | Band of Brothers | 47 | DVD |
| 104775 | The Little Mermaid (Limited Issue) | 49 | DVD |
| 136839 | Fawlty Towers - The Complete Collection | 85 | DVD |
| 7524 | Jerry Seinfeld Live on Broadway: I'm Telling You for the Last Time | 88 | DVD |
| 369922 | Sex and the City - The Complete First Season | 102 | DVD |
| 344171 | Pride and Prejudice (Special Edition) | 107 | DVD |
| 213611 | The Blue Planet - Seas of Life Collector's Set (Parts 1-4) | 111 | DVD |
| 374726 | 24 - Season Two | 119 | DVD |
| 333747 | Sex and the City - The Complete Second Season | 133 | DVD |
| 297444 | The War of the Worlds | 1 | Video |
| 28339 | Shirley Valentine | 2 | Video |
| 113500 | Leslie Sansone - Walk Away the Pounds - Super Fat Burning | 6 | Video |
| 334784 | Robin Hood - Men in Tights | 7 | Video |
| 112817 | Howard the Duck | 12 | Video |
| 385458 | Charlotte's Web | 14 | Video |
| 347515 | A Tree Grows in Brooklyn | 16 | Video |
| 297480 | Star Wars - Episode II, Attack of the Clones | 17 | Video |
| 407073 | The Jungle Book | 17 | Video |
| 161229 | My Neighbor Totoro | 17 | Video |
| 257106 | IlluStory Book Kit | 59 | Toy |
| 305664 | Photostory Junior Book Kit | 2288 | Toy |
| 327405 | Party Tyme Karaoke CD Oldies | 4053 | Toy |
| 922 | Party Tyme Karaoke CD Kids Songs | 7812 | Toy |
| 272037 | Party Tyme Karaoke CD: V2 Super Hits | 10732 | Toy |
| 11660 | The Songs of Britney Spears & Christina Aguilera | 31296 | Toy |
| 51902 | PRIMA PUBLISHING Dark Cloud 2 Official Strategy Guide | 339 | Video Games |
| 96696 | RINGDISC Wagner: The Ring Disc | 327 | Software |
| 243257 | WINDOWS NT SERVER V4.0 RESOURCE | 3828 | Software |
| 197564 | Baby'S Record Keeper And Memory Box | 1017 | Baby Product |
| 224434 | SPELLING CORRECTOR | 39367 | CE |
| 253628 | Hal Leonard Beginning Bass Guitar 1, Instructional Video, 30 Minutes | 69089 | CE |
| 228901 | Hal Leonard Beginning Guitar 1, Instructional Video, 30 Minutes | 71678 | CE |
| 289495 | FRANKLIN COMP. KJB-1440 Electronic Holy Bible (King James Version) | 84976 | CE |
| 310467 | Yoga Kit Living Arts | 4684 | Sports |

## (e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.

-> Query
```sql

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

```

-> Saida
| product_id | asin | title | mean_rating |
| ---------- | ---- | ----- | ----------- |
| 135107 | B00000138D | Ancestral Voices | 5.0000000000000000 |
| 100768 | 044667866X | The Curing Season | 5.0000000000000000 |
| 119930 | B00005ABIT | Quiet Revolution | 5.0000000000000000 |
| 195176 | 083880439X | Wordly Wise: Book 9 | 5.0000000000000000 |
| 236493 | 1559702192 | La Salle : Explorer of the North American Frontier | 5.0000000000000000 |
| 298929 | 0761919015 | Nonvoters : America's No-Shows | 5.0000000000000000 |
| 227460 | B000005IC4 | Strauss: Die Fledermaus | 5.0000000000000000 |
| 310118 | 0910791481 | How to Read Your Opponents Cards | 5.0000000000000000 |
| 80957 | 0791019187 | 101 Educational Conversations With Your Kindergartner-1St Grader (One Hundred One Educational Conversations to Have With Your Child) | 5.0000000000000000 |
| 150069 | 1587680165 | The Little Tern: A Story of Insight | 5.0000000000000000 |

## (f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto.

-> Query
```sql

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

```

-> Saida
| category_id | name | parent_id | 
| ----------- | ---- | --------- |
| 290249 | General | 169660 |
| 4233 | General | 6 |
| 11156 | General | 11149 |
| 11121 | Adolescent Psychology | 11119 |
| 11141 | Psychology | 11132 |
| 169660 | Fitness | 404274 |
| 6 | Cooking, Food & Wine | 1000 |
| 11149 | Counseling | 11119 |
| 11119 | Psychology & Counseling | 10 |
| 11132 | Child Psychology | 11119 |
| 404274 | Genres | 404272 |
| 1000 | Subjects | 283155 |
| 11119 | Psychology & Counseling | 10 |
| 10 | Health, Mind & Body | 1000 |
| 11119 | Psychology & Counseling | 10 |
| 404272 | VHS | 139452 |
| 283155 | Books | None |
| 10 | Health, Mind & Body | 1000 |
| 1000 | Subjects | 283155 |
| 10 | Health, Mind & Body | 1000 |
| 139452 | None | None |
| 1000 | Subjects | 283155 |
| 283155 | Books | None |
| 1000 | Subjects | 283155 |
| 283155 | Books | None |
| 283155 | Books | None |

## (g) Listar os 10 clientes que mais fizeram comentários por grupo de produto.

-> Query
```sql

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

```

-> Saida
| customer_rank | customer_id | name | 
| ------------- | ----------- | ---- |
| 1 | ATVPDKIKX0DER   | Book |
| 2 | A3UN6WX5RRO2AG  | Book |
| 3 | A14OJS0VWMOSWO  | Book |
| 4 | AFVQZQ8PW0L     | Book |
| 5 | A1K1JW1C5CUSUZ  | Book |
| 6 | A2NJO6YE954DBH  | Book |
| 7 | A3QVAKVRAH657N  | Book |
| 8 | A1NATT3PN24QWY  | Book |
| 9 | A1D2C0WDCSHUWZ  | Book |
| 10 | A2ODBHT4URXVXQ  | Book |
| 1 | ATVPDKIKX0DER   | Music |
| 2 | A3UN6WX5RRO2AG  | Music |
| 3 | A9Q28YTLYREO7   | Music |
| 4 | A2U49LUUY4IKQQ  | Music |
| 5 | A2NJO6YE954DBH  | Music |
| 6 | A1GN8UJIZLCA59  | Music |
| 7 | A1J5KCZC8CMW9I  | Music |
| 8 | A3MOF5KF93Q6WE  | Music |
| 9 | AXFI7TAWD6H6X   | Music |
| 10 | A2EENLV6OQ3DYM  | Music |
| 1 | ATVPDKIKX0DER   | DVD |
| 2 | A3UN6WX5RRO2AG  | DVD |
| 3 | A2NJO6YE954DBH  | DVD |
| 4 | AU8552YCOO5QX   | DVD |
| 5 | A3P1A63Q8L32C5  | DVD |
| 6 | A3LZGLA88K0LA0  | DVD |
| 7 | A16CZRQL23NOIW  | DVD |
| 8 | A82LIVYSX6WZ9   | DVD |
| 9 | A152C8GYY25HAH  | DVD |
| 10 | A1CZICCYP2M5PX  | DVD |
| 10 | A20EEWWSFMZ1PN  | DVD |
| 1 | ATVPDKIKX0DER   | Video |
| 2 | A3UN6WX5RRO2AG  | Video |
| 3 | A2NJO6YE954DBH  | Video |
| 4 | AU8552YCOO5QX   | Video |
| 5 | A20EEWWSFMZ1PN  | Video |
| 5 | A3P1A63Q8L32C5  | Video |
| 7 | A16CZRQL23NOIW  | Video |
| 8 | A2QRB6L1MCJ53G  | Video |
| 9 | A3LZGLA88K0LA0  | Video |
| 10 | A152C8GYY25HAH  | Video |
| 1 | AH4M07U4YC695   | Toy |
| 1 | ATVPDKIKX0DER   | Toy |
| 1 | A1SB7SB31ETYZH  | Toy |
| 4 | A1QW8PHDJBH4IC  | Toy |
| 4 | A1T3I4JU36IPM5  | Toy |
| 4 | A2KTGCRR7UZRG7  | Toy |
| 4 | A1ZO50XHPV0QPQ  | Toy |
| 4 | A20R67CABJH79P  | Toy |
| 4 | A20AL96IIDAEBU  | Toy |
| 4 | A1A2RJXP6T26PD  | Toy |
| 4 | A1ABBKXKUZF85X  | Toy |
| 4 | A1BAZPQGXEVWRT  | Toy |
| 4 | A1OA2ZW406NQXM  | Toy |
| 4 | A1OSHA4U8RABFY  | Toy |
| 4 | A1K9DVRKH6TZ1L  | Toy |
| 4 | A1LEF9EM2DFDP2  | Toy |
| 4 | A1ITRIM68VLZG3  | Toy |
| 4 | A2BKFX67DBRYPA  | Toy |
| 4 | A2PJ7WLZ38F47S  | Toy |
| 4 | A1FPVUL053AKXO  | Toy |
| 4 | AH16IHWEMA61J   | Toy |
| 4 | A34KPXP8CGUBO5  | Toy |
| 4 | A2V5INJFFRP7Z8  | Toy |
| 4 | A2U1T90IOVPBAR  | Toy |
| 4 | A2YO9AKVAHDR9I  | Toy |
| 4 | A3S4OTTDBRQ6I1  | Toy |
| 4 | A3DWA4FRL41NQD  | Toy |
| 4 | A3UN6WX5RRO2AG  | Toy |
| 4 | AQJ2XVMHXGN9A   | Toy |
| 4 | A3O19HBWE10FFJ  | Toy |
| 4 | AU8PR9XJ17CCB   | Toy |
| 4 | AXNOIMARQCT3M   | Toy |
| 1 | A3C811U31YG6FS  | Video Games |
| 1 | A226EDS7WDF7S1  | Video Games |
| 1 | A1M4NJYP0WNL8Q  | Video Games |
| 1 | A1EIVBXG3RD150  | Software |
| 1 | A23DFB8IUTIZM0  | Software |
| 1 | A2I0ZWBVR0575O  | Software |
| 1 | A36T3O4TIC1YDQ  | Software |
| 1 | A36NHJPD24UMGJ  | Software |
| 1 | A37UFPGDSSMEV   | Software |
| 1 | A37TFIP0OMKGMW  | Baby Product |
| 1 | AI9SB5VKUFXDC   | Baby Product |
| 1 | A2LAH8VX720175  | Baby Product |
| 1 | A13JU90C7AU3RT  | CE |
| 1 | A1328SYT22GA4U  | CE |
| 1 | A2IX9TMXDBUCYV  | CE |
| 1 | A1SFX3CR838F36  | CE |
| 1 | A1J62O1S6QTHZJ  | CE |
| 1 | A1W180Y9O1FALI  | Sports |
| 1 | A18ZVYTEDAOF9A  | Sports |
| 1 | A2RHSQZ7MAKKCO  | Sports |
| 1 | A3O8EZOX2P399L  | Sports |
| 1 | AL62LOJKDES3M   | Sports |

