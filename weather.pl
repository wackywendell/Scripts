#!/usr/bin/perl

use Switch;
use Encode;
use Text::Wrap;


# This script was written by lvleph and inspired by the original conky weather script written by azhag (azhag@bsd.miki.eu.org)
# Modyfied by LazarusHC to list more details

$code=$ARGV[0]; #zipcode or weather.com city code
$system=$ARGV[1]; #f for imperial c for metric
$what=$ARGV[2]; #what are we looking for?
$file="/tmp/weather.html"; #temp holding weather
$update=3600; #time in seconds to update $file if set to 0 don't use $file

$leadspace="  "; #spacing before each high low
$trailspace="   "; #spacing after each high low.
$fspaces=""; #spacing between condition symbols.
$dspaces="    "; #spacing between each day
$lines="\n\n\n\n"; #each \n represents one line between the days and temps

$Text::Wrap::columns = 58;
$initial_tab=""; #tab before first line in weather output
$subsequent_tab="\t"; #tab before each subsequet line in weather output

$degree= encode_utf8( "\x{00B0}" ); #give me the degree symbol, not everyone has same locale

#ensure user inputs proper system
if($system !=~ "c" || $system !=~ "f"){$what=0;} #this will give usage error 

switch($what){ #determine what user wants
	case "c" { #if current conditions
		&file_op; #save weather to $file
		while(<FILE>){ #cycle through file
			if (/<em>Current conditions/ .. /<h3>/){ #found current conditions
				($cn2) = /<h3>(\b.+\b)<\/h3>/; #save current conditions
				if($cn2){print "$cn2\n"; exit;}			
			}
		}
	}
	case "w" { #if list
		&file_op; #save weather to file
		while(<FILE>){ #cycle through file
			if (/<dt>Feels Like:<\/dt>/ .. /<dd>/){ #found feels like temp
				($tmf) = /<dd>(-?\d+)/; #sav temp								
			}
			if (/<dt>Humidity:<\/dt>/ .. /<dd>/){ #found current humidity
				($hmt) = /<dd>(\d+\%)/; #save current humidity					
			}
			if (/<dt>Wind:<\/dt>/ .. /<dd>/){ #found wind conditions
				($wnd) = /<dd>(\b.+\b)<\/dd>/; #save wind conditions
				#do we have current conditions?
				if($tmf && $hmt && $wnd){
					print "Feels like:  $tmf$degree\n";
					print "Humidity:    $hmt\n"; 
					print "Wind:        $wnd\n"; exit;}
			}
		}
	}	
	case "cp" { #if current conditions symbol
		&file_op; #save weather to $file
		while(<FILE>){ #cycle through file
			if (/<em>Current conditions/ .. /<h3>/){ #found current conditions
				($cnd) = /<h3>(\b.+\b)<\/h3>/; #save current conditions
				#do we have current conditions? Then translate into symbol
				if($cnd){cond_symb($cnd); print "$ctext\n"; exit;}
			}
		}
	}	
	case "t" { #if current temp
		&file_op; #save weather to $file
		while(<FILE>){ #cycle through file
			if (/<div id="forecast-temperature">/ .. /<h3>/){ #found current temp
				($tmp) = /<h3>(-?\d+)/; #save current temp
				#do we have current temp? Then print
				if($tmp){print "$1$degree\n"; exit;}
			}
		}
	}
	case /[1-5]d$/ { #display the days up to specified day 
		&file_op; #save weather to $file
		my $day=(split "t", $what)[0]; #how many days are we looking for
		my $count=0; 
		while(<FILE>){
			if(/<th>(\b.+\b)<\/th>/ && ++$count<=$day){ #look for the conditions upto specified day
				$days[$count-1]=$1; #save day
				&day_space($days);
			}
			elsif($count>=$day){print "$dtext\n"; exit;} #don't keep lopking if everything has been found
		}
	}
	case /[1-5]dp$/ { #display the conditions from today through day $days
		&file_op; #save weather to $file
		my $day=(split "p", $what)[0]; #how many days are we looking for
		my $flag=0; #set flag for when we find start of conditions
		my $count=0; 
		while(<FILE>){
			if(/^<tr class="titles">\s*$/){$flag=1;} #found the start of conditions
			elsif($flag && /(\b.+\b)<\/td>/ && ++$count<=$day){ #look for the conditions upto specified day
				$cnd[$count-1]=$1; #save conditions
				&cond_symb ($cnd[$count-1]); #translate conditions to symbol
				#exit;
			}
			elsif($count>=$day){print "$ctext\n"; exit;} #don't keep looking if everything has been found
		}
	}
	case /[1-5]t$/ { #display the temps from today through day $days
		&file_op; #save weather to $file
		my $count=0;
		my $day=(split "t", $what)[0]; #how many days are we looking for
		while(<FILE>){
			#get the high temp
			(my $high) = /<td><strong>High: (-?\d+)&deg;<\/strong><span>Low: \-?\d+&deg;<\/span><\/td>/;
			#get the low temp
			(my $low) = /<td><strong>High: \-?\d+&deg;<\/strong><span>Low: (-?\d+)&deg;<\/span><\/td>/;
			#print the high and low temp for the specified day
			if($high=~/\d+/ && $low=~/\d+/ && ++$count<=$day){print "$leadspace$high$degree/$low$degree$trailspace";}
			elsif($count>=$day){print "\n"; exit;} #don't keep looking if everything has been found
		}
	}
	case /[1-5]dt$/ {
		&file_op; #save weather to $file
		my $count1 = my $count2=0;
		my $day=(split "dt", $what)[0]; #how many days are we looking for
		my $flag=1; #print days once
		while(<FILE>){
			#get the high temp
			(my $high) = /<td><strong>High: (-?\d+)&deg;<\/strong><span>Low: \-?\d+&deg;<\/span><\/td>/;
			#get the low temp
			(my $low) = /<td><strong>High: \-?\d+&deg;<\/strong><span>Low: (-?\d+)&deg;<\/span><\/td>/;
			#print the high and low temp for the specified day
			if(/<th>(\b.+\b)<\/th>/ && ++$count1<=$day){ #look for the conditions upto specified day
				$days[$count1-1]=$1; #save day
				&day_space($days);
			}
			elsif($high=~/\d+/ && $low=~/\d+/ && ++$count2<=$day){$ttext.=$leadspace.$high.$degree."/".$low.$degree.$trailspace;}
			elsif($count1>=$day && $count2>=$day){print "$dtext\n$lines$ttext\n"; exit;} #don't keep lopking if everything has been found
		}
	}
	case /[1-7]w$/ { #display the weather forecast in words from today through day $days
		&file_op; #save weather to $file
		my $num=(split "w", $what)[0]; #how many are we looking for
		my $count=0; #initialize count
		while(<FILE>){ #cycle through file
			#get the weather
			(my $when) = /<li><strong>(\b.+\b\:)<\/strong>/;
			(my $weather) = /<\/strong>(.+)<\/li>/;
			$weather=$when.$weather;
			#print weather
			if($when && ++$count<=$num){
				#print "$when";
				print wrap($initial_tab, $subsequent_tab, $weather);
				print "\n";
			}
			elsif($count>=$num){exit;} #don't keep looking if everything has been found
		}
	}
	case /[1-5]p$/ { #if conditions of specified day
		&file_op; #save weather to $file
		my $day=(split "p", $what)[0]; #what day are we looking for
		my $flag=0; #set flag for when we find start of conditions
		my $count=0; 
		while(<FILE>){
			if(/^<tr class="titles">\s*$/){$flag=1;} #found the start of conditions
			elsif($flag && /(\b.+\b)<\/td>/ && ++$count==$day){ #look for the conditions for specified day
				$cnd=$1; #save conditions
				&cond_symb ($cnd); #translate conditions to symbol
			}
			elsif($count>=$day){print "$ctext\n"; exit;} #don't keep looking if everything has been found
		}
	}
	case /[1-5]$/ { #if temp of specified day 
		&file_op; #save weather to $file
		while(<FILE>){
			#get the high temp
			($high) = /<td><strong>High: (-?\d+)&deg;<\/strong><span>Low: \-?\d+&deg;<\/span><\/td>/;
			#get the low temp
			($low) = /<td><strong>High: \-?\d+&deg;<\/strong><span>Low: (-?\d+)&deg;<\/span><\/td>/;
			#print the high and low temp for the specified day
			if($high && $low && ++$count==$what){print "$high$degree/$low$degree\n";}
		}
	}
	else { #didn't give proper options
		&usage; #print usage error
	}
}

