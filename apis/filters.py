from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilterSet(filters.FilterSet):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others')
    ]
    RELATIONSHIP_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Committed', 'Committed'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced')
    ]
    education = filters.filters.CharFilter(field_name='profile__education')
    hometown = filters.filters.CharFilter(field_name='profile__hometown')
    work = filters.filters.CharFilter(field_name='profile__work')
    gender = filters.filters.ChoiceFilter(
        choices=GENDER_CHOICES, field_name='profile__gender')
    relationship_status = filters.filters.ChoiceFilter(
        choices=RELATIONSHIP_STATUS_CHOICES, field_name='profile__relationship_status')

    class Meta:
        model = User
        fields = ['education', 'hometown', 'work',
                  'gender', 'relationship_status']
