#!/usr/bin/perl -w

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use JSON;
use File::Slurp;
use List::Util qw(first);
use List::MoreUtils qw(any  first_index);

use lib "/bioseq/oneTwoTree";

#use lib "/bioseq/bioSequence_scripts_and_constants";
use lib "../";
use oneTwoTree_CONSTS_and_Functions;

my $query = new CGI;
my $jobId = $query->param('jobId');

my %jsonData;
$jsonData{'errorOccured'} = 0;
$jsonData{'jobId'} = $jobId;

my $curJobDir = oneTwoTree_CONSTS_and_Functions::RESULTS_LINK."/$jobId";
my $log 	  = "$curJobDir/".oneTwoTree_CONSTS_and_Functions::LOG_FILE;

# checking if jobId is valid
if (!($jobId =~ /^[0-9]+\z/))
{
	$jsonData{'errorOccured'} = 1;
	$jsonData{'error'} = "Job $jobId contains invalid characters";
}
else
{
	#my $curJobDir = oneTwoTree_CONSTS_and_Functions::RESULTS_LINK."/$jobId";

	
	# checking if job directory exists
	if (-d $curJobDir)
	{
		my $paramsFromFile = &GetParamsFromFile($jobId, $curJobDir);
		my %params_vars = %$paramsFromFile;
		
		%jsonData = (%jsonData, %params_vars);
	}
	else
	{
		$jsonData{'errorOccured'} = 1;
	    $jsonData{'error'} = "Job $jobId does not exists.";
	}
}


# parsing return data to json and returnig it to client
my $json = encode_json(\%jsonData);
print $query->header();
print "$json\n";

sub GetParamsFromFile
{
	my ($jobId, $curJobDir) = @_;
	my %jsonData;
	
	$jsonData{'jobId'}		= $jobId;
	$jsonData{'v_include_Nuc'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'include_Nuc');
	$jsonData{'v_include_Mt'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'include_Mt');
	$jsonData{'v_include_CP'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'include_CP');
	$jsonData{'v_ClusteringMethod'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'ClusteringMethod');
	$jsonData{'v_Seq_Ratio'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Seq_Ratio');
	$jsonData{'v_Ortho_Inflation'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Ortho_Inflation');
	$jsonData{'v_MSA_Software'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'MSA_Software');
	$jsonData{'v_MAFFT_maxiterate'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'MAFFT_maxiterate');
	$jsonData{'v_PairwiseAlignmentMethod'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'PairwiseAlignmentMethod');
	$jsonData{'v_FilterMSA_Method'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'FilterMSA_Method');
	$jsonData{'v_Guidance_RowCol'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Guidance_RowCol');
	$jsonData{'v_Trimal_CutOff'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Trimal_CutOff');
	$jsonData{'v_gb_SmallerBlocks'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'gb_SmallerBlocks');
	$jsonData{'v_gb_AllowGaps'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'gb_AllowGaps');
	$jsonData{'v_gb_LessStrictFlanking'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'gb_LessStrictFlanking');
	$jsonData{'v_Tree_Method'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Tree_Method');
	$jsonData{'v_User_MrBayes_Model'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'User_MrBayes_Model');
	$jsonData{'v_clock_model'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'clock_model');
	$jsonData{'v_relaxed_branch_option'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'relaxed_branch_option');
	$jsonData{'v_ngen'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'ngen');
	$jsonData{'v_samplefreq'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'samplefreq');
	$jsonData{'v_nchains'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'nchains');
	$jsonData{'v_burninFrac'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'burninFrac');
	$jsonData{'v_checkFreq'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'checkFreq');
	$jsonData{'v_User_RAxML_Model'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'User_RAxML_Model');
	$jsonData{'v_Use_BootS_RxOn'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Use_BootS_RxOn');
	$jsonData{'v_Raxml_BootS_vals'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Raxml_BootS_vals');
	$jsonData{'v_User_ExaML_Model'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'User_ExaML_Model');
	$jsonData{'v_Use_BootS_ExOn'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Use_BootS_ExOn');
	$jsonData{'v_Examl_BootS_vals'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Examl_BootS_vals');
	$jsonData{'v_Tree_Type'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'Tree_Type');
	$jsonData{'v_ConstraintNewick'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'ConstraintNewick');
	$jsonData{'v_SplitDiv'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'SplitDiv');
	$jsonData{'v_MinAge'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'MinAge');
	$jsonData{'v_MaxAge'}=&ReadParam('$curJobDir/'.oneTwoTree_CONSTS_and_Functions::FILENAME_PARAMS_TXT,'MaxAge');

	return \%jsonData;
}



