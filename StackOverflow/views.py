from django.shortcuts import render
import requests
from django.core.cache import cache
from django.core.paginator import Paginator


def search(request):
    query = request.GET.get('query')
    page = request.GET.get('page', 1)
    per_page = 10

    user_id = request.session.session_key  # Check if the user has exceeded the rate limit
    minute_count = cache.get(f'search_count:{user_id}:minute', 0)
    day_count = cache.get(f'search_count:{user_id}:day', 0)
    if minute_count >= 5:
        return render(request, 'rate_limit_exceeded.html')
    if day_count >= 100:
        return render(request, 'rate_limit_exceeded.html')

    result = cache.get(f'search:{query}:{page}')
    if result is None:
        # If not make a call to Stack Overflow API
        url = f'https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow' \
              f'&pagesize={per_page}&page={page} '
        response = requests.get(url)
        result = response.json()

        cache.set(f'search:{query}:{page}', result, 3600)  # Store the result in cache

    cache.incr(f'search_count:{user_id}:minute')  # Increment the search count for this user
    cache.incr(f'search_count:{user_id}:day')

    questions = result.get('items', [])
    paginator = Paginator(questions, per_page)
    questions_paginated = paginator.get_page(page)

    return render(request, 'search_result.html', {'questions': questions_paginated})
