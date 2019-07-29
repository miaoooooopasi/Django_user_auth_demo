from random import choice

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Django_user_auth_demo.settings import APIKEY
from .models import Verity, User
from user_auth_app.permisons import IsOwnerOrReadOnly
from user_auth_app.serializers import VeritySerializers, SmsSerializer, UserSerializers, UserRegisterSerializer
from user_auth_app.utils.tengxun import TengXun


class UserViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializers


class VerityViewSet(ModelViewSet):
    queryset = Verity.objects.all()
    serializer_class = VeritySerializers


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        teng_xun = TengXun(APIKEY)

        code = self.generate_code()

        sms_status = teng_xun.send_sms(code=code, mobile=mobile)

        if sms_status["result"] != 0:
            return Response({
                "mobile": sms_status["errmsg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = Verity(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile,
                'code': code
            }, status=status.HTTP_201_CREATED)


class UserRegisterViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer