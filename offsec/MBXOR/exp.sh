#!/bin/sh

xortools -x ciphertext.txt -b

grep -R "flag" ./xortools_output
