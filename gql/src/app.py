from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

# Define your data models
@strawberry.type
class Book:
    id: str
    title: str
    author: str


@strawberry.type
class IBook:
    title:str
    author:str

# Sample data
books = [
    Book(id="1", title="1984", author="George Orwell"),
    Book(id="2", title="To Kill a Mockingbird", author="Harper Lee"),
    Book(id="3", title="The Great Gatsby", author="F. Scott Fitzgerald"),
]

# Define queries
@strawberry.type
class Query:
    @strawberry.field
    def book(self, id: str) -> Optional[Book]:
        return next((book for book in books if book.id == id), None)

    @strawberry.field
    def books(self) -> List[IBook]:
        return books

# Define mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        new_book = Book(id=str(len(books) + 1), title=title, author=author)
        books.append(new_book)
        return new_book

# Create Strawberry schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create FastAPI app
app = FastAPI()

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Add GraphQL routes to FastAPI app
app.include_router(graphql_app, prefix="/graphql")

# Optional: Add a root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Book API. Visit /graphql for the GraphQL playground."}
