from django.urls import path
from .views import WebsiteCrawlerView

urlpatterns = [
    path('crawl/', WebsiteCrawlerView.as_view(), name='website-crawler'),
]
