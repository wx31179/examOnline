#!/usr/bin/env python
# -*- coding: utf-8 -*-
import selenium

r = requests.get(
    'https://support.hp.com/us-en/drivers/printers')
data = r.text

print(data)