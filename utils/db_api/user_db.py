from typing import Dict, Any, Optional, List
from .postgresql import Database
from datetime import datetime

class UserDatabase(Database):
    async def create_table_users(self):
        """Foydalanuvchilar jadvalini yaratadi."""
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            username VARCHAR(255) NULL,
            last_active TIMESTAMP NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, commit=True)

    async def add_user(self, telegram_id: int, username: Optional[str], created_at: Optional[datetime] = None):
        """Yangi foydalanuvchi qo'shadi."""
        sql = """
        INSERT INTO Users (telegram_id, username, created_at) 
        VALUES ($1, $2, $3) 
        RETURNING *
        """
        if created_at is None:
            created_at = datetime.now()
        return await self.execute(sql, parameters=(telegram_id, username, created_at), fetchone=True)

    async def select_all_users(self) -> List[Dict[str, Any]]:
        """Barcha foydalanuvchilarni tanlaydi."""
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetchall=True)

    async def select_user(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Berilgan parametrlarga mos foydalanuvchini tanlaydi."""
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchone=True)

    async def count_users(self) -> int:
        """Foydalanuvchilar sonini hisoblaydi."""
        sql = "SELECT COUNT(*) FROM Users"
        result = await self.execute(sql, fetchone=True)
        return result["count"]

    async def delete_users(self):
        """Barcha foydalanuvchilarni o'chiradi."""
        sql = "DELETE FROM Users WHERE TRUE"
        await self.execute(sql, commit=True)

    async def update_user_last_active(self, user_id: int):
        """Foydalanuvchi oxirgi faollik vaqtini yangilaydi."""
        sql = """
        UPDATE Users
        SET last_active = $1
        WHERE id = $2
        """
        last_active = datetime.now()
        await self.execute(sql, parameters=(last_active, user_id), commit=True)

    async def count_users_added_since(self, since_time: datetime) -> int:
        """Berilgan vaqtdan keyin qo'shilgan foydalanuvchilar sonini hisoblaydi."""
        sql = """
        SELECT COUNT(*) FROM Users WHERE created_at >= $1
        """
        result = await self.execute(sql, parameters=(since_time,), fetchone=True)
        return result["count"]

    async def count_active_users_since(self, since_time: datetime) -> int:
        """Berilgan vaqtdan keyin faol bo'lgan foydalanuvchilar sonini hisoblaydi."""
        sql = """
        SELECT COUNT(*) FROM Users WHERE last_active >= $1
        """
        result = await self.execute(sql, parameters=(since_time,), fetchone=True)
        return result["count"]

    async def get_user_mention(self, telegram_id: int) -> str:
        """Foydalanuvchi uchun Telegram mention'ini qaytaradi."""
        user = await self.select_user(telegram_id=telegram_id)
        if user and user["username"]:
            return f"[@{user['username']}](tg://user?id={telegram_id})"
        return f"[ID: {telegram_id}](tg://user?id={telegram_id})"

    async def get_user_id_by_telegram_id(self, telegram_id: int) -> Optional[int]:
        """Telegram ID orqali foydalanuvchi ID'sini qaytaradi."""
        sql = "SELECT id FROM Users WHERE telegram_id = $1"
        result = await self.execute(sql, parameters=(telegram_id,), fetchone=True)
        return result["id"] if result else None