from typing import Dict, Any, Optional, List
from .postgresql import Database
from datetime import datetime

class KinoDatabase(Database):
    async def create_table_kino(self):
        """Kino jadvalini yaratadi."""
        sql = """
        CREATE TABLE IF NOT EXISTS Kino (
            id SERIAL PRIMARY KEY,
            post_id BIGINT NOT NULL UNIQUE,
            file_id VARCHAR(2000) NOT NULL,
            caption TEXT NULL,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        await self.execute(sql, commit=True)

    async def add_kino(self, post_id: int, file_id: str, caption: Optional[str]) -> None:
        """Yangi kino qo'shadi."""
        sql = """
        INSERT INTO Kino (post_id, file_id, caption, views, created_at, updated_at)
        VALUES ($1, $2, $3, 0, $4, $4)
        """
        timestamp = datetime.now()
        await self.execute(sql, parameters=(post_id, file_id, caption, timestamp), commit=True)

    async def update_kino_caption(self, post_id: int, new_caption: Optional[str]) -> None:
        """Kino caption'ini yangilaydi."""
        sql = """
        UPDATE Kino
        SET caption = $1, updated_at = $2
        WHERE post_id = $3
        """
        updated_at = datetime.now()
        await self.execute(sql, parameters=(new_caption, updated_at, post_id), commit=True)

    async def increment_kino_views(self, post_id: int) -> None:
        """Kino ko'rishlar sonini 1 ga oshiradi."""
        sql = """
        UPDATE Kino
        SET views = views + 1
        WHERE post_id = $1
        """
        await self.execute(sql, parameters=(post_id,), commit=True)

    async def get_kino_views(self, post_id: int) -> int:
        """Kino ko'rishlar sonini qaytaradi."""
        sql = """
        SELECT views FROM Kino
        WHERE post_id = $1
        """
        result = await self.execute(sql, parameters=(post_id,), fetchone=True)
        return result["views"] if result else 0

    async def get_kino_by_post_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Post ID orqali kino ma'lumotlarini qaytaradi."""
        sql = """
        SELECT file_id, caption, views FROM Kino
        WHERE post_id = $1
        """
        result = await self.execute(sql, parameters=(post_id,), fetchone=True)
        return {"file_id": result["file_id"], "caption": result["caption"], "views": result["views"]} if result else None

    async def get_all_kinos(self) -> List[Dict[str, Any]]:
        """Barcha kinolarni qaytaradi."""
        sql = """
        SELECT * FROM Kino
        """
        return await self.execute(sql, fetchall=True)

    async def delete_movie(self, post_id: int) -> None:
        """Kino'ni o'chiradi."""
        sql = """
        DELETE FROM Kino WHERE post_id = $1
        """
        await self.execute(sql, parameters=(post_id,), commit=True)

    async def search_kino_by_caption(self, keyword: str) -> List[Dict[str, Any]]:
            """Caption bo'yicha kinolarni qidiradi."""
            sql = """
            SELECT id, file_id, caption, views FROM Kino
            WHERE caption ILIKE $1
            """
            return await self.execute(sql, parameters=(f"%{keyword}%",), fetchall=True)

    async def get_recent_kinos(self, days: int = 7) -> List[Dict[str, Any]]:
        """So'nggi 'days' kun ichida qo'shilgan kinolarni qaytaradi."""
        sql = """
        SELECT * FROM Kino
        WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '$1 days'
        """
        return await self.execute(sql, parameters=(days,), fetchall=True)

    async def count_all_kinos(self) -> int:
        """Barcha kinolar sonini qaytaradi."""
        sql = """
        SELECT COUNT(*) as total FROM Kino
        """
        result = await self.execute(sql, fetchone=True)
        return result["total"] if result else 0

    async def get_inline_kinos(self, keyword_or_post_id: str) -> List[Dict[str, Any]]:
        """Inline so'rov uchun kinolarni qaytaradi (post_id yoki keyword bo'yicha)."""
        try:
            post_id = int(keyword_or_post_id)
            sql = """
            SELECT id, file_id, caption, views FROM Kino
            WHERE post_id = $1
            """
            return await self.execute(sql, parameters=(post_id,), fetchall=True)
        except ValueError:
            sql = """
            SELECT id, file_id, caption, views FROM Kino
            WHERE caption ILIKE $1
            """
            return await self.execute(sql, parameters=(f"%{keyword_or_post_id}%",), fetchall=True)

    async def get_all_kinos_inline(self) -> List[Dict[str, Any]]:
        """Barcha kinolarni inline so'rovlar uchun qaytaradi."""
        sql = """
        SELECT id, file_id, caption, views 
        FROM Kino
        """
        return await self.execute(sql, fetchall=True)

    async def get_most_viewed_kino(self) -> Optional[Dict[str, Any]]:
        """Eng ko'p ko'rilgan kino'ni qaytaradi."""
        sql = """
        SELECT file_id, caption, views FROM Kino
        ORDER BY views DESC LIMIT 1
        """
        result = await self.execute(sql, fetchone=True)
        return {"file_id": result["file_id"], "caption": result["caption"],
                "views": result["views"]} if result else None

    async def get_latest_kino(self) -> Optional[Dict[str, Any]]:
        """Eng so'nggi qo'shilgan kino'ni qaytaradi."""
        sql = """
        SELECT file_id, caption, created_at FROM Kino
        ORDER BY created_at DESC LIMIT 1
        """
        result = await self.execute(sql, fetchone=True)
        return {"file_id": result["file_id"], "caption": result["caption"],
                "created_at": result["created_at"]} if result else None