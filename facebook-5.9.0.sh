#!/usr/bin/env bash
if [ ! -d "export/gps-base-16.0.1" ]; then
	sh gps-base-16.0.1.sh
fi

python pompom.py \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-core/5.9.0/facebook-core-5.9.0.pom \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-login/5.9.0/facebook-login-5.9.0.pom \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-share/5.9.0/facebook-share-5.9.0.pom \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-applinks/5.9.0/facebook-applinks-5.9.0.pom \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-places/5.9.0/facebook-places-5.9.0.pom \
	--pom http://central.maven.org/maven2/com/facebook/android/facebook-messenger/5.9.0/facebook-messenger-5.9.0.pom \
	--out facebook-5.9.0 poms

python pompom.py \
	--exclude export/gps-base-16.0.1/dependencies.json \
	--out facebook-5.9.0 \
	-apv 28 deps
