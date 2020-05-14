from rest_framework import serializers

from .models import Application, User
from .checkups import ProgramChekup, IECheckup, BlackListCheckup
from .exceptions import BaseCheckupException, AmountNotInRangeException, AgeNotInRangeException, UserIsIEException, UserIsBlackListedException


REJECTION_MAPPING = {
    AmountNotInRangeException: Application.Reason.amount_not_in_range,
    AgeNotInRangeException: Application.Reason.age_not_in_range,
    UserIsIEException: Application.Reason.user_is_ie,
    UserIsBlackListedException: Application.Reason.user_is_blacklisted
}

class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return obj.name


class ApplicationSerializer(serializers.ModelSerializer):
    applied_by = serializers.CharField()
    rejection_reason = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
                'status': {'read_only': True},
                'rejection_reason': {'read_only': True},
        }
        checkups = (ProgramChekup, IECheckup, BlackListCheckup)


    def get_rejection_reason(self, application):
        return application.get_rejection_reason_display()

    def validate(self, attrs):
        attrs['applied_by'], _ = User.objects.get_or_create(personal_number=attrs['applied_by'])
        try:
            for checkup in self.Meta.checkups:
                checkup(Application(**attrs)).perform_check()
            attrs['status'] = Application.Status.confirmed
        except BaseCheckupException as e:
            attrs.update({
                'status': Application.Status.rejected,
                'rejection_reason': REJECTION_MAPPING[type(e)]
            })
        return attrs


