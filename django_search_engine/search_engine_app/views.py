from datetime import datetime

from django.shortcuts import render
from elasticsearch import Elasticsearch


client = Elasticsearch('127.0.0.1', port='9200')
# Create your views here.


def index(request):
    return render(request, 'index.html')


def result(request):
    key_words = request.GET.get('q', '')
    page = request.GET.get('p', '1')
    try:
        page = int(page)
    except:
        page = 1
    start_time = datetime.now()
    response = client.search(
        index='cnblog_text',
        doc_type='doc',
        body={
            'query': {
                "multi_match": {
                    "query": key_words,
                    "fields": ["title", "description"]
                }
            },
            "from": (page - 1) * 10,
            "size": 10,
            "highlight": {
                "pre_tags": ['<span class="keyWord">'],
                "post_tags": ['</span>'],
                "fields": {
                    "title": {},
                    "description": {}
                }
            }
        }
    )
    end_time = datetime.now()
    dif_time = (end_time-start_time)
    # 分析数据解析数据用
    # pprint(response)
    total_nums = response['hits']['total']
    hit_list = []
    if (page % 10) > 0:  # 计算页数
        paga_nums = int(total_nums / 10) + 1
    else:
        paga_nums = int(total_nums / 10)
    for hit in response['hits']['hits']:
        hit_dict = {}
        if 'title' in hit['highlight']:
            hit_dict['title'] = hit['highlight']['title']
        else:
            hit_dict['title'] = hit['_source']['title']
        if 'description' in hit['highlight']:
            hit_dict['description'] = hit['highlight']['description']
        else:
            hit_dict['description'] = hit['_source']['description']
        hit_dict['url'] = hit['_source']['url']
        hit_dict['riqi'] = hit['_source']['riqi']
        hit_dict['score'] = hit['_score']
        hit_dict["source_site"] = "博客园"
        hit_list.append(hit_dict)
    return render(request, 'result.html', locals())
