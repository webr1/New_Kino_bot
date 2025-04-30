from typing import Union, Optional, Tuple, List, Dict, Any
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        """Ma'lumotlar bazasi bilan ulanish poolini yaratadi."""
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            host=config.DB_HOST,
            database=config.DB_NAME,
            password=config.DB_PASS,
        )

    async def execute(
            self,
            sql: str,
            parameters: Optional[Tuple] = None,
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False
    ) -> Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]:
        """SQL so'rovini bajaradi."""
        if not parameters:
            parameters = ()
        if not self.pool:
            await self.create()

        async with self.pool.acquire() as connection:
            connection: Connection
            logger(sql)
            try:
                async with connection.transaction():
                    if fetchall:
                        data = await connection.fetch(sql, *parameters)
                    elif fetchone:
                        data = await connection.fetchrow(sql, *parameters)
                    elif commit:
                        await connection.execute(sql, *parameters)
                        data = None
                    return data
            except asyncpg.PostgresError as e:
                print(f"PostgreSQL error: {e}")
                raise
            finally:
                await connection.close()

    @staticmethod
    def format_args(sql: str, parameters: Dict[str, Any]) -> Tuple[str, Tuple]:
        """SQL so'rovini parametrlarga moslashtiradi."""
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())