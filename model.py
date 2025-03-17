from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    DateTimeField,
    BooleanField,
    EmbeddedDocumentField,
    ReferenceField,
    ListField,
    StringField
)


class Tag(EmbeddedDocument):
    name = StringField()


class Author(Document):
    name = StringField(required=True, unique=True)
    birth_date = DateTimeField()
    birth_location = StringField()
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    # tags = ListField(Tag)
    tags = ListField(EmbeddedDocumentField(Tag))
    quote = StringField(required=True)
    author_id = ReferenceField(Author, required=True)
    meta = {"collection": "quotes"}


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    is_message_sent = BooleanField(default=False)
    phone = StringField()
    preferred_channel = StringField()
    meta = {"collection": "contacts"}
