#!/bin/sh -e
curl "https://dl.dropboxusercontent.com/s/fhon6tzc3e20tis/%20%C3ƒ%EF%BF%BD%C3‚%C2%A3%C3ƒ%C2%AF%C3‚%C2%BF%C3‚%C2%BD%C3ƒ%EF%BF%BD%C3‚%C2%A4" --output coocaa.m3u8
sed -i 's/append/default/g' coocaa.m3u8
curl -L http://playlist.vthanhtivi.pw/ --output vthanh.m3u8
sed -i 's/append/default/g' vthanh.m3u8
