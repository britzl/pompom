#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-core/16.0.5/firebase-core-16.0.5.pom --out firebase_core poms
python pompom.py --out firebase_core --exclude exceptions/defold.json -apv 28 deps
