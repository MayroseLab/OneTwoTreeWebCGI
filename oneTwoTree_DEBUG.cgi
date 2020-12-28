#!/usr/bin/perl -w

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use File::Path; 
use File::Slurp;

use lib "../";
use lib "/bioseq/oneTwoTree_DEBUG";
use lib "/bioseq/oneTwoTree_DEBUG/webServer_files";

use oneTwoTree_CONSTS_and_Functions;

# this command limits the size of the uploded file
my $maxMB = 100; 
$CGI::POST_MAX = 1024 * 1000 * $maxMB;

my $safe_filename_characters = "a-zA-Z0-9_.-";
my $jobId 		= $^T;
	
my $curJobdir 		= oneTwoTree_CONSTS_and_Functions::RESULTS_DIR_ABSOLUTE_PATH."/$jobId";
#my $curJobdir 		= oneTwoTree_CONSTS_and_Functions::RESULTS_DIR_ABSOLUTE_PATH.$jobId;
my $log 			= "$curJobdir/".oneTwoTree_CONSTS_and_Functions::LOG_FILE;
my $fnameParamsTxt	= "$curJobdir/".oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT;
my $fnameParamsHtml	= "$curJobdir/".oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_HTML;
my $fnameEmail		= "$curJobdir/".oneTwoTree_CONSTS_and_Functions::FILENAME_EMAIL;
my $errLog 			= "$curJobdir/".oneTwoTree_CONSTS_and_Functions::ERROR_STATUS_LOG_FILE;

my $query = new CGI;

# getting inputs from user
# Global parameters
my $rooted					= $query->param("Outgroup_Flag");
my $MSA_Software			= $query->param("MSA_Software");
my $FilterMSA_Method		= $query->param("FilterMSA_Method");
my $Tree_Method				= $query->param("Tree_Method");
my $OriginJobID 			= $query->param("OriginJobID");
my $rerun 					= ( $OriginJobID eq "None" ? "Off" : "On. Original run ID: $OriginJobID" );

# Local parameters
my $NucleusInclude			= $query->param("NucleusInclude");
$NucleusInclude 			= ( $NucleusInclude eq "on" ? "1" : "0" );

my $MitochondrialInclude	= $query->param("MitochondrialInclude");
$MitochondrialInclude 		= ( $MitochondrialInclude eq "on" ? "1" : "0" );

my $ChloroplastInclude		= $query->param("ChloroplastInclude");
$ChloroplastInclude 		= ( $ChloroplastInclude eq "on" ? "1" : "0" );

my $NucleusConcat			= $query->param("NucleusConcat");
$NucleusConcat 				= ( $NucleusConcat eq "on" ? "1" : "0" );

my $MitochondrialConcat		= $query->param("MitochondrialConcat");
$MitochondrialConcat 		= ( $MitochondrialConcat eq "on" ? "1" : "0" );

my $ChloroplastConcat		= $query->param("ChloroplastConcat");
$ChloroplastConcat 			= ( $ChloroplastConcat eq "on" ? "1" : "0" );

my $clustersOptions 		= "$NucleusInclude $NucleusConcat $MitochondrialInclude $MitochondrialConcat $ChloroplastInclude $ChloroplastConcat";

##my $NodeDateInput			= $query->param("files");
my $fnameNodeDate 			= "$curJobdir/NodeDate.txt";
my $NodeDateInputFile		= $query->param("NodeDateInputFile");
#
&WriteToFile($fnameNodeDate, $NodeDateInputFile);

my $inputFile				= $query->param("inputFile");
my $fnameUserInput 			= "$curJobdir/userInput.txt";
# copy the seq from textarea to file
my $inputText				= $query->param("inputText");

# patch for rerun: always create the file userInput.txt . case user uploads a file: userInput.txt will be overwritten. case rerun: userInput.txt will be empry. 
#if (!($inputText eq ""))
{
	&WriteToFile( $fnameUserInput, $inputText);
}

#Load newick constraint tree to file:
my $fconstraintTreeFile 			= "$curJobdir/ConstraintTree_user.txt";
my $constraintTreeInput				= $query->param("ConstraintNewick");
&WriteToFile( $fconstraintTreeFile, $constraintTreeInput);

