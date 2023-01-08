#!/bin/sh -e
curl https://trada.info/epg.xml --output epg.xml
gzip epg.xml
