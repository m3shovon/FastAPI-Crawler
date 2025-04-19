# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CrawlRequestSerializer
from .utils import crawl_website

class WebsiteCrawlerView(APIView):
    def post(self, request):
        serializer = CrawlRequestSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            data = crawl_website(url)
            return Response({'result': data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
