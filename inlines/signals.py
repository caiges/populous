"""
Signals for the inlines app.
"""

from django.dispatch import Signal

inline_will_be_registered = Signal(providing_args=('inline'))

inline_was_registered = Signal(providing_args=('inline'))