#!/usr/bin/perl

my $adj=0.0;
if( $#ARGV >= 0 ) {
    $adj = $ARGV[0];
}

my $orig = -1.0;
while(<STDIN>) {
    if( /^([0-9.]+)\s+([0-9.]+)(.*)/ ) {
	$t = $1;
	$v = $2;
	$etc = $3;
	if( $orig < 0.0 ) {
	    $orig = $t;
	    $t = 0.0;
	} else {
	    $t = $t - $orig;
	}
	# adjusting
	$t = $t - $adj;
	if($t>0.0) {
	    print "$t $v $etc\n";
	}
    }
}

printf "# TIME_ZERO=%lf\n",   ($orig + $adj);
printf "# TIME_1ST_DATA=%lf\n", $orig;
printf "# TIME_PREP=%lf\n", $adj;

