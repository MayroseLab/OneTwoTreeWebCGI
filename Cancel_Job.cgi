#!/usr/bin/perl -w

use strict;
use warnings;
use diagnostics;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use File::Path; 
use File::Slurp;

use lib "../";
use lib "/bioseq/oneTwoTree";

use oneTwoTree_CONSTS_and_Functions;

my $query = new CGI;

# getting inputs from user form
my $jobId 			= $query->param('jobId');
my $JobNumber 		= $query->param('vLinuxJobNumber');

#system "qdel $JobNumber"; 

