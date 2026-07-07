from quotes.documents import Author, Quote

def test():
    a = Author(fullname="Albert Einstein", description="Physics genius")
    a.save()
    print(f"Автор {a.fullname} успішно збережений в Atlas!")

if __name__ == "__main__":
    test()