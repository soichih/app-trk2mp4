#!/bin/bash

set -e
set -x

freesurfer=$(jq -r .freesurfer config.json)

mris_convert $freesurfer/surf/lh.orig.nofix ./lh.stl
mris_convert $freesurfer/surf/rh.orig.nofix ./rh.stl

ls lh.stl
