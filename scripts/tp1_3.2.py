import os
import psycopg2
import re


class Config:
    

    def __init__(self) -> None:
        self.Error = False
        self.__downloads()

    
    def __downloads(self,) -> bool:
        
        files = [("./downloads/amazon-meta.txt", "1Ru21bKkHhjRi8QV2pX7n6SdPxrs9UOlC"), ]

        for file, id in files:

            if not os.path.exists(file):
                self.Error = True
                print(f"File {file} not exists")
    


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
            print(curs.query.decode("utf-8").strip())
            print(f"ERROR: {e}")

        finally:
            return results


    def close(self,):
        self.conn.close()


class Category:
    category_id: int = None
    category_name: str = None


    def __init__(self, raw_category: str = None) -> None:

        
        pattern_category = r'([^[\]]+)'

        result = re.findall(pattern_category, raw_category)

        if len(result) != 0:
            
            if len(result) >= 2:
                id = result.pop()
                id = int(id)

                self.category_id  = id
                self.category_name = " ".join(result)
            else:
                try:
                    self.category_id  = int(result[0])
                except:
                    self.category_name = result[0]
        
    def __str__(self) -> str:
        string = f"{self.category_name}[{self.category_id}]"
        return string


class Review:

    customer: str = None
    date: str = None
    rating: int = 0
    votes: int = 0
    helpful: int = 0

    def __init__(self, initialLine: str = None) -> None:

        if initialLine:
            self.__process_line(initialLine)


    def __process_line(self, line):

        date_pattern = r'([0-9]+-[0-9]+-[0-9]+)'

        date = re.findall(date_pattern,  line)
        self.date = date[0] if len(date) != 0 else None

        customer_pattern = r'\b(?:cutomer):\s*([^\s]+)'

        customer = re.findall(customer_pattern, line)
        self.customer = customer[0] if len(customer) != 0 else None

        rating_pattern = r'\b(?:rating):\s*([^\s]+)'

        rating = re.findall(rating_pattern, line)
        self.rating = int(rating[0]) if len(rating) != 0 else None

        votes_pattern = r'\b(?:votes):\s*([^\s]+)'

        votes = re.findall(votes_pattern, line)
        self.votes = int(votes[0]) if len(votes) != 0 else None

        helpful_pattern = r'\b(?:helpful):\s*([^\s]+)'

        helpful = re.findall(helpful_pattern, line)
        self.helpful = int(helpful[0]) if len(helpful) != 0 else None

    def __str__(self,):
        string = f"Date: {self.date}, Customer: {self.customer}, Rating: {self.rating}, "
        string += f"Votes: {self.votes}, Helpful: {self.votes}"

        return string


class Item:
    
    id:         int     = None
    asin:       str     = None
    title:      str     = None
    group:      str     = None
    salesrank:  str     = None
    similar:    str   = None
    categories: list    = None # list of categorys
    reviews:    tuple   = (None,None,None)  # (total, downloaded, avg_rating)
    list_reviews: list  = None  # list of the reviews


    def __str__(self) -> str:
        string = f"Id:\t{self.id}\nASIN:\t{self.asin}\n  title: {self.title}\n  group:{self.group}\n   salesrank:{self.salesrank}\n  "
        string += f"similar:{self.similar}\n "

        if self.categories:
            list_formated = [ "|".join([str(y) for y in x]) for x in self.categories]
            string += f"categories: {len(self.categories)}\n   { list_formated }\n  "
        
        if self.reviews[0]:
            string += f"Reviews: total: {self.reviews[0]} downloaded: {self.reviews[1]} avg_rating: {self.reviews[2]}\n "

        if self.list_reviews:
            for rvw in self.list_reviews:
                string += f"  {str(rvw)}\n "

        string += f"\n"
        return string


def readFile(filename: str = None, callback: callable = None):
    if filename is None:
        raise ValueError("filename is None")

    with open(filename, "r") as f:
        new_item = None

        id_pattern = re.compile(r'Id:\s+([0-9]+)')
        asin_pattern = re.compile(r'\b(?:ASIN):\s*([^\n]+)')
        title_pattern = re.compile(r'\b(?:title):\s*([^\n]+)')
        group_pattern = re.compile(r'\b(?:group):\s*([^\n]+)')
        salesrank_pattern = re.compile(r'\b(?:salesrank):\s*([^\n]+)')
        similar_pattern = re.compile(r'\b(?:similar):\s*([^\n]+)')
        categories_pattern = re.compile(r'\b(?:categories):\s*([^\n]+)')
        reviews_patterns = re.compile(r'\b(?:reviews):\s*([^\n]+)')

        for line in f:
            # Check for the start of an item
            id_match = id_pattern.findall(line)
            if id_match:
                if new_item is not None and callback is not None:
                    callback(new_item)
                try:
                    id_math = int(id_match[0])

                    new_item = Item()
               
                    new_item.id = id_math
                except Exception as e:
                    print(f"Error: {e}")

            if new_item is None:
                continue

            asin_match = asin_pattern.findall(line)
            title_match = title_pattern.findall(line)
            group_match = group_pattern.findall(line)
            salesrank_match = salesrank_pattern.findall(line)
            similar_match = similar_pattern.findall(line)
            categories_match = categories_pattern.findall(line)
            reviews_match = reviews_patterns.findall(line)

            if asin_match:
                new_item.asin = asin_match[0]
            elif title_match:
                new_item.title = title_match[0]
            elif group_match:
                new_item.group = group_match[0]
            elif salesrank_match:
                new_item.salesrank = salesrank_match[0]
            elif similar_match:
                new_item.similar = similar_match[0]
            elif categories_match:
                qnt = int(categories_match[0].strip())
                ctgs = [next(f, None).strip() for _ in range(qnt)]

                list_categorys_raw = [ [ Category(raw_category=y) for y in x.split("|") if len(y) > 0] for x in ctgs]

                new_item.categories = list_categorys_raw
            elif reviews_match:
                rwv = reviews_match[0]
                total = int(re.findall(r'\b(?:total):\s*([^\s]+)', rwv)[0]) if 'total' in rwv else None
                downloaded = int(re.findall(r'\b(?:downloaded):\s*([^\s]+)', rwv)[0]) if 'downloaded' in rwv else None
                avg_rating = float(re.findall(r'\b(?:avg rating):\s*([^\s]+)', rwv)[0]) if 'avg rating' in rwv else None
                new_item.reviews = (total, downloaded, avg_rating)
                new_item.list_reviews = [Review(next(f, None)) for _ in range(downloaded)]

        if new_item is not None and callback is not None:
            callback(new_item)


