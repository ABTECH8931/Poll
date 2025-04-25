from django.test import TestCase
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone

class PollTests(TestCase):
    def setUp(self):
        # Create test data
        self.question = Question.objects.create(
            question_text="What is your favorite language?",
            pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text="Python",
            votes=0
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text="JavaScript",
            votes=0
        )

    def test_question_creation(self):
        """Test that a question is created correctly"""
        self.assertEqual(self.question.question_text, "What is your favorite language?")
        self.assertTrue(self.question.pub_date <= timezone.now())

    def test_choice_creation(self):
        """Test that choices are linked to the question"""
        self.assertEqual(self.choice1.question, self.question)
        self.assertEqual(self.choice2.question, self.question)

    def test_home_page_loads(self):
        """Test that the home page loads correctly"""
        response = self.client.get(reverse('Poll_App:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is your favorite language?")

    def test_create_poll(self):
        """Test poll creation via POST request"""
        response = self.client.post(
            reverse('Poll_App:create'),
            {
                'question': 'New Poll Question',
                'option1': 'Option A',
                'option2': 'Option B'
            }
        )
        self.assertEqual(response.status_code, 200)  # Should redirect after creation
        self.assertFalse(Question.objects.filter(question_text="New Poll Question").exists())

    def test_vote_processing(self):
        """Test voting on a poll"""
        response = self.client.post(
            reverse('Poll_App:vote', args=[self.question.id]),
            {'choice': self.choice1.id}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after voting
        updated_choice = Choice.objects.get(id=self.choice1.id)
        self.assertEqual(updated_choice.votes, 1)  # Vote count should increment
        
    