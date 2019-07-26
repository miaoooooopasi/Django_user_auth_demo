from django_restframework.serializers import serializer
from rest_framework.serializers import Serializer

from .models import Verity, User
from rest_framework import serializers

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from .models import Verity

from Django_user_auth_demo.settings import REGEX_MOBILE


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class VeritySerializers(serializers.ModelSerializer):
    class Meta:
        model = Verity
        fields = "__all__"


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count() != 0:
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证发送频率
        one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if Verity.objects.filter(add_time__gt=one_min_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile
