import os
import shutil
from django.core.files import File as django_file
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITransactionTestCase
from rest_framework.authtoken.models import Token

from qfieldcloud.apps.model.models import (
    Project, ProjectCollaborator, File, FileVersion)
from .utils import testdata_path

User = get_user_model()


class PermissionTestCase(APITransactionTestCase):

    def setUp(self):
        # Create a user (owner)
        self.user1 = User.objects.create_user(
            username='user1', password='abc123')
        self.user1.save()
        self.token1 = Token.objects.get_or_create(user=self.user1)[0]

        # Create a second user
        self.user2 = User.objects.create_user(
            username='user2', password='abc123')
        self.user2.save()
        self.token2 = Token.objects.get_or_create(user=self.user2)[0]

        # Create a project
        self.project1 = Project.objects.create(
            name='project1',
            private=True,
            owner=self.user1)
        self.project1.save()

        # Create a collaborator
        self.collaborator1 = ProjectCollaborator.objects.create(
            project=self.project1,
            collaborator=self.user2,
            role=ProjectCollaborator.ROLE_READER)

    def tearDown(self):
        # Remove all projects avoiding bulk delete in order to use
        # the overrided delete() function in the model
        for p in Project.objects.all():
            p.delete()

        User.objects.all().delete()
        # Remove credentials
        self.client.credentials()

    def test_reader_cannot_push(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)

        file_path = testdata_path('file.txt')
        # Push a file
        response = self.client.post(
            '/api/v1/files/{}/file.txt/?client=qgis'.format(self.project1.id),
            {
                "file": open(file_path, 'rb')
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reporter_can_push(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)

        self.collaborator1.role = ProjectCollaborator.ROLE_REPORTER
        self.collaborator1.save()

        file_path = testdata_path('file.txt')
        # Push a file
        response = self.client.post(
            '/api/v1/files/{}/file.txt/?client=qgis'.format(self.project1.id),
            {
                "file": open(file_path, 'rb')
            },
            format='multipart'
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_pull_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

        f = open(testdata_path('file.txt'))
        file_obj = File.objects.create(
            project=self.project1,
            original_path='foo/bar/file.txt')

        FileVersion.objects.create(
            file=file_obj,
            stored_file=django_file(
                f,
                name=os.path.join(
                    'foo/bar',
                    os.path.basename(f.name))))

        # Pull the file
        response = self.client.get(
            '/api/v1/files/{}/foo/bar/file.txt/?client=qgis'.format(self.project1.id))

        self.assertTrue(status.is_success(response.status_code))

        # Remove credentials
        self.client.credentials()

        # Pull the file
        response = self.client.get(
            '/api/v1/files/{}/foo/bar/file.txt/?client=qgis'.format(self.project1.id))
        self.assertFalse(status.is_success(response.status_code))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_project_admin_can_create_collaborator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        self.collaborator1.role = ProjectCollaborator.ROLE_ADMIN
        self.collaborator1.save()

        # Create a user
        user3 = User.objects.create_user(
            username='user3', password='abc123')
        user3.save()

        # Add the user3 as a collaborator
        response = self.client.post(
            '/api/v1/collaborators/{}/'.format(self.project1.id),
            {
                'collaborator': 'user3',
                'role': 'editor',
            }
        )

        self.assertTrue(status.is_success(response.status_code))

    def test_project_editor_cannot_create_collaborator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        self.collaborator1.role = ProjectCollaborator.ROLE_EDITOR
        self.collaborator1.save()

        # Create a user
        user3 = User.objects.create_user(
            username='user3', password='abc123')
        user3.save()

        # Add the user3 as a collaborator
        response = self.client.post(
            '/api/v1/collaborators/{}/'.format(self.project1.id),
            {
                'collaborator': 'user3',
                'role': 'editor',
            }
        )

        self.assertFalse(status.is_success(response.status_code))
        self.assertEqual(response.status_code, 403)

    def test_not_collaborator_cannot_list_collaborators(self):
        # Create a user
        user3 = User.objects.create_user(
            username='user3', password='abc123')
        user3.save()
        token3 = Token.objects.get_or_create(user=user3)[0]

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token3.key)

        # List collaborators
        response = self.client.get(
            '/api/v1/collaborators/{}/'.format(self.project1.id))

        self.assertFalse(status.is_success(response.status_code))
        self.assertEqual(response.status_code, 403)