from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from tgbot.config import load_config

config = load_config(".env")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
            max_inactive_connection_lifetime=3
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection()
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users_index (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE, 
        language VARCHAR(255) NOT NULL,
        liked_id VARCHAR(255) NULL,
        disliked_id VARCHAR(255) NULL, 
        orders INT NULL
        );
        """
        await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=2)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, first_name, username, telegram_id, language):
        sql = "INSERT INTO Users_index (first_name, username, telegram_id, language) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, first_name, username, telegram_id, language, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users_index"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users_index WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_user(self, telegram_id, **kwargs):
        sql = "UPDATE Users_index SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Users_index;", fetchval=True, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users_index", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Index_Admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE, 
        name VARCHAR(255) NOT NULL, 
        level INT NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_administrator(self, telegram_id, name, level):
        sql = "INSERT INTO Index_Admins (telegram_id, name, level) VALUES ($1, $2, $3) returning *"
        return await self.execute(sql, telegram_id, name, level, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM Index_Admins"
        return await self.execute(sql, fetch=True)

    async def select_id_admins(self):
        sql = "SELECT telegram_id FROM Index_Admins"
        return await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Index_Admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, telegram_id):
        await self.execute("DELETE FROM Index_Admins WHERE telegram_id=$1", telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE Index_Admins", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_flats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Flats2 (
        id SERIAL PRIMARY KEY,
        category VARCHAR(255) NOT NULL,
        sub1_code INT NULL,
        sub1category VARCHAR(255) NULL,
        sub1category_uz VARCHAR(255) NULL,
        sub2category VARCHAR(255) NULL,
        sub2category_uz VARCHAR(255) NULL,
        article_url VARCHAR(255) NOT NULL,
        article_url_uz VARCHAR(255) NOT NULL,
        likes INT NULL, 
        dislikes INT NULL,
        viewed INT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_flat(self, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, likes, dislikes, viewed):
        sql = "INSERT INTO Flats2 (category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, " \
              "article_url, article_url_uz, likes, dislikes, viewed) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *"
        return await self.execute(sql, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, likes, dislikes, viewed, fetchrow=True)

    async def drop_flats(self):
        await self.execute("DROP TABLE Flats2", execute=True)

    async def select_in_category(self, category):
        sql = "SELECT * FROM Flats2 WHERE category=$1"
        return await self.execute(sql, category, fetch=True)

    async def select_in_sub1category(self, category, sub1category):
        sql = "SELECT * FROM Flats2 WHERE category=$1 AND sub1category=$2"
        return await self.execute(sql, category, sub1category, fetch=True)

    async def select_in_sub1category_uz(self, category, sub1category_uz):
        sql = "SELECT * FROM Flats2 WHERE category=$1 AND sub1category_uz=$2"
        return await self.execute(sql, category, sub1category_uz, fetch=True)

    async def select_in_sub2category(self, category, sub1category, sub2category):
        sql = "SELECT * FROM Flats2 WHERE category=$1 AND sub1category=$2 AND sub2category=$3"
        return await self.execute(sql, category, sub1category, sub2category, fetch=True)

    async def select_in_sub2category_uz(self, category, sub1category_uz, sub2category_uz):
        sql = "SELECT * FROM Flats2 WHERE category=$1 AND sub1category_uz=$2 AND sub2category_uz=$3"
        return await self.execute(sql, category, sub1category_uz, sub2category_uz, fetch=True)

    async def select_flat(self, **kwargs):
        sql = "SELECT * FROM Flats2 WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_flat(self, id, **kwargs):
        sql = "UPDATE Flats2 SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE id=$1"
        return await self.execute(sql, id, *parameters, execute=True)

    async def select_all_flats(self):
        sql = "SELECT * FROM Flats2"
        return await self.execute(sql, fetch=True)

    async def delete_flat(self, id):
        await self.execute("DELETE FROM Flats2 WHERE id=$1", id, execute=True)

    async def select_sub1(self):
        sql = "SELECT sub1_code FROM Flats2"
        return await self.execute(sql, fetch=True)


    # # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # async def create_table_flats2(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS Flats2 (
    #     id SERIAL PRIMARY KEY,
    #     category VARCHAR(255) NOT NULL,
    #     sub1_code INT NULL,
    #     sub1category VARCHAR(255) NULL,
    #     sub1category_uz VARCHAR(255) NULL,
    #     sub2category VARCHAR(255) NULL,
    #     sub2category_uz VARCHAR(255) NULL,
    #     article_url VARCHAR(255) NOT NULL,
    #     article_url_uz VARCHAR(255) NOT NULL,
    #     likes INT NULL,
    #     dislikes INT NULL,
    #     viewed INT NULL
    #     );
    #     """
    #     await self.execute(sql, fetch=True)
    #
    # async def add_flat2(self, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, likes, dislikes, viewed):
    #     sql = "INSERT INTO Flats2 (category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, " \
    #           "article_url, article_url_uz, likes, dislikes, viewed) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *"
    #     return await self.execute(sql, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, likes, dislikes, viewed, fetchrow=True)
    #
    # async def drop_flats2(self):
    #     await self.execute("DROP TABLE Flats2", execute=True)
    #
    # async def delete_flat2(self, id):
    #     await self.execute("DELETE FROM Flats2 WHERE id=$1", id, execute=True)