from elasticsearch_dsl import Document, Text, Keyword, Date, analyzer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['127.0.0.1'])
ik_analyzer = analyzer('ik_max_word')


class CnblogsType(Document):
    title = Text(analyzer='ik_max_word')
    description = Text(analyzer='ik_max_word')
    url = Keyword()
    riqi = Date()

    class Index:
        name = 'cnblog_text'
        settings = {
            'number_of_shards': 5,
        }


es = connections.create_connection(CnblogsType)

if __name__ == '__main__':
    CnblogsType.init()