my $fconstraintUserIDFile 			= "$curJobdir/ConstraintTaxIdList_user.txt";
my $constraintTaxIDInput				= $query->param("ConstraintTaxaList");
&WriteToFile( $fconstraintUserIDFile, $constraintTaxIDInput);


my $email_to_address		= $query->param("inputEmail");
my $jobTitle				= $query->param("jobTitle");
my $date					= $query->param("date");

=pod
my $clustersOptions			= "on";
$clustersOptions 			= ( $clustersOptions eq "on" ? "1" : "0" );
# if cluster options checkbox is checked, get val of 6 other checboxes as 1/0 and add to clustersOptions to be added to cmd later
if ($clustersOptions eq "1") 
{
	my $NucleusInclude			= $query->param("NucleusInclude");
	$NucleusInclude 			= ( $NucleusInclude eq "on" ? "1" : "0" );

	my $MitochondrialInclude	= $query->param("MitochondrialInclude");
	$MitochondrialInclude 		= ( $MitochondrialInclude eq "on" ? "1" : "0" );

	my $ChloroplastInclude		= $query->param("ChloroplastInclude");
	$ChloroplastInclude 		= ( $ChloroplastInclude eq "on" ? "1" : "0" );

	my $NucleusConcat			= $query->param("NucleusConcat");
	$NucleusConcat 			= ( $NucleusConcat eq "on" ? "1" : "0" );

	my $MitochondrialConcat	= $query->param("MitochondrialConcat");
	$MitochondrialConcat 		= ( $MitochondrialConcat eq "on" ? "1" : "0" );

	my $ChloroplastConcat		= $query->param("ChloroplastConcat");
	$ChloroplastConcat 		= ( $ChloroplastConcat eq "on" ? "1" : "0" );

	$clustersOptions .=	" $NucleusInclude $NucleusConcat $MitochondrialInclude $MitochondrialConcat $ChloroplastInclude $ChloroplastConcat";
}
=cut

=pod

# these will be displayed on results.html:
&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Submitted at:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$date."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Job title:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$jobTitle."&nbsp</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Outgroup selection:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$rooted."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">MSA software:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$MSA_Software."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">MSA filter:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$FilterMSA_Method."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Phylogenetic tree method:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$Tree_Method."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Rerun:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$rerun."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

&WriteToFile( $fnameParamsHtml, "<div class=\".row\">");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-3 col-lg-3 params\">Email:</div>");
&WriteToFile( $fnameParamsHtml, "<div class=\"col-md-9 col-lg-9 params\">".$email_to_address."</div><br>");
&WriteToFile( $fnameParamsHtml, "</div>");

=cut



#&WriteToFile( $fnameParamsHtml, "<h4>Job title: <i>".$jobTitle."</i></h4><h4>Rooted: <i>".$rooted."</i></h4><h4>MSA software: <i>".$MSA_Software."</i></h4><h4>MSA Filter: <i>".$FilterMSA_Method."</i></h4><h4>Phylogenetic Tree Method: <i>".$Tree_Method."</i></h4><h4>Rerun: <i>".$rerun."</i></h4><h4>Email: <i>".$email_to_address."</i></h4>");
&WriteToFile( $fnameEmail, $email_to_address); # to be read by result cgi once run ends

# print all params to params.txt file
my @names = $query->param;
foreach my $name ( @names ) 
{
	# dont print field inputText to params.txt
	if ($name eq "inputText")
	{
		next;
	}
	WriteToFile($fnameParamsTxt, $name . ":" . $query->param($name));
}

# creating cur job directory
mkpath($curJobdir);

#if ( !$inputFile )
#{
#	print $query->header ( );
#	print "There was a problem uploading your structure zip (try a smaller file).";
#	exit;
#} 

# checking filename for invalid characters
if ($inputFile)
{
	my ( $name, $path, $extension ) = fileparse ( $inputFile, '\..*' );
	$inputFile = $name . $extension;
	$inputFile =~ tr/ /_/;
	$inputFile =~ s/[^$safe_filename_characters]//g;

	if ( $inputFile =~ /^([$safe_filename_characters]+)$/ )
	{
		$inputFile = $1;
	}
	else
	{
		die "Filename contains invalid characters";
	}
	
	# uploading file to job directory
	my $upload_filehandle = $query->upload("inputFile");
	my $serverLocation = "$curJobdir/$inputFile";
	open ( UPLOADFILE, ">$serverLocation" ) or die "$!";
	binmode UPLOADFILE;

	while ( <$upload_filehandle> )
	{
		print UPLOADFILE;

	}

	close UPLOADFILE;
	rename $serverLocation, $fnameUserInput;
}


