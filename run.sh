#!/bin/sh -e
wget https://lichphatsong.xyz/schedule/epg.xml.gz -O epg.xml.gz
wget https://playlist.vthanhtivi.pw -O tv.data
curl http://m3u.in/HVdAHQEO --output coocaa.m3u8
sed -i 's/append/default/g' coocaa.m3u8
curl -L http://playlist.vthanhtivi.pw/ --output vthanh.m3u8
sed -i 's/append/default/g' vthanh.m3u8
