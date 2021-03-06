import unittest

from rx.observable import Observable
from rx.testing import TestScheduler, ReactiveTest
from rx.disposables import Disposable, SerialDisposable

on_next = ReactiveTest.on_next
on_completed = ReactiveTest.on_completed
on_error = ReactiveTest.on_error
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created

class TestTakeLast(unittest.TestCase):
    def test_takelast_zero1(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(
            on_next(210, 1),
            on_next(220, 2),
            on_completed(230))

        def create():
            return xs.take_last_with_time(0, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_completed(230))
        xs.subscriptions.assert_equal(subscribe(200, 230))

    def test_takelast_zero2(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(220, 2), on_next(230, 3), on_completed(230))

        def create():
            return xs.take_last_with_time(0, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_completed(230))
        xs.subscriptions.assert_equal(subscribe(200, 230))

    def test_takelast_some1(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(220, 2), on_next(230, 3), on_completed(240))

        def create():
            return xs.take_last_with_time(25, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_next(240, 2), on_next(240, 3), on_completed(240))
        xs.subscriptions.assert_equal(subscribe(200, 240))

    def test_takelast_some2(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(220, 2), on_next(230, 3), on_completed(300))

        def create():
            return xs.take_last_with_time(25, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_completed(300))
        xs.subscriptions.assert_equal(subscribe(200, 300))

    def test_takelast_some3(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(220, 2), on_next(230, 3), on_next(240, 4), on_next(250, 5), on_next(260, 6), on_next(270, 7), on_next(280, 8), on_next(290, 9), on_completed(300))

        def create():
            return xs.take_last_with_time(45, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_next(300, 6), on_next(300, 7), on_next(300, 8), on_next(300, 9), on_completed(300))
        xs.subscriptions.assert_equal(subscribe(200, 300))

    def test_takelast_some4(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(240, 2), on_next(250, 3), on_next(280, 4), on_next(290, 5), on_next(300, 6), on_completed(350))

        def create():
            return xs.take_last_with_time(25, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_completed(350))
        xs.subscriptions.assert_equal(subscribe(200, 350))

    def test_takelast_all(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(210, 1), on_next(220, 2), on_completed(230))

        def create():
            return xs.take_last_with_time(50, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_next(230, 1), on_next(230, 2), on_completed(230))
        xs.subscriptions.assert_equal(subscribe(200, 230))

    def test_takelast_error(self):
        ex = 'ex'
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_error(210, ex))

        def create():
            return xs.take_last_with_time(50, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal(on_error(210, ex))
        xs.subscriptions.assert_equal(subscribe(200, 210))

    def test_takelast_never(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable()

        def create():
            return xs.take_last_with_time(50, scheduler)

        res = scheduler.start(create)

        res.messages.assert_equal()
        xs.subscriptions.assert_equal(subscribe(200, 1000))

