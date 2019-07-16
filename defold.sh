#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/android/gms/play-services-ads/17.2.1/play-services-ads-17.2.1.pom --out defold poms
python pompom.py --out defold -apv 28 deps
