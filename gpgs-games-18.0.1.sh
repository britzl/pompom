#!/usr/bin/env bash
if [ ! -d "export/gps-base-17.0.0" ]; then
	sh gps-base-17.0.0.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-games/18.0.1/play-services-games-18.0.1.pom \
	--pom https://maven.google.com/com/google/android/gms/play-services-drive/17.0.0/play-services-drive-17.0.0.pom \
	--pom https://maven.google.com/com/google/android/gms/play-services-auth/17.0.0/play-services-auth-17.0.0.pom \
	--out gpgs-games-18.0.1 poms

python pompom.py --out gpgs-games-18.0.1 --exclude export/gps-base-17.0.0/dependencies.json -apv 28 deps
