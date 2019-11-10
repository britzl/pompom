#!/usr/bin/env bash
# https://developers.google.com/android/guides/setup

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-base/16.0.1/play-services-base-16.0.1.pom \
	--out gps-base-16.0.1 poms

python pompom.py \
	--exclude export/support-v4-27.0.2/dependencies.json \
	--out gps-base-16.0.1 \
	-apv 28 deps
