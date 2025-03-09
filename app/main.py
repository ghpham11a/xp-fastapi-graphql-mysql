from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.mutations import Mutation
from app.queries import Query

ACCOUNTS_DB: List[Account] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

def create_app() -> FastAPI:

    schema = strawberry.Schema(query=Query, mutation=Mutation)

    """
    Creates and configures the FastAPI application.
    """
    app = FastAPI(lifespan=lifespan)

    # 7. Create a GraphQL router
    graphql_app = GraphQLRouter(schema)

    # 8. Mount the GraphQL router at /graphql
    app.include_router(graphql_app, prefix="/graphql")

    return app

app = create_app()