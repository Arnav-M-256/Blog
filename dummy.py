import app

books = app.get_all_books()
for book in books:
    print(list(book))