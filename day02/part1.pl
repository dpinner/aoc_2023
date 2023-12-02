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
	my ($id) = /(\d+):/;
	my ($reds) = max(/ (\d+) red/g) <= 12;
	my ($blues) = max(/ (\d+) blue/g) <= 14;
	my ($greens) = max(/ (\d+) green/g) <= 13;
	$sum += $id if ($reds && $blues && $greens);
}
print "$sum\n";