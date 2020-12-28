#!/usr/bin/perl -w

use strict;
use warnings;
use diagnostics;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use File::Path; 
use File::Slurp;
#use CGI qw(:standard);
use File::Copy qw( copy );

use lib "../";
use lib "/bioseq/oneTwoTree";

use oneTwoTree_CONSTS_and_Functions;
use Archive::Zip;
use CGI qw(:standard);

my $query = new CGI;

# getting inputs from user form
my $jobId 			= $query->param('jobId');
my $clusterId 		= $query->param('clusterId');
my $userSelected	= $query->param("dropdown");


my $pathAligned		= "oneTwoTree_results/$jobId/concat/$clusterId/";
my $pathNotAligned	= "oneTwoTree_results/$jobId/$clusterId/";

my $fnameAligned	= "oneTwoTree.$jobId.$clusterId.aligned.seqs-organism-concat.fasta";
my $fnameNotAligned	= "oneTwoTree.$jobId.$clusterId.notAligned.seqs-no-multiple-accessions.fasta";

my $zip = Archive::Zip->new();

if ($userSelected eq "aligned")
{
	send_file($pathAligned, "seqs-organism-concat.fasta");
}

if ($userSelected eq "notAligned")
{
	send_file($pathNotAligned, "seqs-no-multiple-accessions.fasta");
}

if ($userSelected eq "both")
{
	$zip->addFile($pathAligned,$fnameAligned);	
	$zip->addFile($pathNotAligned,$fnameNotAligned);
	print header(-type=>'application/zip',-attachment=>$fnameZip);
	binmode(STDOUT);
	$zip->writeToFileHandle(*STDOUT);
}



sub send_file {
    my ($dir, $file) = @_;

    my $path = catfile($dir, $file);

    open my $fh, '<:raw', $path
        or die "Cannot open '$path': $!";

    binmode STDOUT, ':raw';
    copy $fh => \*STDOUT, 8_192;
    close $fh
        or die "Cannot close '$path': $!";

    return;
}