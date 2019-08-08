#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-analytics/16.0.5/firebase-analytics-16.4.0.pom --out firebase_analytics poms
python pompom.py --out firebase_analytics --exclude exceptions/defold.json --exclude exceptions/firebase_core.json -apv 28 deps
