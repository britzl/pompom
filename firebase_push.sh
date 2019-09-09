#!/usr/bin/env bash
python pompom.py --pom https://maven.google.com/com/google/firebase/firebase-messaging/17.3.4/firebase-messaging-17.3.4.pom --out firebase_push poms
python pompom.py --out firebase_push --exclude exceptions/gpg.json --exclude exceptions/firebase_core.json -apv 28 deps
