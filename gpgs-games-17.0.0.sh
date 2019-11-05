#!/usr/bin/env bash
if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

python pompom.py \
	--pom https://maven.google.com/com/google/android/gms/play-services-games/17.0.0/play-services-games-17.0.0.pom \
	--pom https://maven.google.com/com/google/android/gms/play-services-drive/16.0.0/play-services-drive-16.0.0.pom \
	--pom https://maven.google.com/com/google/android/gms/play-services-auth/16.0.0/play-services-auth-16.0.0.pom \
	--out gpgs-games-17.0.0 poms

python pompom.py --out gpgs-games-17.0.0 --exclude export/gps-base-16.0.1/dependencies.json -apv 28 deps
