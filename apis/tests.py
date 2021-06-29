import io
from PIL import Image
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import response, status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from user_profile.models import Feed
User = get_user_model()


def user_register_request(client, data):
    url = reverse('api:user_register')
    response = client.post(url, data, format='json')
    return response


def user_login_request(client, data):
    url = reverse('api:user_login')
    response = client.post(url, data, format='json')
    return response


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


def create_post_request(client, data):
    url = reverse('api:post')
    return client.post(url, data)


def get_post_request(client, id=None):
    url = '/api/post/'
    if id:
        url += '?id={}'.format(id)
    return client.get(url)


class TestRegistration(APITestCase):
    incorrect_user = {
        'email': 'testuser@gmail.com',
        'password': '12345',
        'confirm_password': '1234a',
        'first_name': 'Hussnain',
        'gender': 'male',
        'birthday': '1234'
    }

    correct_user = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }

    def test_incorrect_user(self):
        response = user_register_request(self.client, self.incorrect_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_user(self):
        response = user_register_request(self.client, self.correct_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@gmail.com')
        self.assertEqual(
            Feed.objects.count(), 1)
        self.assertEqual(
            Feed.objects.get().feed_template.feed_type, 'register')


class TestLogin(APITestCase):
    correct_user_login_creds = {
        'username': 'testuser@gmail.com',
        'password': 'cnc4312056'
    }
    incorrect_user_login_creds = {
        'username': 'test@gmail.com',
        'password': '12345'
    }
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }

    def setUp(self):
        user_register_request(self.client, self.user_reg_data)

    def test_correct_signin(self):
        response = user_login_request(
            self.client, self.correct_user_login_creds)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(Token.objects.get(
            user__email=self.correct_user_login_creds['username'])), response.data['token'])

    def test_incorrect_signin(self):
        response = user_login_request(
            self.client, self.incorrect_user_login_creds)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserPasswordChange(APITestCase):
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }
    correct_password_change_data = {
        'current_password': 'cnc4312056',
        'new_password': 'ubook5420',
        'confirm_new_password': 'ubook5420'
    }
    incorrect_password_change_data = {
        'current_password': 'ubook5420',
        'new_password': '1234',
        'confirm_new_password': '1234'
    }

    def change_password_request(self, data):
        url = reverse('api:change_password')
        response = self.client.patch(url, data, format='json')
        return response

    def setUp(self):
        # Normal user
        user_register_request(self.client, self.user_reg_data)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=self.user_reg_data['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

    def test_with_correct_data(self):
        response = self.change_password_request(
            self.correct_password_change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.correct_token = Token.objects.get(
            user__email=self.user_reg_data['email']).key
        self.assertEqual(response.data['token'], self.correct_token)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token)

    def test_with_incorrect_data(self):
        response = self.change_password_request(
            self.incorrect_password_change_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_auth(self):
        self.client.credentials()
        response = self.change_password_request(
            self.correct_password_change_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserProfilePicturesUpload(APITestCase):
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }

    def setUp(self):

        # Normal user
        user_register_request(self.client, self.user_reg_data)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=self.user_reg_data['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

    def test_profile_pictures_update(self):
        url = reverse('api:update_profile_pictures')

        profile_picture = generate_photo_file()
        cover_picture = generate_photo_file()
        data = {
            'profile_picture': profile_picture,
            'cover_picture': cover_picture}

        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserPosts(APITestCase):
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }

    correct_text_post_data = {
        'content': 'this is a test post',
    }

    correct_photo_post_data = {
        'image': generate_photo_file()
    }

    correct_complete_post_data = {
        'content': 'this is post with image and text',
        'image': generate_photo_file()
    }

    def setUp(self):

        # Normal user
        user_register_request(self.client, self.user_reg_data)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=self.user_reg_data['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

    def test_create_text_post(self):
        response = create_post_request(
            self.client, self.correct_text_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feed.objects.filter(
            user__email=self.user_reg_data['email']).count(), 2)
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__content=self.correct_text_post_data['content']).feed_template.content, self.correct_text_post_data['content'])
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__content=self.correct_text_post_data['content']).feed_template.feed_type, 'add_new_text')

    def test_invalid_post(self):
        response = create_post_request(self.client, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_text_post(self):
        response = create_post_request(
            self.client, self.correct_photo_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feed.objects.filter(
            user__email=self.user_reg_data['email']).count(), 2)
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__image__icontains='test').feed_template.feed_type, 'add_new_photo')
        self.assertNotEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__feed_type='add_new_photo').feed_template.image, None)

    def test_complete_post(self):
        response = create_post_request(
            self.client, self.correct_complete_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feed.objects.filter(
            user__email=self.user_reg_data['email']).count(), 2)
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__content=self.correct_complete_post_data['content']).feed_template.content, self.correct_complete_post_data['content'])
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__image__icontains='test').feed_template.feed_type, 'add_new_photo')
        self.assertEqual(Feed.objects.get(
            user__email=self.user_reg_data['email'], feed_template__content=self.correct_complete_post_data['content']).feed_template.feed_type, 'add_new_photo')

    def test_get_current_user_posts(self):
        response = get_post_request(
            self.client
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Feed.objects.filter(
            user__email=self.user_reg_data['email']).count(), len(response.data))

    def test_get_other_user_posts(self):
        response = get_post_request(
            self.client, id=2
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Feed.objects.filter(
            user__id=2).count())

    def test_get_other_users_posts(self):
        new_user = self.user_reg_data
        new_user['email'] = 'test2@gmail.com'
        user_register_request(self.client, new_user)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=new_user['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)
        response = get_post_request(
            self.client, id=1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Feed.objects.filter(
            user__id=1).count())


class TestUserProfileUpdate(APITestCase):
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }

    correct_user_update_data = {
        "email": "test123@gmail.com",
        "first_name": "dummy",
        "last_name": "user",
        "profile": {
            "bio": "updating my bio",
            "work": "as",
            "education": "xyz",
            "hometown": "lahore",
            "relationship_status": "Committed"
        }
    }

    incorrect_user_update_data = {
        'email': 'test123@gmail.com',
        'first_name': 'dummy',
        'last_name': 'user',
        'profile': {
            'birthday': '123'
        }
    }

    def setUp(self):

        # Normal user
        user_register_request(self.client, self.user_reg_data)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=self.user_reg_data['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

    def update_user_request(self, data):
        url = reverse('api:update_profile')
        return self.client.patch(url, data, format='json')

    def test_correct_user_profile_update(self):
        response = self.update_user_request(self.correct_user_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'],
                         self.correct_user_update_data['email'])
        self.assertEqual(response.data['first_name'],
                         self.correct_user_update_data['first_name'])
        self.assertEqual(response.data['last_name'],
                         self.correct_user_update_data['last_name'])
        self.assertEqual(response.data['profile']['bio'],
                         self.correct_user_update_data['profile']['bio'])
        self.assertEqual(response.data['profile']['hometown'],
                         self.correct_user_update_data['profile']['hometown'])
        self.assertEqual(response.data['profile']['education'],
                         self.correct_user_update_data['profile']['education'])
        self.assertEqual(response.data['profile']['work'],
                         self.correct_user_update_data['profile']['work'])
        self.assertEqual(response.data['profile']['relationship_status'],
                         self.correct_user_update_data['profile']['relationship_status'])

    def test_incorrect_user_profile_update(self):
        response = self.update_user_request(self.incorrect_user_update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserSearch(APITestCase):
    user_reg_data = {
        'email': 'testuser@gmail.com',
        'password': 'cnc4312056',
        'confirm_password': 'cnc4312056',
        'first_name': 'Awais',
        'last_name': 'Ahmad',
        'gender': 'Male',
        'birthday': '2007-12-1'
    }
    correct_user_update_data = {
        "profile": {
            "work": "as",
            "education": "xyz",
            "hometown": "lahore",
            "relationship_status": "Committed"
        }
    }

    correct_search_query = {
        'search': 'Awa',
        'profile__hometown': 'lahore',
        'profile__education': 'xyz',
        'profile__relationship_status': 'Committed'
    }
    incorrect_search_query = {
        'search': 'Awa',
        'profile__hometown': 'lahore',
        'profile__education': 'xyz',
        'profile__relationship_status': 'committed'
    }

    def setUp(self):

        # Normal user
        user_register_request(self.client, self.user_reg_data)

        self.correct_token, _ = Token.objects.get_or_create(
            user__email=self.user_reg_data['email'])

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

    def update_user_request(self, data):
        url = reverse('api:update_profile')
        return self.client.patch(url, data, format='json')

    def user_search_request(self, search_args):
        url = reverse('api:search')
        url = f'{url}?{urlencode(search_args)}'
        return self.client.get(url)

    def test_correct_same_user_search(self):
        self.update_user_request(self.correct_user_update_data)
        response = self.user_search_request(self.correct_search_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data)), 0)

    def test_incorrect_same_user_search(self):
        response = self.user_search_request(self.incorrect_search_query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_user_search(self):
        self.update_user_request(self.correct_user_update_data)
        new_user = self.user_reg_data
        new_user['email'] = 'test2@gmail.com'
        user_register_request(self.client, new_user)
        self.correct_token, _ = Token.objects.get_or_create(
            user__email=new_user['email'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.correct_token.key)

        response = self.user_search_request(self.correct_search_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data)), 1)
