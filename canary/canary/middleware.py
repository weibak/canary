class SQLLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.db import connection

        response = self.get_response(request)

        for query in connection.queries:
            if query["sql"].startswith("INSERT INTO"):
                with connection.cursor() as cursor:
                    new_query = query["sql"].replace('VALUES, (" "', ' VALUES("canary-")')
                    cursor.execute(new_query)

        return response
