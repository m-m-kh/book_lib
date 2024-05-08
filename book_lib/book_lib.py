import sqlite3
from pathlib import Path


class BookMixin:
    __id = ''
    
    @property
    def id(self):
        return self.__id
    
    @id.getter
    def id(self):
        if not self.__id:
            kwargs = locals().copy()
            kwargs.pop('self') 
            
            conditions = 'where '
            
            for k,v in kwargs.items():
                if v:
                    if isinstance(v,str): 
                        conditions += f"{k} = '{v}' and "
                    else:
                        conditions += f"{k} = {v} and "
            a = self.db_con.execute(f"""
                            select id from books {conditions[:-4]};
                            """)
            
            self.__id = a.fetchall()[-1][0]
        return self.__id
    
    @id.setter
    def id(self, new_id):
        self.__id = new_id
    
    
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        self.db_con:sqlite3.Connection
        if new_title in ('', ' ',None):
            raise ValueError("title cannot be blank or None.")
        
        self.__title = new_title
        
    @title.deleter
    def title(self):
        self.__title = None
    
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, new_author):
        if new_author in ('', ' ', None):
            raise ValueError('author cannot be blank or None')
        self.__author = new_author
    
    @author.deleter
    def author(self):
        self.__author = None
    
    @property
    def publisher(self):
        return self.__publisher
    
    @publisher.setter
    def publisher(self, new_publisher):
        if new_publisher in ('', ' '):
            new_publisher = None
        self.__publisher = new_publisher
        
    @publisher.deleter
    def publisher(self):
        self.__publisher = None

    @property
    def categorie(self):
        return self.__categorie
    
    @categorie.setter
    def categorie(self, new_categorie):
        if new_categorie in ('', ' ',None):
            raise ValueError('categorie cannot be blank or None')
        self.__categorie = new_categorie
    
    @categorie.deleter
    def categorie(self):
        self.__categorie = None
    
    @property
    def summary(self):
        return self.__summary
    
    @summary.setter
    def summary(self, new_summary):
        if new_summary in ('', ' '):
            new_summary = None
        self.__summary = new_summary
    
    @summary.deleter
    def summary(self):
        self.__summary = None
    

class Book(BookMixin):
    def __init__(self, db_con:sqlite3.Connection):
        self.db_con = db_con
    
    def __save(self):
        self.db_con.execute(f"""
                            insert into books(title,author,categorie, publisher, summary) values (?,?,?,?,?);
                            """,[self.title,self.author,self.categorie,self.publisher,self.summary])
        self.db_con.commit()

    def apply(self):
        self.db_con.execute(f"""
                        update books set title = ? , author = ? ,
                        publisher = ? , categorie = ? , summary = ? where id = ?;
                        """,[self.title,self.author,self.categorie,self.publisher,self.summary,self.id])
        self.db_con.commit()
        
    def remove(self):
        self.db_con.execute(f"""
                        delete from books where id = ?;
                        """,[self.id])
        self.db_con.commit()
        return True
    
    def __repr__(self):
        return f'title: {self.title} | author:{self.author} | categorie: {self.categorie}'
        


class BookLib:
    def __init__(self, db_name):
        self.db_con = sqlite3.connect(Path(__file__).parent.joinpath(db_name+'.db'))
        self.db_con.execute("""
                            create table if not exists books(
                                id integer PRIMARY KEY,
                                title varchar(128) not null,
                                author varchar(128) not null,
                                categorie varchar(128) not null,
                                publisher varchar(128),
                                summary text
                            );
                            """)
        
            
    def add_book(self, title:str, author:str, categorie:str,
                 publisher:str = None,summary:str = None):
                
        book = Book(self.db_con)
        book.title = title
        book.author = author
        book.publisher = publisher
        book.categorie = categorie
        book.summary = summary
        
        book._Book__save()

        return book
    
    def find_book(self, title:str=None, author:str=None,categorie:str=None,
                  publisher:str = None, summary:str = None):
        kwargs = locals().copy()
        kwargs.pop('self') 
        
        conditions = 'where '
        
        for k,v in kwargs.items():
            if v:
                if isinstance(v,str): 
                    conditions += f"{k} = '{v}' and "
                else:
                    conditions += f"{k} = {v} and "
                    
        
        
        books = self.db_con.execute(f"""
                            select * from books {conditions[:-4]};
                            """)
        
        books_list = []
        
        for book in books.fetchall():
            b = Book(self.db_con)
            b.id = book[0]
            b.title = book[1]
            b.author = book[2]
            b.categorie = book[3]
            b.publisher = book[4]
            b.summary = book[5]

            books_list.append(b)
        
        return books_list
    
    def __iter__(self):
        books = self.db_con.execute("""
                            select * from books;
                            """)
    
        for book in books.fetchall():
            b = Book(self.db_con)
            b.id = book[0]
            b.title = book[1]
            b.author = book[2]
            b.categorie = book[3]
            b.publisher = book[4]
            b.summary = book[5]
            yield b
    

    
    
    
    
    
        