# building perl script command
my $serverName 		= oneTwoTree_CONSTS_and_Functions::SERVER_NAME;
my $pythonModule	= oneTwoTree_CONSTS_and_Functions::PYTHON_MODULE_TO_LOAD;
my $perlModule		= oneTwoTree_CONSTS_and_Functions::PERL_MODULE_TO_LOAD;



my $pid = fork();
if( $pid == 0 )
{
	# this code runs async
	open STDIN,  '<', '/dev/null';
    #open STDOUT, '>', $validationLog; # point to /dev/null or to a log file
    #open STDERR, '>&STDOUT';
    
	# logging user request
	use POSIX qw(strftime);
	my $date = strftime('%F %H:%M:%S', localtime);
	my $logPath = oneTwoTree_CONSTS_and_Functions::LOG_DIR_ABSOLUTE_PATH; 
	$logPath = $logPath.oneTwoTree_CONSTS_and_Functions::MAIN_PIPELINE_LOG;
	&WriteToFile( $logPath, "$email_to_address\t$date\t$jobId");

    #creating shell script file for lecs2
	my $qsub_script = "$curJobdir/qsub.sh";
	open (QSUB_SH,">$qsub_script");
	  
	print QSUB_SH "#!/bin/tcsh\n";
	print QSUB_SH '#$ -N ', "$serverName"."_$jobId\n";
	print QSUB_SH '#$ -S /bin/tcsh', "\n";
	print QSUB_SH '#$ -cwd', "\n";
	#print QSUB_SH '#$ -l bioseq', "\n"; # original
	#print QSUB_SH '#$ -q bioseq.q', "\n"; # what Mike said to change
	#print QSUB_SH '#$ -q 12tree.q', "\n"; # dedicated queue for oneTwoTree on jekyl
	print QSUB_SH '#$ -l 12tree', "\n"; # dedicated queue for oneTwoTree on jekyl
	#print QSUB_SH '#$ -i itaym', "\n"; 
	print QSUB_SH '#$ -e ', "$curJobdir", '/$JOB_NAME.$JOB_ID.ER', "\n";
	print QSUB_SH '#$ -o ', "$curJobdir", '/$JOB_NAME.$JOB_ID.OU', "\n";
	print QSUB_SH "cd $curJobdir\n";
	print QSUB_SH "module load $pythonModule\n";
	#print QSUB_SH "module load $perlModule\n";
	print QSUB_SH "hostname;\n"; # for debug - to know which node ran the job		

	my $cmd .= "python /bioseq/oneTwoTree_DEBUG/OneTwoTree.py $fnameUserInput $curJobdir $jobId;";
	print QSUB_SH "$cmd\n";
	
	# this is not done here, but by OTT at end of run
	#my $cmdEmail = "perl /bioseq/$serverName/sendLastEmail.pl --toEmail $email_to_address --id $jobId;";
	#print QSUB_SH "$cmdEmail\n";
	
	close (QSUB_SH);
    
	my $qsubCmd =  'ssh bioseq@jekyl qsub '."$qsub_script";
	#my $qsubCmd =  'ssh bioseq@lecs2 qsub '."$qsub_script";
	
	my 	$qsubJobNum = "NONE";
	my $ans = `$qsubCmd`;
	if ($ans =~ /(\d+)/)
	{
		$qsubJobNum = $1;
	}
	
	write_file("$curJobdir/".oneTwoTree_CONSTS_and_Functions::QSUB_JOB_NUM_FILE, $qsubJobNum);
	&WriteToFileWithTimeStamp($log, "Job $jobId was submitted to queue.");
	
	exit 0;
}


# redirecting client to results page
my $redirectedURL = oneTwoTree_CONSTS_and_Functions::RESULTS_PAGE_URL."?jobId=";
$redirectedURL = $redirectedURL.$jobId;
$redirectedURL .= "&jobTitle=".$jobTitle;

print $query->redirect($redirectedURL);
