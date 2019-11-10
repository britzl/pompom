#!/usr/bin/env bash

python pompom.py \
	--pom https://maven.google.com/com/android/support/support-v4/27.0.2/support-v4-27.0.2.pom \
	--pom https://maven.google.com/com/android/support/customtabs/27.0.2/customtabs-27.0.2.pom \
	--out support-v4-27.0.2 poms

python pompom.py --out support-v4-27.0.2 -apv 28 deps
