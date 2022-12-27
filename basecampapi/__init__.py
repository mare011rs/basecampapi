import requests

import os
import json
from mimetypes import MimeTypes

from .basecamp import Basecamp, Authorization
from .endpoints.camprife import Campfire
from .endpoints.messageboard import MessageBoard