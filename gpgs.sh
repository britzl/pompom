#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/android/gms/play-services-games/15.0.0/play-services-games-15.0.0.pom --out gpgs poms
python pompom.py --out gpgs -apv 28 deps
