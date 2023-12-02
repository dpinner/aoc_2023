#!/usr/bin/perl

sub max {
    my $max = shift;
    foreach (@_) {
        $max = $_ if $_ > $max;
    }
    return $max;
}

my ($sum) = 0;
while(<>) {
	my ($reds) = max(/ (\d+) red/g);
	my ($blues) = max(/ (\d+) blue/g);
	my ($greens) = max(/ (\d+) green/g);
	$sum += ($reds * $blues * $greens);
}
print "$sum\n";