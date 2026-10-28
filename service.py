from connection import *      


async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) Values
        ($1, $2, $3) 
                     """, username, full_name,str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()
        
        

async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        

async def check_admin(telegram_id):
    try:
        conn = await connection_db()
        users = await conn.fetchrow("""
        select * from users where telegram_id = $1 and is_admin = true
                     """, str(telegram_id))
        return users
    except Exception as Error:
        print(f"Get user Error: {Error}")
    finally:
        await conn.close()
                
                
                
async def create_book_db(title, caption, author_id, category_id, publisher):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into books(title, caption, autor_id, category_id, publisher)Values
        ($1, $2, $3, $4, $5) 
                     """, title, caption, int(author_id), int(category_id), publisher)
        return True
    except Exception as Error:
        print(f"Create book Error: {Error}")
        return False
    finally:
        await conn.close()
        
                 
                 
async def create_category_db(title):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into category(category)Values
        ($1) 
                     """, title)
        return True
    except Exception as Error:
        print(f"Create category Error: {Error}")
        return False
    finally:
        await conn.close()
        
        
                 
async def create_author_db(full_name, country):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into autors(full_name, country)Values
        ($1, $2) 
                     """, full_name, country)
        return True
    except Exception as Error:
        print(f"Create author Error: {Error}")
        return False
    finally:
        await conn.close()
        
    
        
        
        
async def get_book():
    try:
        conn = await connection_db()
        books = await conn.fetch("""
        select books.title, books.books_id, books.caption, books.publisher, autors.full_name, category.category from books
        Join autors on autors.autor_id = books.autor_id 
        Join category on category.category_id = books.category_id 
                     """)
        return books
    except Exception as Error:
        print(f"Get books by id Error: {Error}")
    finally:
        await conn.close()
        
        
        
async def get_category():
    try:
        conn = await connection_db()
        categorys = await conn.fetch("""
        select * from category
                     """)
        return categorys
    except Exception as Error:
        print(f"Get categorys by id Error: {Error}")
    finally:
        await conn.close()
        
        
        
        
        
        
async def get_author():
    try:
        conn = await connection_db()
        authors = await conn.fetch("""
        select * from autors
                     """)
        return authors
    except Exception as Error:
        print(f"Get authors by id Error: {Error}")
    finally:
        await conn.close()