#print "\n"; # need endline to make things look nice

close FILE;

sub file_op { #do file operations
	if(-e $file ){ #does the file exist and is not empty?
		my $size=`stat -c %s $file`;
		if($size >= 1000){
			my $date=`date -u +%s`; #get current date in seconds
			my $created=`stat -c %Y $file`; #get creation date of file in seconds
			$age=$date - $created; #determine age of file
		}
		else{
			$age=$update+1;
		}
	}
	else{ #if file doesn't exist make it and set to update the file
		`touch $file`;
		$age=$update+1;
	}

	if ($age>=$update){ #only get a new file every hour
		#obtain the weather forecast and store it in $file
		`wget -O - http://weather.yahoo.com/forecast/"$code"_"$system".html > $file`;
	}
	open(FILE, $file) or die "Could not open file $file: $!\n";
}

sub usage { #if correct options haven't been passed usage error
		print "Usage error weather.pl <citycode> <system> <option>\n";
		print "weather.pl <citycode> <system> <option>\n";
		print "\t<citycode> - weather.com city code\n";
		print "\t<system> - c for metric or f for imperial\n";
		print "\t<option> - Only one option can be entered at a time\n";
		print "\t\tc displays current conditions\n";
		print "\t\tw displays list of current conditions\n";
		print "\t\tcp displays current conditions symbol\n";
		print "\t\tt displays current temp in chosen system\n";
		print "\t\t[1-5]d displays the days up to specified day\n"; 
		print "\t\t[1-5]dp displays condition symbol for days up to specified day\n";
		print "\t\t[1-5]t displays high/low temp in chosen system up to specified day\n";
		print "\t\t[1-5]dt displays days and then high/low temp in chosen system up to specified day\n";
		print "\t\t[1-7]w displays the weather in words up number specified\n";
		print "\t\t[1-5]p displays conditions for specified day\n";
		print "\t\t[1-5] displays high/low temp in chosen system for specified day\n";
}

