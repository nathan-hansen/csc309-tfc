from rest_framework import generics, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import EnrollClass
from classes.models import Class, ClassTimeTable
from classes.serializers import ClassSerializer
from classes.utils import get_classes_with_spots, get_user_classes


# Create your views here.
class ListUpcomingClassView(generics.ListAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):
        return get_classes_with_spots()

class ListMyClassView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        return get_user_classes(self.request.user)

class ModifyClassView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        classtime = request.data.get('timeid')
        op = request.data.get('op')

        if not classtime or not op:
            return Response({'error': 'Missing class or time'}, status=400)

        if op not in ['enroll', 'drop']:
            return Response({'error': 'Invalid op'}, status=400)

        enroll_class = EnrollClass()
        if enroll_class.check_enroll(user, classtime) and op == 'enroll':
            return Response({'error': 'Already enrolled'}, status=400)
        elif not enroll_class.check_enroll(user, classtime) and op == 'drop':
            return Response({'error': 'Not enrolled'}, status=400)

        classtime_ = get_object_or_404(ClassTimeTable, id=classtime)
        if classtime_.check_full() and op == 'enroll':
            return Response({'error': 'Class is full'}, status=400)

        if op == 'enroll':
            enroll_class.enroll(user, classtime_)
            return Response({'message': 'Enrolled'}, status=200)
        elif op == 'drop':
            enroll_class.drop(user, classtime_)
            return Response({'message': 'Dropped'}, status=200)