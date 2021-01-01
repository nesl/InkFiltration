# InkFiltration: Using Inkjet Printers for Acoustic Data Exfiltration from Air-Gapped Networks

A covert channel can be established by leveraging the acoustic emissions of inkjet printers to exfiltrate information from an air-gapped network. In essence, malware installed on a computer with access to a printer can inject certain imperceptible patterns into all documents being sent to the printer, so as to control the printing process in such a way that an acoustic signal is generated which can be captured with a nearby smartphone.

The code consists of the follwing:

1. A series of programs used to inject the patterns into documents. These are located in the **patternInjection** directory.
1. The **receiver** code that was implemented both in MATLAB and for an Android app.

To download with the submodules use the next command: git clone --recurse-submodules https://github.com/nesl/InkFiltration.git

# Procedure to add a new printer

## Trying existing parameters

First of all, to add a new printer, you could try and test if the existing functions work with it. For that you may print a page and record the sounds for both the case were you have a blank page and were you have a page with text.
Use the next command to create a blank page with modulation for a desired printer (e.g. for an HP printer):
./randomBits.sh HP 1

Or to create a text page with modulation, you can use one of the layouts in the Layouts directory:
./randomBits.sh -tf Layouts/simpleLayoutArial.pdf HP 1

Executing either command will result in a text file containing the random bits used in the modulation, for reference, with a name like HP251_bits or HP101text_bits respectively.
A pdf file named as testPDF.pdf will also be created, and this file will be the one that should be printed.

In linux, printing should be made from the command line when testing, as other programs may add some modifications to the pdf file that would render ineffective the modulation.
To print from command line you first need to get the printer's name, which can be retrieved by calling:
lpstat -e
Which will display a list of printers that have been configured in your system.
Search for your desired printer, copy its name and use the next command to print the file:

lp -d PRINTER_NAME testPDF.pdf

With this command you can specify the page range with the -P option, and the number of copies with the -n option.

After recording the sound of the printer while printing, you can use the MATLAB program "testdemod.m" to inspect the waveform and spectrogram and see if anything coherent surfaces.
You may want to convert the sound file into wav format by using for example "ffmpeg -i filename.oldformat filename.newformat"

If transmission doesn't seem to be correct, you may use 

For testing purposes you can record directly from your computer by using the following command:
arecord -t wav -c 1 -r 44100 -f S16_LE file.wav

To aide you through this testing procedure, you may try to also record the sound so that you can inspect it again as many times as you want.

## Discovering new parameters

### Testing algorithm for DPPM:

1. Two parameters are important at first, line_offset and yellow_shade_blank. The first tests should try to print sequences of lines and see if the number of rollers sounds the printer makes is equivalent to the number of lines sent to print (just take into account that the first and last lines may not generate the same sound because of their proximity to the initial and final sounds the printer makes). A sequence like "111111" or "000000" may be good enough to determine this. It should be noticed that in this step you should no try at first to use the lightest yellow shade as that may not be recognized by the printer (yellow_shade_blank use for example 0.9 or less). Then, if the number of lines doesn't correspond to the number of sounds, you should try to increase the line offset. If your line offset is sufficient, you may try decreasing it until you find its limit, the same with the yellow shade value, you may increase it until you see the printer stops recognizing the lines. Just remember that decreasing the offset size may also attenuate the sound, so you also need to take this into account.

2. Once you have the correct offset and color, you should try printing patterns like "1010110101", which should result in a combination of short and large pulse differences. It should be noted that you should try both "10" and "01" patterns as there may be some issues when changing the bit order. If it results in problems, you may try changing the short_alignment parameter towards either "right", "center", or "left", as this alignes the short lines towards a respective side.

3. You may want to play with the line_length parameter so as to produce the maximum difference in time between pulses by combining the shortest line possible with the longest line possible. Finally, you may want to add a guard line both at the start (guard_init) as well as at the end (guard_end) to isolate the sounds from the start and end sounds the printer makes. It may also work if you change the starting point by modifying the blank_total parameter.

4. Calculating the packet size (packet_size_blank) is just a matter of counting the number of lines that you are able to inject into the document without passing the margins (remember that the lower limit is 9).

### Testing algorithm for FPM-DPPM

1. You may want to start with a relatively large rectangle width (rec_width maybe 100) and print a bit sequence like 101010 and see if there is a frequency occurs. You should try this also with a not so light yellow shade (yellow_shade_text of 0.9 o less). After this you should try to reduce the rectangle width to its minimum. At this point it is recommended to use the blank file Layouts/whitePages.pdf.

./raw_injection.sh -tf Layouts/whitePages.pdf HP_Deskjet_1115 "101010101010"

2. Because this modulation is supposed to be used with text, and blank documents might produce other behaviour, if somehow the previous procedure didn't produce any change, you should now try with a text document. When testing with a text document the modulation may not work as well as with the blank document. At this point you may first want to modify the cluster lines width (cluster_width) large enough, you may also want to reduce the number of cluster lines (cluster_lines and cluster_lines_after_rec) to 0 (which means only one line is utilized) and play again with the rectangle width parameter. There is a trick you can do so as to lower the blackness of the text in the document so as to enhance the power of the patterns by specifying the -b flag. Another trick you can use is to reduce the length of the cluster lines so as to make them encompass only the same space as the text in the document, by modifying the cluster_left_margin and cluster_line_length parameters (by putting 56.8 and 500 for example).

3. Once you can achieve the same frequency effect with text documents, you may want to add cluster lines and test the modulation in text documents with gaps in them, to see if it is robust to those spacings (you may also want to test it again on a blank page). Now, at this point you may want to make sure the next patterns are also handled well: "111", "000", and derived variations. At this point you may need further tinkering by utilizing both the cluster_width_after_rec and cluster_lines_after_rec, which are bit sequence dependent. The first one modifies the buffer cluster lines introduced after every rectangle and the second one modifies the number of lines in this cluster. This is important specially when you have continous rectangles as each of this should be separated by a cluster of lines. For this part you may already want to use the MATLAB scripts to find the time offset between pulses and analyze the waveform. There is also custom_space_rules_rec which gives you a finer control on space following a rectangle and extra_cluster_line for space following a cluster of lines.
