#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-core/16.0.7/firebase-core-16.0.7.pom --pom https://maven.google.com/com/google/android/gms/play-services-measurement-sdk-api/16.3.0/play-services-measurement-sdk-api-16.3.0.pom --out firebase_core poms
python pompom.py --out firebase_core --exclude exceptions/defold.json -apv 28 deps
