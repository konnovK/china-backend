import os


class Config():
    db_user = os.getenv('DB_USER', 'user12345') 
    db_password = os.getenv('DB_PASSWORD', '12345')
    db_host = os.getenv('DB_HOST', 'localhost:5432') 
    db_name = os.getenv('DB_NAME', 'china')
    jwt_secret = os.getenv('JWT_SECRET', 'qwerty12345')

config = Config()
