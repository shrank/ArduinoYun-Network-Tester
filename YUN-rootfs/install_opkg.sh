#!/bin/sh
TMP=`mktemp -d`
echo $TMP
tar -xzf $1 -C $TMP
tar -xzf $TMP/data.tar.gz -C $2
rm -rf $TMP
