from rest_framework.exceptions import ValidationError
from main_setting.models import MainSetting


class UserSettingHelper:

    @staticmethod
    def checked_for_update_setting(request):
        data = request.data
        for key, value in data.lists():
            if MainSetting.objects.values_list(key, flat=True).last() < int(value[0]):
                raise ValidationError(str(key).replace("_", " ") + "  more is main setting.")
