import json
from xml.etree import ElementTree
from abc import ABC, abstractmethod


class Document(ABC):
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    @abstractmethod
    def print_document(self, print_type: str) -> None:
        pass


class DisplayDocumentMixin(ABC):
    @abstractmethod
    def display(self, display_type: str) -> None:
        pass


class OperateDocumentMixin(ABC):
    @abstractmethod
    def serialize(self, serialize_type: str) -> str:
        pass


class DisplayBookMixin(DisplayDocumentMixin):
    def display(self, display_type: str) -> None:
        if display_type == "console":
            print(self.content)
        elif display_type == "reverse":
            print(self.content[::-1])
        else:
            raise ValueError(f"Unknown display type: {display_type}")


class OperateBookMixin(OperateDocumentMixin):
    def serialize(self, serialize_type: str) -> str:
        if serialize_type == "json":
            return json.dumps({"title": self.title, "content": self.content})
        elif serialize_type == "xml":
            root = ElementTree.Element("book")
            title = ElementTree.SubElement(root, "title")
            title.text = self.title
            content = ElementTree.SubElement(root, "content")
            content.text = self.content
            return ElementTree.tostring(root, encoding="unicode")
        else:
            raise ValueError(f"Unknown serialize type: {serialize_type}")


class Book(Document, DisplayBookMixin, OperateBookMixin):
    def __init__(self, title: str, content: str) -> None:
        super().__init__(title, content)

    def print_document(self, print_type: str) -> None:
        if print_type == "console":
            print(f"Printing the book: {self.title}...")
            print(self.content)
        elif print_type == "reverse":
            print(f"Printing the book in reverse: {self.title}...")
            print(self.content[::-1])
        else:
            raise ValueError(f"Unknown print type: {print_type}")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            book.display(method_type)
        elif cmd == "print":
            book.print_document(method_type)
        elif cmd == "serialize":
            return book.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
