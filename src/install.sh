#!/bin/sh

basedir=/

mkdir -p ${basedir}tester/
rm -r ${basedir}tester/*
cp -r *.py ${basedir}tester/
mkdir -p ${basedir}tester/NetworkTester
cp -r NetworkTester/* ${basedir}tester/NetworkTester
chmod a+x ${basedir}tester/daemon.py
cp NetworkTester.init ${basedir}etc/init.d/NetworkTester
chmod a+x ${basedir}etc/init.d/NetworkTester
/etc/init.d/NetworkTester enable

