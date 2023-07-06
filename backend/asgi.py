#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend import __version__
from backend.apps.main import get_app

app = get_app(__version__)
