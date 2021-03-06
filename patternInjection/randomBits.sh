#!/bin/bash

FLOOR=0;
CEILING=1;
RANGE=$(($CEILING-$FLOOR+1));

if [ "$#" -lt 2 ]; then
	echo "Wrong number of paramenters. Usage: randomBits.sh [options] printer pages"
	echo "Use this function to generate random bit patterns that are injected into 'pages' number of pages of a PDF file ready to be printed by a 'printer'. By default the program injects the patterns into a PDF file with white pages"
	echo -e "Current defined printers: $(python3 ./testPrinter.py -l)"
	echo -e "Options:\n -l : reuse previous random bit patterns\n -f [file] : PDF file to be injected with patterns (by default it injects to a blank document)\n -o : instead of random bits, create a sequence that increases in value and starts with zero"
	exit 1
fi

LOAD=""
ORDERED=""
FILE_IN="Layouts/simpleLayoutBlank.pdf"


ARGUMENTS=(${@: -2})


while getopts "lof:" arg; do
	case ${arg} in
		l ) 
		LOAD="y"
		;;
		f ) 
		FILE_IN="${OPTARG}"
		;;
		o ) 
		ORDERED="y"
		;;
	esac
done

PEEPDF="python2 peepdf/peepdf.py"

cp Layouts/whitePDF.pdf.old Layouts/whitePDF.pdf

NUM_PAGES=${ARGUMENTS[1]}
PRINTER=${ARGUMENTS[0]}

MANCHESTER=""

: '
if [ $PRINTER = "HP_Deskjet_1115" ]; then
        MANCHESTER="-m"
fi
'


AKA=$($PEEPDF -C 'search "/Type /Page"'  $FILE_IN | cut -f1 -d$'\x1b')
AKA2=$(echo -n $AKA | tr -d '[]')
IFS=', ' read -r -a array <<< $AKA2
AKA=$($PEEPDF -C 'search "/Type /Pages"'  $FILE_IN | cut -f1 -d$'\x1b')
AKA2=$(echo -n $AKA | tr -d '[]')
array=( ${array[@]/$AKA2} )
pdftk $FILE_IN cat 1 output Layouts/whitePDF.pdf

NUM_BITS=$(python3 ./testPrinter.py $MANCHESTER -ti $PRINTER)



FILE_BITS="../receiver/MATLAB/payloads/${PRINTER}_${NUM_BITS}_${NUM_PAGES}text_bits"


#if [ -n "$LOAD" ]; then

AKA=$($PEEPDF -C 'search "/Type /Page"'  Layouts/whitePDF.pdf | cut -f1 -d$'\x1b')
AKA2=$(echo -n $AKA | tr -d '[]')
IFS=', ' read -r -a array2 <<< $AKA2
AKA=$($PEEPDF -C 'search "/Type /Pages"'  Layouts/whitePDF.pdf | cut -f1 -d$'\x1b')
AKA2=$(echo -n $AKA | tr -d '[]')
array2=( ${array2[@]/$AKA2} )
AKA3=$($PEEPDF -C "object ${array2[0]}" Layouts/whitePDF.pdf | grep -oE "/Contents\s[0-9]+" | cut -f2 -d" ")
echo -e "modify stream $AKA3 randomStream\nsave" > randomScript

#fi

BIT_NUMBER=0


echo -e "\nSUCCESSFUL INJECTION (testPDF.pdf)----------------\nPAYLOAD saved in $FILE_BITS\n"

for j in $(seq $NUM_PAGES)
do

	if [ -z "$LOAD" ]; then
                if [ -z "$ORDERED" ]; then
                        for i in $(seq $NUM_BITS)
                        do

                                RESULT=$RANDOM;
                                let "RESULT %= $RANGE";
                                RESULT=$(($RESULT+$FLOOR));

                                FINAL="$FINAL$RESULT"

                        done
                        
                else
                        FINAL=$(printf "%0${NUM_BITS}d" $(echo "obase=2;$BIT_NUMBER" | bc))
                        BIT_NUMBER=$(($BIT_NUMBER+1))
		fi
		
	else
		if [ $j -eq 1 ]; then
			FINAL="$(tail -c +$(((j-1)*$NUM_BITS)) $FILE_BITS | head -c $NUM_BITS)"
		else
			FINAL="$(tail -c +$(((j-1)*$NUM_BITS+1)) $FILE_BITS | head -c $NUM_BITS)"
		fi	
	fi

	
	#echo $FINAL
	
        AKA3=$($PEEPDF -C "object ${array[$(($j-1))]}" $FILE_IN | grep -oE "/Contents\s[0-9]+" | cut -f2 -d" ")
        STREAM=$($PEEPDF -C "stream $AKA3" $FILE_IN | cut -f1 -d$'\x1b')

        python3 ./testPrinter.py $MANCHESTER -t -p $FINAL $PRINTER > randomStream

        if [ $PRINTER = "Epson_L4150" ]; then
                echo "$STREAM" | sed 's/0 0 0 rg/0.01 g/; s/0 0 0 RG/0.01 G/' >> randomStream			
        elif [ $PRINTER = "Canon_MG2410" ]; then
                echo "$STREAM" | sed 's/0 0 0 rg/0.01 g/; s/0 0 0 RG/0.01 G/' >> randomStream			
        else
                echo "$STREAM" >> randomStream
        fi

			

	$PEEPDF -s randomScript Layouts/whitePDF.pdf > log



	if [ $j -eq 1 ]; then
		cp Layouts/whitePDF.pdf testPDF.pdf
		if [ -z "$LOAD" ]; then
			echo -n $FINAL > $FILE_BITS
		fi

	else
		pdfunite testPDF.pdf Layouts/whitePDF.pdf tmpPDF.pdf
		mv tmpPDF.pdf testPDF.pdf
		if [ -z "$LOAD" ]; then
			echo -n $FINAL >> $FILE_BITS
		fi


	fi
	
	echo -e "$FINAL"
	
	FINAL=""
done

rm randomStream randomScript

echo
