import json
import os
from model import Author, Quote, Tag
import connect


current_dir = os.path.dirname(__file__)
FILE_AUTHOR = "authors.json"
FILE_QUOTE = "quotes.json"


def load_authors(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        for author in data:
            author_obj = Author(
                name=author.get("fullname"),
                birth_date=author.get("born_date"),
                birth_location=author.get("born_location"),
                description=author.get("description")
            )
            author_obj.save()
    print("Authors are loaded")


def load_quotes(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        for quote in data:
            author = quote.get("author")
            author_obj = Author.objects(name=author).first()
            if author_obj:
                tags = []
                for tag in quote.get("tags"):
                    tag_obj = Tag(name=tag)
                    tags.append(tag_obj)

                quote_obj = Quote(
                    tags=tags,
                    quote=quote.get("quote"),
                    author_id=author_obj
                )
                quote_obj.save()
            else:
                print(f"Author '{author}' is not found")
    print("Quotes are loaded")


if __name__ == "__main__": 
    load_authors(file_path=os.path.join(current_dir, FILE_AUTHOR))
    load_quotes(file_path=os.path.join(current_dir, FILE_QUOTE))
    print("Data is loaded")
