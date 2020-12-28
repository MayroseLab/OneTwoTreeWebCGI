#!/usr/bin/perl -w

use strict;
use warnings;
use diagnostics;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use File::Path; 
use File::Slurp;
use File::Copy;

use lib "../";
use lib "/bioseq/oneTwoTree";
use lib "/bioseq/oneTwoTree/webServer_files";

use oneTwoTree_CONSTS_and_Functions;
use Archive::Zip;
use CGI qw(:standard);

my $query = new CGI;

# getting inputs from user form
my $jobId 			= $query->param('jobId');
my $clusterId 		= $query->param('clusterId');
my $userSelected	= $query->param("dropdown");

# construct file names
my $pathAligned		= "oneTwoTree_results/$jobId/concat/$clusterId/seqs-organism-concat.fasta";
my $pathNotAligned	= "oneTwoTree_results/$jobId/$clusterId/seqs-no-multiple-accessions.fasta";

my $fnameAligned	= "oneTwoTree.$jobId.$clusterId.aligned.seqs-organism-concat.fasta";
my $fnameNotAligned	= "oneTwoTree.$jobId.$clusterId.notAligned.seqs-no-multiple-accessions.fasta";
my $fnameZip 		= "oneTwoTree.$jobId.$clusterId.zip";	

# zip
my $zip = Archive::Zip->new();

if ($userSelected eq "aligned")
{
	$zip->addFile($pathAligned,$fnameAligned);
}

if ($userSelected eq "notAligned")
{
	$zip->addFile($pathNotAligned,$fnameNotAligned);	
}

if ($userSelected eq "both")
{
	$zip->addFile($pathAligned,$fnameAligned);	
	$zip->addFile($pathNotAligned,$fnameNotAligned);
}

# push to download
#print header(-type=>'application/zip',-attachment=>'OneTwoTreeDownload.zip');
print header(-type=>'application/zip',-attachment=>$fnameZip);
binmode(STDOUT);
$zip->writeToFileHandle(*STDOUT);