#!/usr/bin/env bash
if [ ! -d "export/support-v4-27.0.2" ]; then
	sh support-v4-27.0.2.sh
fi

if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-ads/17.2.1/play-services-ads-17.2.1.pom \
	--out gps-ads-17.2.1 poms

python pompom.py \
	--exclude export/gps-base-16.0.1/dependencies.json \
	--exclude export/support-v4-27.0.2/dependencies.json \
	--out gps-ads-17.2.1 \
	-apv 28 deps
