from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from .models import User
from .serializers import ReferralSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer
from rest_framework.authtoken.models import Token



def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
  
@api_view(['POST'])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate token for the user
        token = get_tokens_for_user(user)
        # Return user details along with token
        return Response({
            'user_id': user.id,
            'token': token,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        data = serializer.data
        return Response(data)
    
class ReferralsView(generics.ListAPIView):
    serializer_class = ReferralSerializer

    def get_queryset(self):
        user = self.request.user
        referral_code = user.email  
        return User.objects.filter(referral_code=referral_code)