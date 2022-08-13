from fileinput import filename
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
from .serializers import FileSerializer
from .HelperFunction.helper import process

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      path = (str(Path(__file__).resolve().parent.parent)+"\media")
      filename=file_serializer.data['file'].split("/")[2].split(".")[0]
      results=process(path,filename)
      completeResults={**results,**file_serializer.data}
      return Response(completeResults, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)