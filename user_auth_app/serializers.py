from django_restframework.serializers import serializer
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from .models import Verity, User
from rest_framework import serializers

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from .models import Verity, User

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


class UserRegisterSerializer(serializers.ModelSerializer):
    # error_message:自定义错误消息提示的格式
    code = serializers.CharField(required=True, allow_blank=False, write_only=True, min_length=4, max_length=4,
                                 help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 })
    # 利用drf中的validators验证username是否唯一
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    pwd = serializers.CharField(required=True)

    # 对code字段单独验证(validate_+字段名)
    def validate_code(self, code):
        verify_records = Verity.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            # five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 获取5分钟之前的时间
            # if last_record.add_time > five_minutes_ago:
            #   raise serializers.ValidationError('验证码过期')
            # 判断验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误1')
            # 不用将code返回到数据库中，只是做验证
            # return code
        else:
            raise serializers.ValidationError('验证码错误2')

    # attrs：每个字段validate之后总的dict
    def validate(self, attrs):

        attrs['mobile'] = attrs['username']
        # 从attrs中删除code字段
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'pwd', 'mobile')
