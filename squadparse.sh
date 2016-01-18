#!/bin/bash
#
# This script parses a set of images extracted from the Game screen
# and performs OCR on them using tesseract and gocr tools.
# 
# It also extracts some nice thumbnails for the characters based on their
# names and saves on the /tmp/heroes/thumbs and /tmp/heroes/shards folders
#
# ALL numbers bellow are magic.

# Global parameters for the OCR tools used
export tess="tesseract stdin stdout -l por -psm 7"
export gocr="gocr -p /tmp/gocrdb/ -f UTF8 -"

# Output directories
mkdir -p /tmp/heroes/{thumbs,shards}

# Loop over all characters ...
for i in `seq 0 70`; do
	# Setting up some global constants
    char=`printf '/tmp/squaddump-character-%02d-char.png' $i`
    stat=`printf '/tmp/squaddump-character-%02d-stat.png' $i`
	star=`printf '/tmp/squaddump-character-%02d-star.png' $i`

	# Parses the character level
    level=$(convert -crop 43x39+102+875  $char - | $tess)

	# Parses the character power
    power=$(convert -crop 82x40+1712+173 $char - | convert - -resize 800x600 pnm:- | $tess | sed 's/[^0-9]//g')
    
	# Parses and fixes the character name. This is the hardest part and the parameters
	# bellow produced the best results possible.
    name=$(convert -crop 586x44+348+91 -threshold 60% $stat - | convert - -resize 800x600 pnm:- | $tess)
	name=$( echo "$name" | sed \
		-e 's/Draide/Dróide/g' \
		-e 's/\[IT-5555/CT-5555/g' \
		-e 's/IG-I 00/IG-100/g' \
		-e 's/l(on/Kylo/g' \
		-e 's/Fase l/Fase I/g' \
		-e 's/IIS-86/IG-86/g' \
		-e 's/IIS-88/IG-88/g' \
		-e 's/Qui-Bon/Qui-Gon/g' \
		-e 's/Motf/Moff/g' \
		-e 's/URORR/URoRR/g' )

	# Parses the gear and fixes some weird symbols.
    gear="I"
    if [ $level -gt 1 ] ; then
        gear=$(convert -crop 258x48+675+835 -threshold 60% $char pnm:- | $tess)
		gear=$(echo "$gear" | sed -e 's/\\Í/VI/g')
	gear=$(echo $gear | sed 's/\./. /g' | awk '{print $3}')
    fi

	# Parses the required and current shard count for the next promotion/activation.
    shards=$(convert -crop 45x46+1776+678 -threshold 90% $char pnm:- | $gocr | tr 'O' '0' | sed 's/[^0-9]//g' )
    myshards=$(convert -crop 40x45+1721+678 -threshold 90% $char pnm:- | $gocr | sed 's/[^0-9]//g')

	# Fetch star rating. Tricky, but works just fine.
	# 1. We convert the image into black and white, after blurring/sharpenning,
	#    so we have a temp file with white circles.
	convert -crop 218x36+851+209 $char -blur 4x8 pnm:- | convert - -sharpen 0x12 -negate -threshold 15% -negate $star
	# 2. We check the highest pixel that is white,
	#    and identify what is the highest start active.
	starcount=7
	for x in 200 170 140 110 80 50 20 ; do
		pixel=`convert $star -crop 1x1+$x+18 -depth 8 txt:- | tail -n 1 | awk '{print $3}'`
		if [ x"$pixel" = x"#FFFFFF" ] ; then break ; fi
		let starcount--
	done

	# TODO(ronoaldo): Export the health as well.
	# Here we get all stats in CSV format
    # printf "%6s;%3s;%2s;%2s;%3s;%s;%s\n" "${power}" "${level}" "${myshards}" "${shards}" "${gear}" "${starcount}" "${name}"
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "${power}" "${level}" "${starcount}" "${gear}" "${myshards}" "${shards}" "${name}"

	# Finally, we crop the character pictures. 
	convert -crop 317x596+802+246 $char "/tmp/heroes/thumbs/${name}.png"
	convert -crop 88x88+1522+742  $char "/tmp/heroes/shards/${name}.png"
done

