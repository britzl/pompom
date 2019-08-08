#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/android/gms/play-services-games/17.0.0/play-services-games-17.0.0.pom --pom https://maven.google.com/com/google/android/gms/play-services-drive/16.0.0/play-services-drive-16.0.0.pom --pom https://dl.google.com/dl/android/maven2/com/google/android/gms/play-services-auth/16.0.0/play-services-auth-16.0.0.pom --out gpgs poms
python pompom.py --out gpgs --exclude exceptions/defold.json -apv 28 deps
