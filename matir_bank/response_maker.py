from rest_framework.response import Response
from rest_framework import status
"""
GLBOAL RULE
{
	"status": 200,
	"data": {object},
	"error": {
		"code": 101,
		"summary": "string",
		"data": {object}
	}
}
"""
def _response(statusCode, data = {}, error = {}):
	
     return Response({
         'status': statusCode,
         'data' : data,
         'error': error,
     }, status=status.HTTP_200_OK)

def Ok(data):
	return _response(200, data=data)

def Error(error):
	return _response(400, error=error)
