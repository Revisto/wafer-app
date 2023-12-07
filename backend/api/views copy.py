from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import User

@api_view(['GET'])
def user_balance(request):
    username = request.GET.get("username")
    try:
        user = User.objects.get(username=username)
    
    except User.DoesNotExist:
        new_user = User(username=username, balance=500)
        new_user.save()
        user = User.objects.get(username=username)

    return Response({"username": user.username, "balance": user.balance})