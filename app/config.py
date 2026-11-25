import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/connect_barang'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
