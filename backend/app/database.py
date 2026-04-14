import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class Database:
    _instance = None
    
    def __init__(self):
        self.connection = None
        self.connect()
        self.init_schema()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def connect(self):
        """Установка соединения с PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 5432)),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                dbname=os.getenv('DB_NAME', 'medication_reminder')
            )
            self.connection.autocommit = False
            logger.info('✅ Успешное подключение к PostgreSQL')
        except Exception as e:
            logger.error(f'❌ Ошибка подключения к PostgreSQL: {e}')
            raise e

    def init_schema(self):
        """Инициализация схемы БД"""
        try:
            with self.connection.cursor() as cursor:
                # Таблицы users, reminders, roles, user_roles (твои существующие)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(100),
                        gender VARCHAR(20),
                        age INTEGER,
                        height_cm INTEGER,
                        weight_kg DECIMAL(5,2),
                        target_weight_kg DECIMAL(5,2),
                        bio TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP
                    );
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reminders (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        medication_name VARCHAR(100) NOT NULL,
                        dosage VARCHAR(50) NOT NULL,
                        reminder_time TIME NOT NULL,
                        days JSONB NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reminder_files (
                        id SERIAL PRIMARY KEY,
                        reminder_id INTEGER NOT NULL REFERENCES reminders(id) ON DELETE CASCADE,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        file_key VARCHAR(255) NOT NULL,
                        file_name VARCHAR(255) NOT NULL,
                        content_type VARCHAR(100),
                        size BIGINT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS roles (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        description TEXT,
                        permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_roles (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, role_id)
                    );
                ''')

                # 🔥 НОВЫЕ ТАБЛИЦЫ: refresh_tokens (БЕЗ индексов внутри)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS refresh_tokens (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        token_hash VARCHAR(255) NOT NULL,
                        jti UUID DEFAULT gen_random_uuid(),
                        expires_at TIMESTAMP NOT NULL,
                        revoked BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(token_hash)
                    );
                ''')

                # 🔥 ИНДЕКСЫ ОТДЕЛЬНО
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_refresh_user ON refresh_tokens(user_id);')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_refresh_revoked ON refresh_tokens(revoked, expires_at);')

                # Инициализация ролей
                cursor.execute("""
                    INSERT INTO roles (name, description, permissions) VALUES 
                    ('guest', 'Гость', '["auth:register","auth:login","auth:verify"]'::jsonb),
                    ('user', 'Пользователь', '["user:read_own","user:update_own","reminder:read_own","reminder:create_own","reminder:update_own","reminder:delete_own","reminder:toggle_own"]'::jsonb),
                    ('admin', 'Администратор', '["user:*","reminder:*","role:*","user:assign_role"]'::jsonb)
                    ON CONFLICT (name) DO NOTHING;
                """)
                
                self.connection.commit()
                logger.info('✅ База данных инициализирована (включая refresh_tokens)')
                
        except Exception as e:
            self.connection.rollback()
            logger.error(f'❌ Ошибка инициализации БД: {e}')
            raise e

    @contextmanager
    def get_cursor(self):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def execute_query(self, query, params=()):
        """Выполнить запрос и вернуть результат"""
        try:
            with self.get_cursor() as cursor:
                logger.info(f"🛠️ Executing: {query}")
                if params:
                    logger.info(f"🛠️ Params: {params}")

                cursor.execute(query, params)

                upper = query.strip().upper()
                if upper.startswith('SELECT'):
                    result = cursor.fetchall()
                    logger.info(f"📊 Query returned {len(result)} rows")
                else:
                    result = cursor.rowcount
                    logger.info(f"📊 Query affected {result} rows")

                return result

        except Exception as e:
            logger.error(f'❌ Query error: {e}')
            if self.connection:
                self.connection.rollback()
            raise e

    def close(self):
        if self.connection:
            try:
                self.connection.close()
                logger.info('✅ PostgreSQL connection closed')
            except Exception as e:
                logger.error(f'❌ Close error: {e}')

db = Database.get_instance()

def get_db():
    return db
    
def init_db():
    db = get_db()
    db.init_schema()
