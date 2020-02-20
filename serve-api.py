from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
import scraper, json, csv, sqlite3

app = Flask(__name__)
api = Api(app)

news_list = []

news_list_fields = {
    'id': fields.Integer,
    'title': fields.String
}

class scrapeNewsApi(Resource):
    def __init__(self):
        super(scrapeNewsApi,self).__init__()
    
    def save_json(self,filename):
        with open(f"{filename}.json",'w') as fp:
            json.dump(news_list,fp,indent=4)

    def save_csv(self,filename):
        with open(f"{filename}.csv",'w',newline='') as csvfile:
            write = csv.DictWriter(csvfile,fieldnames=['id','title'])
            write.writeheader()
            for data in news_list:
                write.writerow(data)

    def create_connection(self):
        conn = sqlite3.connect('newslist.db')
        print("DB Connected")
        return conn

    def insert_news(self,conn,news):
        cur = conn.cursor()
        cur.execute('insert into newslist values (?,?)',news)
        return cur.lastrowid
        
    def save_db(self):
        create_table_if_not_exist = """ CREATE TABLE IF NOT EXISTS newslist (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL
                                ); """
        conn = self.create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(create_table_if_not_exist)

            for news in news_list:
                inp_news = (news.get('id'),news.get('title'))
                # print(inp_news)
                self.insert_news(conn, inp_news)
            conn.commit()

    def get(self):
        news_json = scraper.main()
        news_list.extend(news_json)
        self.save_db()
        self.save_csv('newslist')
        self.save_json('newslist')

        return{'Status':'success'}, 200

    def put(self):
        pass

class newsListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(newsListApi, self).__init__()

    def get(self):
        return {'List Judul': [marshal(news_list,news_list_fields) for news in news_list]}

    def put(self):
        pass
    
class newsApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',type=str, required = True, location = 'json')
        super(newsApi,self).__init__()

    def get(self,id):
        news_title = news_list[id-1]
        if len(news_title) == 0:
            abort(404)
        return {'Judul berita': marshal(news_title, news_list_fields)}
    def put(self,id):
        pass

# class dumpAsJson(Resource):
#     def __init__(self):
#         super(dumpAsJson,self).__init__()
    
#     def get(self,filename):
#         if news_list != []:
#             with open(f"{filename}.json",'w') as fp:
#                 json.dump(news_list,fp,indent=4)
#         else:
#             return {'Status':'empty news list'},400

#     def put(self):
#         pass

# class dumpAsCsv(Resource):
#     def __init__(self):
#         super(dumpAsCsv,self).__init__()
    
#     def get(self,filename):
#         if news_list != []:
#             with open(f"{filename}.csv",'w',newline='') as csvfile:
#                 write = csv.DictWriter(csvfile,fieldnames=['id','title'])
#                 write.writeheader()
#                 for data in news_list:
#                     write.writerow(data)
#             return {'Status':'success'},201
#         else:
#             return {'Status':'empty news list'},400

# class commitToDB(Resource):
#     def __init__(self):
#         super(commitToDB,self).__init__()
    
#     def create_connection(self):
#         conn = sqlite3.connect('newslist.db')
#         print("DB Connected")
#         return conn

#     def insert_news(self,conn,news):
#         cur = conn.cursor()
#         cur.execute('insert into newslist values (?,?)',news)
#         return cur.lastrowid
        
#     def get(self):
#         create_table_if_not_exist = """ CREATE TABLE IF NOT EXISTS newslist (
#                                     id integer PRIMARY KEY,
#                                     title text NOT NULL
#                                 ); """
#         conn = self.create_connection()
#         if conn is not None:
#             c = conn.cursor()
#             c.execute(create_table_if_not_exist)

#             for news in news_list:
#                 inp_news = (news.get('id'),news.get('title'))
#                 # print(inp_news)
#                 self.insert_news(conn, inp_news)
#             conn.commit()
#         return {'Status':'success'},201

class getListFromDB(Resource):
    def __init__(self):
        super(getListFromDB,self).__init__()

    def get(self):
        conn = sqlite3.connect('newslist.db')
        cur = conn.cursor()
        cur.execute("SELECT * from newslist")
        list_from_db = cur.fetchall()

        n = []
        for news_from_db in list_from_db:
            n.append({'id':news_from_db[0], 'title': news_from_db[1]})
        return {'List Judul': [marshal(news_list,news_list_fields) for news in n]}

class flushDB(Resource):
    def __init__(self):
        super(flushDB,self).__init__()

    def get(self):
        conn = sqlite3.connect('newslist.db')
        if conn is not None:
            cur = conn.cursor()
            cur.execute('delete from newslist')
            conn.commit()
        return {'Status':'success'},200


api.add_resource(scrapeNewsApi, '/scrape-news', endpoint='scrapeNews')
api.add_resource(newsListApi, '/scrape-news/news-list',endpoint='newsList')
api.add_resource(newsApi, '/scrape-news/news-list/<int:id>', endpoint='news')
# api.add_resource(dumpAsJson, '/scrape-news/save-json/<filename>',endpoint='saveJson')
# api.add_resource(dumpAsCsv, '/scrape-news/save-csv/<filename>',endpoint='saveCsv')
# api.add_resource(commitToDB, '/scrape-news/db/save', endpoint='saveDB')
api.add_resource(getListFromDB, '/scrape-news/db/list', endpoint='getDB')
api.add_resource(flushDB, '/scrape-news/db/flush', endpoint='flushDB')

if __name__ == '__main__':
    app.run(debug=True)
    