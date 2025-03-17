import os
import aiomysql

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

import strawberry
from strawberry.fastapi import GraphQLRouter

from app.mutations import Mutation
from app.queries import Query

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Read MySQL parameters from environment variables
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user = os.getenv("MYSQL_USER", "myuser")
    mysql_password = os.getenv("MYSQL_PASSWORD", "mypassword")
    mysql_db = os.getenv("MYSQL_DB", "mydatabase")

    # Create the aiomysql pool on startup
    pool = await aiomysql.create_pool(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        db=mysql_db,
        autocommit=True,
        minsize=1,
        maxsize=10,
    )
    app.state.pool = pool
    print("aiomysql pool created")

    # Yield to start handling requests
    yield

    # Cleanup on shutdown
    pool.close()
    await pool.wait_closed()
    print("aiomysql pool closed")

def create_app() -> FastAPI:

    schema = strawberry.Schema(query=Query, mutation=Mutation)

    # Provide request context to resolvers, so we can get the pool
    async def get_context(request: Request):
        return {"request": request}

    """
    Creates and configures the FastAPI application.
    """
    app = FastAPI(lifespan=lifespan)

    # Create a GraphQL router with context_getter
    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context
    )

    # 8. Mount the GraphQL router at /graphql
    app.include_router(graphql_app, prefix="/graphql")

    return app

app = create_app()