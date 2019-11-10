#!/usr/bin/env bash
# https://developers.google.com/android/guides/setup
if [ ! -d "export/androidx-1.0.0" ]; then
	sh androidx-1.0.0.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-base/17.0.0/play-services-base-17.0.0.pom \
	--out gps-base-17.0.0 poms

python pompom.py \
	--exclude export/androidx-1.0.0/dependencies.json \
	--out gps-base-17.0.0 \
	-apv 28 deps
