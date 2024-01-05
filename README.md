
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
JOIN products p2 ON p2.asin = pp.reference_asin
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
| 548514 | Help Me Talk Right: How to Teach a Child to Say the "R" Sound in 15 Easy Lessons | 0 | Book |
| 548521 | Michelin the Green Guide Berlin and Potsdam (Michelin Green Guide: Berlin and Potsdam) | 0 | Book |
| 548520 | The Diligent: A Voyage through the Worlds of the Slave Trade | 0 | Book |
| 548519 | The Irish Americans: The Immigrant Experience | 0 | Book |
| 548512 | Common Sense About Uncommon Wisdom: Ancient Teachings of Vedanta | 0 | Book |
| 548513 | How To Get The Best Creative Work From Your Agency: Advertising, Interactive And Other Marketing Communications | 0 | Book |
| 548518 | Dona Barbara | 0 | Book |
| 548517 | The Manager's Bible: A Practical Guide for the Current and Future Manager | 0 | Book |
| 548516 | El arte de amar | 0 | Book |
| 548515 | Gods on Earth (Thor, Book 3) | 0 | Book |
| 548545 | I Need Your Loving | 0 | Music |
| 548536 | Improvisations - Jazz In Paris | 0 | Music |
| 548544 | Lucky Man | 0 | Music |
| 548551 | That Travelin' Two-Beat/Sings the Great Country Hits | 0 | Music |
| 370604 | Buzz Buzz | 27 | Music |
| 536884 | A Rush of Blood to the Head | 33 | Music |
| 450096 | Michael Bublé | 42 | Music |
| 187690 | Come Away with Me | 46 | Music |
| 175533 | Songs About Jane | 53 | Music |
| 124898 | Facing Future | 55 | Music |
| 548547 | The Drifter | 0 | DVD |
| 548548 | The House Of Morecock | 0 | DVD |
| 548550 | 1, 2, 3 Soleils: Taha, Khaled, Faudel | 0 | DVD |
| 193107 | Star Wars - Episode I, The Phantom Menace (Widescreen Edition) | 28 | DVD |
| 137401 | Band of Brothers | 47 | DVD |
| 104775 | The Little Mermaid (Limited Issue) | 49 | DVD |
| 547782 | The Wizard of Oz | 55 | DVD |
| 544622 | Star Wars - Episode II, Attack of the Clones (Widescreen Edition) | 85 | DVD |
| 136839 | Fawlty Towers - The Complete Collection | 85 | DVD |
| 7524 | Jerry Seinfeld Live on Broadway: I'm Telling You for the Last Time | 88 | DVD |
| 548526 | From Soup to Nuts | 0 | Video |
| 297444 | The War of the Worlds | 1 | Video |
| 28339 | Shirley Valentine | 2 | Video |
| 113500 | Leslie Sansone - Walk Away the Pounds - Super Fat Burning | 6 | Video |
| 334784 | Robin Hood - Men in Tights | 7 | Video |
| 486684 | Richard Simmons - Sweatin' to the Oldies | 8 | Video |
| 112817 | Howard the Duck | 12 | Video |
| 385458 | Charlotte's Web | 14 | Video |
| 347515 | A Tree Grows in Brooklyn | 16 | Video |
| 297480 | Star Wars - Episode II, Attack of the Clones | 17 | Video |
| 257106 | IlluStory Book Kit | 59 | Toy |
| 465900 | Wizard Card Game Deluxe | 1890 | Toy |
| 305664 | Photostory Junior Book Kit | 2288 | Toy |
| 327405 | Party Tyme Karaoke CD Oldies | 4053 | Toy |
| 922 | Party Tyme Karaoke CD Kids Songs | 7812 | Toy |
| 272037 | Party Tyme Karaoke CD: V2 Super Hits | 10732 | Toy |
| 11660 | The Songs of Britney Spears & Christina Aguilera | 31296 | Toy |
| 421292 | R- Photostory Senior | 45241 | Toy |
| 51902 | PRIMA PUBLISHING Dark Cloud 2 Official Strategy Guide | 339 | Video Games |
| 527037 | ClickArt Christian Publishing Suite 3 | 200 | Software |
| 96696 | RINGDISC Wagner: The Ring Disc | 327 | Software |
| 456958 | Zondervan Bible Study Library: Leader's Edition 5.0 | 1955 | Software |
| 532431 | Just Enough Vocals The Learning Co | 3771 | Software |
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
| 195176 | 083880439X | Wordly Wise: Book 9 | 5.0000000000000000 |
| 100768 | 044667866X | The Curing Season | 5.0000000000000000 |
| 14985 | 0525451358 | Winnie-The-Pooh's Teatime Cookbook | 5.0000000000000000 |
| 227460 | B000005IC4 | Strauss: Die Fledermaus | 5.0000000000000000 |
| 151520 | 0815746091 | The Black-White Test Score Gap | 5.0000000000000000 |
| 119930 | B00005ABIT | Quiet Revolution | 5.0000000000000000 |
| 80957 | 0791019187 | 101 Educational Conversations With Your Kindergartner-1St Grader (One Hundred One Educational Conversations to Have With Your Child) | 5.0000000000000000 |
| 236493 | 1559702192 | La Salle : Explorer of the North American Frontier | 5.0000000000000000 |
| 64279 | B000000T7Z | Garrick Ohlsson - The Complete Chopin Piano Works Vol. 1 ~ Sonatas | 5.0000000000000000 |
| 112785 | B00004Y9XC | The Best of Blind Lemon Jefferson [Yazoo] | 5.0000000000000000 |

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
| 4233 | General | 6 |
| 11141 | Psychology | 11132 |
| 11121 | Adolescent Psychology | 11119 |
| 169660 | Fitness | 404274 |
| 6 | Cooking, Food & Wine | 1000 |
| 6 | Cooking, Food & Wine | 1000 |
| 11132 | Child Psychology | 11119 |
| 11119 | Psychology & Counseling | 10 |
| 404274 | Genres | 404272 |
| 1000 | Subjects | 283155 |
| 1000 | Subjects | 283155 |
| 11119 | Psychology & Counseling | 10 |
| 10 | Health, Mind & Body | 1000 |
| 404272 | VHS | 139452 |
| 283155 | Books | None |
| 283155 | Books | None |
| 10 | Health, Mind & Body | 1000 |
| 1000 | Subjects | 283155 |
| 139452 | None | None |
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
| 5 | A1GN8UJIZLCA59  | Music |
| 6 | A2NJO6YE954DBH  | Music |
| 7 | A1J5KCZC8CMW9I  | Music |
| 8 | A3MOF5KF93Q6WE  | Music |
| 9 | AXFI7TAWD6H6X   | Music |
| 10 | A38U2M9OAEJAXJ  | Music |
| 1 | ATVPDKIKX0DER   | DVD |
| 2 | A3UN6WX5RRO2AG  | DVD |
| 3 | A2NJO6YE954DBH  | DVD |
| 4 | AU8552YCOO5QX   | DVD |
| 5 | A3P1A63Q8L32C5  | DVD |
| 6 | A3LZGLA88K0LA0  | DVD |
| 7 | A82LIVYSX6WZ9   | DVD |
| 8 | A152C8GYY25HAH  | DVD |
| 9 | A16CZRQL23NOIW  | DVD |
| 10 | A1CZICCYP2M5PX  | DVD |
| 1 | ATVPDKIKX0DER   | Video |
| 2 | A3UN6WX5RRO2AG  | Video |
| 3 | A2NJO6YE954DBH  | Video |
| 4 | AU8552YCOO5QX   | Video |
| 5 | A3P1A63Q8L32C5  | Video |
| 6 | A20EEWWSFMZ1PN  | Video |
| 7 | A16CZRQL23NOIW  | Video |
| 8 | A3LZGLA88K0LA0  | Video |
| 9 | A2QRB6L1MCJ53G  | Video |
| 10 | A152C8GYY25HAH  | Video |
| 1 | AH4M07U4YC695   | Toy |
| 1 | ATVPDKIKX0DER   | Toy |
| 1 | A1SB7SB31ETYZH  | Toy |
| 4 | A1QW8PHDJBH4IC  | Toy |
| 4 | A1T3I4JU36IPM5  | Toy |
| 4 | A20R67CABJH79P  | Toy |
| 4 | A20AL96IIDAEBU  | Toy |
| 4 | A1OA2ZW406NQXM  | Toy |
| 4 | A1OSHA4U8RABFY  | Toy |
| 4 | A1K9DVRKH6TZ1L  | Toy |
| 4 | A1LEF9EM2DFDP2  | Toy |
| 4 | A1ITRIM68VLZG3  | Toy |
| 4 | A1ZO50XHPV0QPQ  | Toy |
| 4 | A1BAZPQGXEVWRT  | Toy |
| 4 | A1DTOHMM2Y5KY0  | Toy |
| 4 | A1FPVUL053AKXO  | Toy |
| 4 | A1A2RJXP6T26PD  | Toy |
| 4 | A1ABBKXKUZF85X  | Toy |
| 4 | A2BKFX67DBRYPA  | Toy |
| 4 | AU8PR9XJ17CCB   | Toy |
| 4 | AXNOIMARQCT3M   | Toy |
| 4 | AQJ2XVMHXGN9A   | Toy |
| 4 | AH16IHWEMA61J   | Toy |
| 4 | A34KPXP8CGUBO5  | Toy |
| 4 | A3DWA4FRL41NQD  | Toy |
| 4 | A2PJ7WLZ38F47S  | Toy |
| 4 | A3O19HBWE10FFJ  | Toy |
| 4 | A2KTGCRR7UZRG7  | Toy |
| 4 | A2JTMTR2BZGLX   | Toy |
| 4 | A3UN6WX5RRO2AG  | Toy |
| 4 | A3S4OTTDBRQ6I1  | Toy |
| 4 | A2V5INJFFRP7Z8  | Toy |
| 4 | A2U1T90IOVPBAR  | Toy |
| 4 | A2YO9AKVAHDR9I  | Toy |
| 1 | A3C811U31YG6FS  | Video Games |
| 1 | A226EDS7WDF7S1  | Video Games |
| 1 | A1M4NJYP0WNL8Q  | Video Games |
| 1 | A1T6PXM2M3N84A  | Software |
| 1 | A23DFB8IUTIZM0  | Software |
| 1 | A183K8JAQJW8LZ  | Software |
| 1 | A1XQB8IU7S8WEU  | Software |
| 1 | A1EIVBXG3RD150  | Software |
| 1 | A1F8RIBFWRYM3Y  | Software |
| 1 | A3D5ICIQ8STPCH  | Software |
| 1 | A36NHJPD24UMGJ  | Software |
| 1 | A36T3O4TIC1YDQ  | Software |
| 1 | A37UFPGDSSMEV   | Software |
| 1 | A39UZ9VVRJW4P8  | Software |
| 1 | A2I0ZWBVR0575O  | Software |
| 1 | AK9MWTH6LJF64   | Software |
| 1 | AI9SB5VKUFXDC   | Baby Product |
| 1 | A2LAH8VX720175  | Baby Product |
| 1 | A37TFIP0OMKGMW  | Baby Product |
| 1 | A2IX9TMXDBUCYV  | CE |
| 1 | A1328SYT22GA4U  | CE |
| 1 | A13JU90C7AU3RT  | CE |
| 1 | A1J62O1S6QTHZJ  | CE |
| 1 | A1SFX3CR838F36  | CE |
| 1 | A18ZVYTEDAOF9A  | Sports |
| 1 | A1W180Y9O1FALI  | Sports |
| 1 | AL62LOJKDES3M   | Sports |
| 1 | A2RHSQZ7MAKKCO  | Sports |
| 1 | A3O8EZOX2P399L  | Sports |

