#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use YAML::XS 'LoadFile';

my $yaml = LoadFile('wadjet-draft.yml');

print Dumper($yaml);