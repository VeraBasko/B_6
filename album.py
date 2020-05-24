
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

def connect_db(db_path):
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(db_path)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

    def __init__(self, year, artist, genre, album):
        self.year = year
        self.artist = artist
        self.genre = genre
        self.album = album


def save_album(album_data):
    """Сохранение нового альбома

    :param album_data: данные об альбоме
    :return: сообщение о добавлении данных в базу
    """
    try:
        error_text = ''
        now = datetime.now()  # current date and time
        now_year = now.strftime("%Y")
        year = int(album_data.get('year', now_year))
        artist = str(album_data.get('artist', 'Неизвестен'))
        genre = str(album_data.get('genre', 'Неизвестен'))
        album = album_data.get('album')
        if not album:
            error_text = 'Альбом не задан'
            raise ValueError
        session = connect_db(DB_PATH)
        if int(now_year) <= year and year > 0:
            new_album = Album(year, artist, genre, album)
            session.add(new_album)
            session.commit()
        else:
            error_text = 'Год больше текущего, альбом еще не вышел'
            raise ValueError

    except ValueError:
        return f"Не удалось добавить данные в БД. " + error_text
    return f"В базу данных добавлен альбом {album} исполнителя {artist}"

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db(DB_PATH)
    albums = session.query(Album).filter(Album.artist == artist).all()
    if albums:
        count_albums = len(albums)
    else:
        count_albums = 0
    return albums, count_albums
