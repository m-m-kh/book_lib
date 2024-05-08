from book_lib.book_lib import BookLib



lib = BookLib('lib1')

# b=lib.add_book(title='hesaban',author='hasan',categorie='math')
# print(b)

for i in lib:
    i.remove()

print(lib.find_book())