import sqlite3
import hashlib
import os

class DatabaseManager:
    def __init__(self):
        # 确保数据目录存在
        db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.db_path = os.path.join(db_dir, 'users.db')
        self.init_database()

    def init_database(self):
        """初始化数据库，创建用户表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def hash_password(self, password):
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, role, name=None, email=None):
        """注册新用户"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查用户名是否已存在
            cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return False, "用户名已存在"
            
            # 插入新用户
            hashed_password = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password, role, name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashed_password, role, name, email))
            
            conn.commit()
            return True, "注册成功"
        except Exception as e:
            return False, f"注册失败: {str(e)}"
        finally:
            conn.close()

    def verify_user(self, username, password, role):
        """验证用户登录"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取用户信息
            cursor.execute('''
                SELECT password, role FROM users 
                WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            if not user_data:
                return False, "用户不存在"
            
            stored_password, user_role = user_data
            
            # 验证密码和角色
            if self.hash_password(password) != stored_password:
                return False, "密码错误"
            
            if role != user_role:
                return False, "用户角色不匹配"
            
            return True, "登录成功"
        except Exception as e:
            return False, f"登录失败: {str(e)}"
        finally:
            conn.close()

    def get_user_info(self, username):
        """获取用户信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, role, name, email, created_at
                FROM users WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            if user_data:
                return {
                    'id': user_data[0],
                    'username': user_data[1],
                    'role': user_data[2],
                    'name': user_data[3],
                    'email': user_data[4],
                    'created_at': user_data[5]
                }
            return None
        finally:
            conn.close()

    def get_all_users(self, role_filter=None):
        """获取所有用户信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if role_filter:
                cursor.execute('''
                    SELECT id, username, role, name, email, created_at
                    FROM users WHERE role = ?
                    ORDER BY created_at DESC
                ''', (role_filter,))
            else:
                cursor.execute('''
                    SELECT id, username, role, name, email, created_at
                    FROM users
                    ORDER BY created_at DESC
                ''')
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row[0],
                    'username': row[1],
                    'role': row[2],
                    'name': row[3],
                    'email': row[4],
                    'created_at': row[5]
                })
            return users
        finally:
            conn.close()

    def reset_user_password(self, username):
        """重置用户密码为默认密码123456"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            default_password = self.hash_password('123456')
            cursor.execute('''
                UPDATE users SET password = ?
                WHERE username = ?
            ''', (default_password, username))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"重置密码失败: {e}")
            return False
        finally:
            conn.close()

    def delete_user(self, username):
        """删除用户"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"删除用户失败: {e}")
            return False
        finally:
            conn.close() 