#!/usr/bin/env bash
python pompom.py --pom https://dl.google.com/dl/android/maven2/com/google/android/gms/play-services-auth/16.0.0/play-services-auth-16.0.0.pom --pom https://maven.google.com/com/google/android/gms/play-services-ads/17.2.0/play-services-ads-17.2.0.pom --out gpgs poms
python pompom.py --out gpgs -apv 28 deps
