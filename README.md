# RESTFUL-finance-news-scraper API
News scraper untuk mencari judul berita dengan tag finansial pada 7 portal berita Indonesia. Berita diambil dari website Tribun, Tempo, Liputan6, Detik, Merdeka, Kompas, dan Viva.

### Mulai server dengan menjalankan *serve-api.py*

## Perintah-perintah:

|HTTP Method| Alamat | Keterangan |
|--------|-------|-------|
| GET | http://[localhost]/scrape-news | Cari judul berita dan simpan ke database, csv, dan json|
| GET | http://[localhost]/scrape-news/news-list | Lihat berita yang sudah di-*scrape* |
| GET | http://[localhost]/scrape-news/news-list/123 | Lihat berita ke-123 |
| GET | http://[localhost]/scrape-news/db/list | Lihat berita yang tersimpan di database |
| GET | http://[localhost]/scrape-news/db/flush | Kosongkan database |

Requirement:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-RESTFUL](https://flask-restful.readthedocs.io/en/latest/)
- [Beautifoulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- Sqlite3
