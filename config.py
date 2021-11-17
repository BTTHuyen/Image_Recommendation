#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "b69a4680-b985-425c-8446-24b0b778efdc")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "rccms2021")
