#!/usr/bin/env bash
if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

if [ ! -d "export/firebase_core-16.0.7" ]; then
	sh firebase_core-16.0.7.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/firebase/firebase-analytics/16.0.5/firebase-analytics-16.0.5.pom \
	--out firebase_analytics-16.0.5 poms

python pompom.py \
	--exclude export/gps-base-16.0.1/dependencies.json \
	--exclude export/firebase_core-16.0.7/dependencies.json \
	--out firebase_analytics-16.0.5 \
	-apv 28 deps
