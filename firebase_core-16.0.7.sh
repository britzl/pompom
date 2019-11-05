#!/usr/bin/env bash
if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/firebase/firebase-core/16.0.7/firebase-core-16.0.7.pom \
	--out firebase_core-16.0.7 poms

python pompom.py --out firebase_core-16.0.7 --exclude export/gps-base-16.0.1/dependencies.json -apv 28 deps
