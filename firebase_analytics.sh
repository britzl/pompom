#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-core/16.0.5/firebase-core-16.0.5.pom --pom https://maven.google.com/com/google/firebase/firebase-analytics/16.0.5/firebase-analytics-16.0.5.pom --pom https://maven.google.com/com/google/android/gms/play-services-base/16.0.1/play-services-base-16.0.1.pom --out firebase_analytics poms
python pompom.py --out firebase_analytics deps
