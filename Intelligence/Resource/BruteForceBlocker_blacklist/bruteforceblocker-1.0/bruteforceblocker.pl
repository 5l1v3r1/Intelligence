#!/usr/bin/perl -w

# BruteForceBlocker.pl v1.0
#
# If you want to use this script, you will need a File::Tail
# perl extension. Under FreeBSD it is located at
# /usr/ports/devel/p5-File-Tail
#
# you will also need to add a new table to the pf config file
# you can do so by adding lines to the pf.conf similar to these:
#
# table <bruteforce> persist file "/data/sysop/fw/ssh.bruteforce"
# block in log quick inet proto tcp from <bruteforce> to any port ssh
#
# - Daniel Gerzo <danger@rulez.sk>

use strict;
use warnings;
use File::Tail;

my $logfile = '/var/log/auth/bruteforce.log';		# file where this script will log to
my $pidfile = '/var/run/bruteforceblocker.pid';		# process pid file
my $pfctl = '/sbin/pfctl';				# pfctl binary
my $authlog = '/var/log/auth/auth.log';			# sshd log file
my $table = 'bruteforce';				# pf table
my $tablefile = '/data/sysop/fw/ssh.bruteforce';	# file where table persist
my $max_attempts = 3;					# number of max allowed fails
my $timeout = 3600;					# number of seconds after resetting of ip
my %count = ();
my %time = ();						# last modified time

# list of IPs that will never be blocked
my @trusted_IPs = qw(
	127.0.0.1
	10.10.10.1
);

if(-e $pidfile) {
	print "It seems like another bruteforceblocker is already running, I will try to stop it...";
	`kill \`cat $pidfile\``;			# kill old process
	`rm -f $pidfile`;				# remove old pidfile
	print "...done.\n";
}

# Daemonize
if(my $pid = fork) {
	`echo $pid > $pidfile`;				# create pidfile
	exit(0);
} elsif(!defined $pid) {
	 die "Can't fork: $!\n";
} else {

print "BruteForceBlocker was successfuly launched to the background.\n";

# open log for writing and disable caching
open (FILE, ">>$logfile") or die ("Couldn't open $logfile for writing");
select FILE; $| = 1; select STDOUT;

print (FILE "\n------- log started at ", scalar(localtime), " -------\n\n");

my $file = tie *authlog, "File::Tail", (name => $authlog,
				interval => 1,
				maxinterval => 5,
				adjustafter => 300,
				errmode => "return");

# the core process
while (<authlog>) {
	print (FILE "$_");
	
	if(my ($IP) = $_ =~ /.*Failed password.*from ((?:\d{1,3}\.){3}\d{1,3}) port.*/) {
	
		print (FILE "$IP was logged.\n");
		if($time{$IP}) {
			if ($time{$IP} < time - $timeout) {
				delete $count{$IP};
				print (FILE "resetting $IP count, since it wasn't modified for more than $timeout seconds.\n");
			}
		}
		
		$time{$IP} = time;
		$count{$IP}++;
 
		if($count{$IP} == $max_attempts+1) {
			print (FILE "IP $IP reached the maximum number of failed attempts!!!\n");
			if(!grep { /$IP/ } @trusted_IPs) {
				print (FILE "Adding IP to the firewall...\n");
				system("$pfctl -t $table -T add $IP/32") == 0 or die "Couldn't add $IP to firewall";
				system("echo $IP/32 >> $tablefile") == 0 or die "Could't write $IP to ${table}'s table file";
			} else {
				print (FILE "...but it is Trusted IP, so i won't block it!\n");
			}
		}
	}
}

close(FILE);

}
