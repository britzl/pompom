#!/usr/bin/env bash
if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

if [ ! -d "export/firebase_core-16.0.7" ]; then
	sh firebase_core-16.0.7.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/firebase/firebase-messaging/17.3.4/firebase-messaging-17.3.4.pom \
	--out firebase_push-17.3.4 poms

python pompom.py \
	--exclude export/gps-base-16.0.1/dependencies.json \
	--exclude export/firebase_core-16.0.7/dependencies.json \
	--out firebase_push-17.3.4 \
	-apv 28 deps
