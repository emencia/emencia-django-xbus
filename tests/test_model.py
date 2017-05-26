# -*- coding: utf-8 -*-
import uuid
from mock import patch, MagicMock

from django.test import TestCase, TransactionTestCase
from django.core.management import call_command

from xbus.models import Envelope

from tests.models import (
    EmitterWithoutMethod, SimpleEmitter, EmitterWithExitCondition, Consumer)


class TestEmitterWithoutMethod(TestCase):
    """To test emitter without method"""
    def test_without_method(self):
        with self.assertRaises(NotImplementedError):
            EmitterWithoutMethod.objects.create(name='Try')


class TestSimpleEmitter(TransactionTestCase):
    """To test simple emitter"""

    @patch('xbus.api.new_connection_to_xbus')
    def test_simple_emitter(self, mock_xbus):
        mock_xbus.return_value = (MagicMock(
            end_event=lambda x, y, z: (True, '')), uuid.uuid4())
        count = Envelope.objects.count()
        emitter = SimpleEmitter.objects.create(name='Try')

        call_command('xbus_queue')

        envelope = Envelope.objects.last()
        refresh_count = Envelope.objects.count()

        self.assertEqual(emitter.name, 'Try')
        self.assertEqual(envelope.state, 'error')
        self.assertEqual(refresh_count, count + 1)


class TestEmitterWithExitCondition(TestCase):
    """To test emitter with exit condition"""
    def test_with_exit_condition(self):
        count = Envelope.objects.count()
        emitter = EmitterWithExitCondition.objects.create(name='Try')

        call_command('xbus_queue')

        refresh_count = Envelope.objects.count()

        self.assertEqual(emitter.name, 'Try')
        self.assertEqual(refresh_count, count)


class TestConsumer(TestCase):
    """To test consumer"""
    def test_consumer(self):
        consumer = Consumer.objects.create(name='Try')
        self.assertEqual(consumer.name, 'Try')
