import pyodbc
import pandas as pd

# establish connection
connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=PANDA;'
                      'Database=coba_etl_python;'
                      'Trusted_Connection=yes;')

cursor = connection.cursor()

# Albums, Artist, Genres DataFrame
albums = pd.read_csv('../chinook/Album.csv')
albums_df = pd.DataFrame(albums)
artists = pd.read_csv('../chinook/Artist.csv')
artists_df = pd.DataFrame(artists)
genres = pd.read_csv('../chinook/Genre.csv')
genres_df = pd.DataFrame(genres)

print(albums_df)
print(artists_df)
print(genres_df)

# create table albums
def make_albums():{
    cursor.execute('''
    DROP TABLE IF EXISTS albums;
    CREATE TABLE albums (
        album_id int primary key,
        title varchar(255),
        artist_id int,
    )
    ''')
}

# create table artists
def make_artists():{
    
    cursor.execute('''
    DROP TABLE IF EXISTS artists;
    CREATE TABLE artists (
        artist_id int primary key,
        artist_name varchar(255),
    )
    ''')
}

# create table genres
def make_genres():{
    
    cursor.execute('''
    DROP TABLE IF EXISTS genres;
    CREATE TABLE genres (
        genre_id int primary key,
        genre_name varchar(255),
    )
    ''')
}

make_albums()
make_artists()
make_genres()

#table lists
table = {'albums','artists','genres'}

#clear tables
def clear(table):{
    cursor.execute('DELETE FROM ' + table)
}

for i in table:
    clear(i)


# insert into orders
for row in albums_df.itertuples():
    cursor.execute('''
                INSERT INTO albums (album_id, title, artist_id)
                VALUES (?,?,?)
                ''',
                row.AlbumId, 
                row.Title,
                row.ArtistId,
                )



# insert into artists
for row in artists_df.itertuples():
    cursor.execute('''
                INSERT INTO artists (artist_id, artist_name)
                VALUES (?,?)
                ''',
                row.ArtistId, 
                row.Name,
                )

                
# insert into genres
for row in genres_df.itertuples():
    cursor.execute('''
                INSERT INTO genres (genre_id, genre_name)
                VALUES (?,?)
                ''',
                row.GenreId, 
                row.Name,
                )

# commit queries
connection.commit()