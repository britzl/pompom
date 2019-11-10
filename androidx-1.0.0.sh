#!/usr/bin/env bash

python pompom.py \
	--pom https://maven.google.com/androidx/appcompat/appcompat/1.0.0/appcompat-1.0.0.pom \
	--out androidx-1.0.0 poms

python pompom.py --out androidx-1.0.0 -apv 28 deps
