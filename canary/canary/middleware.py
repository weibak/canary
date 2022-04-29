import re


class SQLLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.db import connection

        response = self.get_response(request)

        for query in connection.queries:
            if query["sql"].startswith("UPDATE") != query["sql"].startswith('UPDATE "django_session"'):
                with connection.cursor() as cursor:
                    table = re.findall(r'"(.*?)"', query["sql"])[0]
                    table_name = str(table)
                    reque = str(query["sql"])
                    new_reque = reque.split()[0]
                    new_query = query["sql"].replace(
                        f'{reque}',
                        f'INSERT INTO "dbcanary_canary" ("table", "canary") VALUES ("{table_name}", "{new_reque}")'
                    )
                    cursor.execute(new_query)
            if query["sql"].startswith("INSERT INTO") != query["sql"].startswith('INSERT INTO "django_session"'):
                with connection.cursor() as cursor:
                    new_query = query['sql'].replace('VALUES ("', 'VALUES ("canary-')
                    cursor.execute(new_query)

        return response
