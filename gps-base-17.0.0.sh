#!/usr/bin/env bash
# https://developers.google.com/android/guides/setup

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-base/17.0.0/play-services-base-17.0.0.pom \
	--pom https://maven.google.com/com/google/android/gms/play-services-ads-identifier/17.0.0/play-services-ads-identifier-17.0.0.pom \
	--pom https://maven.google.com/android/arch/core/common/1.1.1/common-1.1.1.pom \
	--out gps-base-17.0.0 poms

python pompom.py --out gps-base-17.0.0 -apv 28 deps