# Download files
conf = Config()

path_file = "./downloads/amazon-meta.txt"


connect = Connect()


groups = """
CREATE TABLE IF NOT EXISTS groups (
    group_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) UNIQUE
)
"""

products = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER NOT NULL,
    asin CHAR(10) NOT NULL UNIQUE,
    title VARCHAR(300),
    salesrank BIGINT,
    total_reviews INTEGER,
    group_id_fK INTEGER,
    PRIMARY KEY (product_id),
    FOREIGN KEY (group_id_fk) REFERENCES groups (group_id) ON DELETE CASCADE
)
"""

reviews = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL NOT NULL,
    date DATE,
    rating INTEGER,
    votes INTEGER,
    helpful INTEGER,
    customer_id CHAR(15),
    product_id_fk INTEGER,
    PRIMARY KEY (review_id),
    FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE
)
"""

category = """
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER NOT NULL,
        name VARCHAR(50),
        parent_id INTEGER,
        PRIMARY KEY (category_id),
        FOREIGN KEY (parent_id) REFERENCES category (category_id) ON DELETE CASCADE
    )
"""

products_category = """
    CREATE TABLE IF NOT EXISTS ProductsCategories (
        product_id_fk INTEGER NOT NULL,
        category_id_fk INTEGER NOT NULL,
        PRIMARY KEY (product_id_fk, category_id_fk),
        FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE,
        FOREIGN KEY (category_id_fk) REFERENCES category (category_id) ON DELETE CASCADE
    )
"""

product_product = """
 CREATE TABLE IF NOT EXISTS ProductProduct (
    product_id_fk INTEGER NOT NULL,
    reference_asin CHAR(10) NOT NULL,
    PRIMARY KEY (product_id_fk, reference_asin),
    FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE
 )
"""

tables = [groups, products, reviews, category, products_category, product_product]

for table in tables:
    connect.exec_query(query=[table,], debugger=True)

            
group_set = set()

def addDatabase(item: Item):
    
    if not item.title:
        return
    
    group_insert_sql = """
    INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING
    """

    product_insert_sql = """
    INSERT INTO products (product_id, asin, title, salesrank, total_reviews, group_id_fk)
    VALUES (%s,%s,%s,%s,%s, (SELECT group_id FROM groups WHERE name = %s))
    """

    category_insert_sql = """
    INSERT INTO category (category_id, name, parent_id)
    VALUES (%s,%s,%s) ON CONFLICT (category_id) DO NOTHING
    """

    reviews_insert_sql = """
    INSERT INTO reviews (date, rating, votes, helpful, customer_id, product_id_fk)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    productscategories_insert_sql = """
    INSERT INTO productscategories (product_id_fk, category_id_fk)
    VALUES (%s, %s)
    """

    productproduct_insert_sql = """
    INSERT INTO productproduct (product_id_fk, reference_asin)
    VALUES (%s,  %s)
    """
    
    if item.group and item.group not in group_set:
        group_set.add(item.group)
        connect.exec_query(query=[group_insert_sql, (item.group, )])


    connect.exec_query(query=[product_insert_sql, (item.id, item.asin, item.title, item.salesrank, item.reviews[0], item.group)], debugger=True)

    if item.reviews[1]:

        for rvw in item.list_reviews:
            connect.exec_query(query=[reviews_insert_sql, (rvw.date,rvw.rating, rvw.votes, rvw.helpful, rvw.customer, item.id)])
    
    if item.categories:
        for category in item.categories:

            father:Category = category.pop(0)
            connect.exec_query(query=[category_insert_sql, (father.category_id, father.category_name, None)])

            for child in category:
                connect.exec_query(query=[category_insert_sql, (child.category_id, child.category_name, father.category_id)])
                father = child
            
            connect.exec_query(query=[productscategories_insert_sql, (item.id, father.category_id)])

    if item.similar:
        list_sims = [ x.strip() for x in item.similar.split(" ") if len(x.split()) ]
        tol_simis = int(list_sims.pop(0))

        if tol_simis:
            for simi in list_sims:
                connect.exec_query(query=[productproduct_insert_sql, (item.id, simi)])        

def insert_memory(item: Item):
    if not item.title:
        return
    
    addDatabase(item)

if not conf.Error:
    readFile(filename=path_file, callback=insert_memory)

connect.close()