from django.http import JsonResponse
from elasticsearch import Elasticsearch

es_url = "192.168.50.8:9200"
client = Elasticsearch(es_url, timeout=30)
bucket_size = 1000
search_result_size = 100

def SearchDocument_ES_web(request, text):
    res_query = {"match_phrase": {"name": text}}

    index_name = "doticfull_document"

    response = client.search(index=index_name,
                             _source_includes=['document_id', 'name', 'approval_reference_name', 'approval_date'],
                             request_timeout=40,
                             query=res_query,
                             size=10)

    result = response['hits']['hits']

    total_hits = response['hits']['total']['value']

    if total_hits == 10000:
        total_hits = client.count(body={"query": res_query}, index=index_name, doc_type='_doc')['count']

    return JsonResponse({"result": result,'total_hits': total_hits})