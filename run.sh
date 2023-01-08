#!/bin/sh -e
curl http://m3u.in/HVdAHQEO --output coocaa.m3u8
sed -i 's/append/default/g' coocaa.m3u8
curl https://trada.info/epg.xml --output epg.xml
gzip epg.xml
curl -L http://playlist.vthanhtivi.pw/ --output vthanh.m3u8
sed -i 's/append/default/g' vthanh.m3u8
