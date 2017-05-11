from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Listing


def create_listing(title: str, description: str, creator: str = 'test@listings.com', date: timezone = timezone.now()):
    Listing.objects.create(title=title,
                           description=description,
                           creator_email=creator,
                           last_edit_date=date)


class IndexViewTests(TestCase):
    def setUp(self):
        for i in range(3):
            # create 3 listings, with 3 being the most recently edited & 1 being the last edited
            create_listing('test listing ' + str(i), 'description ' + str(i),
                           date=(timezone.now() - timezone.timedelta(days=2 - i)))

    def test_index_view_order(self):
        response = self.client.get('/listings/')
        listings = response.context['latest_listings']
        for i in range(3):
            # order by same operation (2-i) to ensure we're testing the correct order
            self.assertEqual('test listing ' + str(2 - i), listings[i].title,
                             'Incorrect index display order:\n' + str(listings))


class NewViewTests(TestCase):
    def setUp(self):
        self.client.post('/listings/new/',
                         {'title': 'new title',
                          'description': 'new description',
                          'creator email': 'newtest@listings.com',
                          'posted': True})

    def test_creation_data(self):
        listing = Listing.objects.get(pk=1)

        # test title, description, creator email
        message = 'Wrong {attribute}. Expected "{expected_val}", found "{val}"'
        self.assertEqual(listing.title, 'new title',
                         message.format(attribute='title', expected_val='new title', val=listing.title))
        self.assertEqual(listing.description, 'new description',
                         message.format(attribute='description', expected_val='new description',
                                        val=listing.description))
        self.assertEqual(listing.creator_email, 'newtest@listings.com',
                         message.format(attribute='creator email', expected_val='newtest@listings.com',
                                        val=listing.creator_email))

    def test_new_token_works(self):
        token = Listing.objects.get(pk=1).edit_token
        response = self.client.get(reverse('list_app:edit', args=(token,)))
        self.assertEqual(response.status_code, 200,
                         'Edit token {} returned with status code {}'.format(token, response.status_code))


class DetailViewTest(TestCase):
    def setUp(self):
        create_listing('listing title', 'lorem ipsum')

    def test_detail_data(self):
        response = self.client.get('/listings/1/')
        l = response.context['listing']
        title, description = l.title, l.description
        self.assertEqual(title, 'listing title', 'Wrong title. Expected "listing title", received {}.'.format(title))
        self.assertEqual(description, 'lorem ipsum',
                         'Wrong description. Expected "lorem ipsum", received {}.'.format(description))
