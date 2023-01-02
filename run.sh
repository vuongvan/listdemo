#!/bin/sh -e
wget -O coocaa.m3u8 http://m3u.in/HVdAHQEO
sed -i 's/append/default/g' coocaa.m3u8
curl -L http://playlist.vthanhtivi.pw/ --output vthanh.m3u8
sed -i 's/append/default/g' vthanh.m3u8
