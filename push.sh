#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-messaging/17.3.4/firebase-messaging-17.3.4.pom --pom https://maven.google.com/com/google/firebase/firebase-core/16.0.7/firebase-core-16.0.7.pom --out push poms
python pompom.py --out push --exclude exceptions.json -apv 28 deps
