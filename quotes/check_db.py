from quotes.documents import Quote

def check():
    count = Quote.objects.count()
    print(f"Цитат у базі: {count}")
    if count > 0:
        print(f"Перша цитата: {Quote.objects.first().text}")

if __name__ == "__main__":
    check()