#!/usr/bin/perl

# HEATER.PREP_TIME=0.174395
my $prep = 0.0;
while(<STDIN>) {
    if(/HEATER.PREP_TIME=([0-9.]+)/) {
	$prep = $1;
    }
}

print $prep

# ceiling 
# print int($prep)+1