sub cond_symb { #translates conditions into symbol in weather font
	if ($_ =~ "Partly Cloudy"){$_="c";}
	elsif ($_ =~ "Fair" || $_ =~ "Sun" || $_ =~ "Clear"){$_="A";}
	elsif ($_ =~ "Cloud" || $_ =~ "Fog"){$_="e";}
	elsif ($_ =~ "Storm" || $_ =~ "Thunder" || $_ =~ "T-"){$_="i";}
	elsif ($_ =~ "Snow" || $_ =~ "Flurries" || $_ =~ "Wintry"){$_="k";}
	elsif ($_ =~ "Rain" || "Drizzle"){$_="h";}
	elsif ($_ =~ "Shower"){$_="g";}
	$ctext.=$_.$fspaces;
}

sub day_space { #Adds spaces for aligment
	if ($_ =~ "Today"){$_="  Today ";}
	elsif ($_ =~ "Tonight"){$_="Tonight";}
	elsif ($_ =~ "Tomorrow"){$_="Tomorrow";}
	elsif ($_ =~ "Thu"){$_="   Thu  ";}
	elsif ($_ =~ "Fri"){$_="   Fri  ";}
	elsif ($_ =~ "Sat"){$_="   Sat  ";}
	elsif ($_ =~ "Sun"){$_="   Sun  ";}
	elsif ($_ =~ "Mon"){$_="   Mon  ";}
	elsif ($_ =~ "Tue"){$_="   Tue  ";}
	elsif ($_ =~ "Wed"){$_="   Wed  ";}
	$dtext.=$_.$dspaces;
}
