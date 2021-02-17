#!/usr/bin/env python

import sys, getopt, math
import numpy as np

image_array = np.full((790, 612, 3), 255, dtype = np.uint8) 
        
def add_shape(x, y, width, height):
    global image_array
    
    print("%.2f %.2f %i %.2f re" %(x, y, width, height))
    
    if(y > 0):
        y_index = int(round(800-y))
        x = int(x)
        image_array[y_index-int(height):y_index, x:x+int(width),:] = (0,200,255)
        
def add_line_rectangle(x, width, height, num_lines):
        global total
        
        add_shape(x, total, width, 1)
        total -= height/(num_lines+1)
        for i in range(num_lines):
                add_shape(x, total, width, 1)
                total -= height/(num_lines+1)
        add_shape(x, total, width, 1)
        

def to_manchester(pattern):
        
        new_pattern = ""
        for i in pattern:
                if(int(i)):
                        new_pattern += "01"
                else:
                        new_pattern += "10"
                        
        return new_pattern
        
        
def blank(parameters, packet):
        global total, max_length
        offset = parameters['line_offset'] #offset between lines, the unit is points
        length = parameters['line_length'] #length of the short line, the length of the long line is supposed to be the largest possible in a letter sized page (594)

        if('blank_total' in parameters):
                total = parameters['blank_total']
                
        short_alignment = parameters['short_alignment'] #The short line can be aligned to the 'center', 'left' or 'right'

        
        if(short_alignment == "left"):
                left_margin = 9
        elif(short_alignment == "center"):
                left_margin = int((max_length+9-length)/2)
        elif(short_alignment == "right"):
                left_margin = max_length+9 - length
                
                
        guard_init = parameters['guard_init'] #Modulation may require an initial line that separates the data transmission from the initial printer procedures. You can specify how many initial lines to separate your data lines.
        
        if(guard_init > 0):
                for i in range(guard_init):
                        add_shape(9, total, max_length, 1)
                        total -= offset
                
        for bitidx in packet:

                if(not int(bitidx)):
                                add_shape(left_margin, total, length, 1)
                else:
                        add_shape(9, total, max_length, 1)
                
                total -= offset
                
        if(parameters['guard_end']):
                add_shape(9, total, max_length, 1)#A final "guard" line is added so as to make sure the last time offset falls between individual roller pulses and not with respect to the random noises that the printer makes when it finishes printing a page
        
def text(parameters, packet):
        global total, max_length
        
        
        text_guard_init = parameters['text_guard_init'] #Extra element at the beginning of the page
        guard_end = parameters['guard_end'] #Extra element at the end of the page
        
        use_rectangles = parameters['use_rectangles'] #You can use lines instead of rectangles
        
        
        if(use_rectangles):
                use_only_rectangles = parameters['use_only_rectangles'] #Use only rectangles of different size
                rec_width = parameters['rec_width'] #Rectangle width
                rec_left_margin = parameters['rec_left_margin'] #Rectangle left margin
                rec_line_length = parameters['rec_line_length'] #Rectangle length
                

                if(use_only_rectangles):
                        rec_width2 = parameters['rec_width2'] #Rectangle width
                        rec_left_margin2 = parameters['rec_left_margin2'] #Rectangle left margin
                        rec_line_length2 = parameters['rec_line_length2'] #Rectangle length
                else:
                        extra_cluster_line = parameters['extra_cluster_line'] #If you need to add an extra line in some conditions
                        cluster_width = parameters['cluster_width']  #Cluster of lines total width
                        cluster_lines = parameters['cluster_lines'] #Number of cluster lines
                        cluster_left_margin = parameters['cluster_left_margin'] #Cluster of lines left margin
                        cluster_line_length = parameters['cluster_line_length'] #Cluster of lines length
                        custom_space_rules_rec = parameters['custom_space_rules_rec'] #If you need more control over spacing when dealing with different bit sequences
                        asymmetric_lines_after_rec = parameters['asymmetric_lines_after_rec'] #If you don't want the lines after a rectangle to be symmetrical in space
                        if(custom_space_rules_rec):
                                cluster_width_after_rec_before_cluster = parameters['cluster_width_after_rec_before_cluster']
                                cluster_width_after_rec_before_rec = parameters['cluster_width_after_rec_before_rec']
                                cluster_lines_after_rec_before_cluster = parameters['cluster_lines_after_rec_before_cluster']
                                cluster_lines_after_rec_before_rec = parameters['cluster_lines_after_rec_before_rec']
                        else:
                                cluster_width_after_rec = parameters['cluster_width_after_rec'] #Cluster of lines total width after a rectangle is drawn (special case)
                                cluster_lines_after_rec = parameters['cluster_lines_after_rec'] #Number of cluster lines after a rectangle is drawn (special case)
                        
        else:
                extra_cluster_line = parameters['extra_cluster_line'] #If you need to add an extra line in some conditions
                cluster_width = parameters['cluster_width']  #Cluster of lines total width
                cluster_lines = parameters['cluster_lines'] #Number of cluster lines
                cluster_left_margin = parameters['cluster_left_margin'] #Cluster of lines left margin
                cluster_line_length = parameters['cluster_line_length'] #Cluster of lines length
                cluster_width2 = parameters['cluster_width2']  #Cluster of lines total width
                cluster_lines2 = parameters['cluster_lines2'] #Number of cluster lines
                cluster_left_margin2 = parameters['cluster_left_margin2'] #Cluster of lines left margin
                cluster_line_length2 = parameters['cluster_line_length2'] #Cluster of lines length
                
                
        
        
        


        if('text_total' in parameters):
                total = parameters['text_total']
                
                
        """
        add_shape(cluster_left_margin2, total, cluster_line_length2, 1)
        total -= cluster_width2/(cluster_lines2+1)
        for i in range(cluster_lines2):
                add_shape(cluster_left_margin2, total, cluster_line_length2, 1)
                total -= cluster_width2/(cluster_lines2+1)
        """
        
        packet = "1"*text_guard_init + packet
                
        if(guard_end):
                if(not use_rectangles):
                        packet += "111"
                        
        
        
        for j,bitidx in enumerate(packet):
                
                
                
                #For Canon
                if(j + 1 < len(packet) and packet[j:j+2] == "10"):
                        total -= rec_width2/2.0
                        add_shape(rec_left_margin, total, rec_line_length, rec_width2/2.0)
                        total -= rec_width2/2.0
                        add_shape(rec_left_margin2, total, rec_line_length2, rec_width2/2.0)
                        continue
                
                        

                if(not int(bitidx)):
                        
                        if(use_rectangles and use_only_rectangles):
                                
                                total -= rec_width2
                                add_shape(rec_left_margin2, total, rec_line_length2, rec_width2)
                                #add_shape(300, total, 1, rec_width2)
                        else:
                                add_shape(cluster_left_margin, total, cluster_line_length, 1)
                                #add_shape(200, total, 4, 1)
                                total -= cluster_width/(cluster_lines+1)
                                for i in range(cluster_lines):
                                        add_shape(cluster_left_margin, total, cluster_line_length, 1)
                                        #add_shape(200, total, 4, 1)
                                        total -= cluster_width/(cluster_lines+1)
                                #add_shape(200, total, 4, cluster_width)
                                if(extra_cluster_line):
                                        if(j > 0 and not int(packet[j-1])): #An extra line is drawn when a cluster of lines precedes the actual cluster of lines, e.g., bit sequence 0-0
                                                add_shape(cluster_left_margin, total, cluster_line_length, 1)
                                                total -= cluster_width/(cluster_lines+1)
                                                
                
                else:
                        if(use_rectangles):
                                
                                if(j == 0):
                                        total -= 20.04
                                        add_shape(rec_left_margin, total, rec_line_length, 20.04) 
                                else:
                                        total -= rec_width
                                        add_shape(rec_left_margin, total, rec_line_length, rec_width)
                                #add_shape(200, total, 300, rec_width)
                                #add_shape(50, total, 500, rec_width)
                                
                                if(not use_only_rectangles):
                                
                                        if(custom_space_rules_rec):
                                        
                                                #Space is modified according to whether a rectangle follows another rectangle or a cluster of lines follow a rectangle, e.g., bit sequence 1-1 or 1-0 respectively
                                                
                                                if(j + 1 < len(packet) and not int(packet[j+1])): #Cluster of lines follows rectangle
                                                
                                                        cluster_width_after_rec_tmp = cluster_width_after_rec_before_cluster
                                                        cluster_lines_after_rec_tmp = cluster_lines_after_rec_before_cluster
                                                        
                                                else: #Rectangle follows rectangle
                
                                                        cluster_width_after_rec_tmp = cluster_width_after_rec_before_rec
                                                        cluster_lines_after_rec_tmp = cluster_lines_after_rec_before_rec
                                        else:
                                        
                                                cluster_width_after_rec_tmp = cluster_width_after_rec
                                                cluster_lines_after_rec_tmp = cluster_lines_after_rec
                                
                                        if(asymmetric_lines_after_rec and j + 1 < len(packet) and int(packet[j+1])):
                                                total -= cluster_width_after_rec_tmp/(cluster_lines_after_rec_tmp+2)
                                                for i in range(cluster_lines_after_rec_tmp+1):
                                                        if(i == 1):
                                                                add_shape(cluster_left_margin, total, cluster_line_length, 1)
                                                        total -= cluster_width_after_rec_tmp/(cluster_lines_after_rec_tmp+2)
                                        else:
                                                total -= cluster_width_after_rec_tmp/(cluster_lines_after_rec_tmp+1)
                                                for i in range(cluster_lines_after_rec_tmp):
                                                        add_shape(cluster_left_margin, total, cluster_line_length, 1)
                                                        total -= cluster_width_after_rec_tmp/(cluster_lines_after_rec_tmp+1)
                                                
                        else:
                                
                                if(j == 0):
                                        add_line_rectangle(cluster_left_margin2, cluster_line_length2, 65.52,31)
                                else:
                                        add_line_rectangle(cluster_left_margin2, cluster_line_length2, cluster_width2,cluster_lines2)
                                """
                                add_shape(cluster_left_margin2, total, cluster_line_length2, 1)
                                total -= cluster_width2/(cluster_lines2+1)
                                for i in range(cluster_lines2):
                                        add_shape(cluster_left_margin2, total, cluster_line_length2, 1)
                                        total -= cluster_width2/(cluster_lines2+1)
                                add_shape(cluster_left_margin2, total, cluster_line_length2, 1)#Comment out
                                """

                
        
        if(guard_end):
                if(use_rectangles):
                        total -= rec_width
                        add_shape(9, total, max_length, rec_width)
        
def SweepOffset(parameters):
        global total
        lower_margin = 10.0

        offset = parameters['line_offset']
        total -= offset

        while total > lower_margin:
        
                add_shape(9, total, 594, 1)
                total -= offset
                offset += 2
                
def SweepLength(parameters):
        global total
        offset = 28.0 #Same offset for all printers
        lower_margin = 10.0
        line_size = 594.0
        start = 9.0
        packet_size = int(math.floor((total - lower_margin)/offset))
        line_decrement = math.floor(line_size/packet_size)

        if(parameters['name'] == "Canon_MG2410" or parameters['name'] == "HP_Photosmart_D110"):
                total -= offset

        for i in range(packet_size):
                add_shape(start, total, line_size, 1)
                total -= offset
                line_size -= line_decrement

                if(parameters['name'] == "HP_Photosmart_D110"):
                        start += line_decrement/2
                elif(parameters['name'] == "Epson_L4150"):
                        start += line_decrement


def printer_parameters(key): #Remember to define your printer name below in printer_name_list
         
        global total
        parameters = {}
        
        if(key == 0): #Canon_MG2410
        
                parameters['guard_end'] = True
                
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = True
                parameters['rec_width'] = 38.4#33#33#35.0 Cambiar a menos
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['rec_width2'] = 38.4#56#60.0 Este o 56 only problem is with 5 zeroes
                parameters['rec_left_margin2'] = 590 #550
                parameters['rec_line_length2'] = 13 #53

                parameters['yellow_shade_text'] = 0.94
                parameters['packet_size_text'] = 14#11
                parameters['text_guard_init'] = 1 #cambie esto
                """
                parameters['guard_end'] = True
                
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = True
                parameters['rec_width'] = 33#33#33#35.0 Cambiar a menos
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['rec_width2'] = 60#56#60.0 Este o 56 only problem is with 5 zeroes
                parameters['rec_left_margin2'] = 590 #550
                parameters['rec_line_length2'] = 13 #53

                parameters['yellow_shade_text'] = 0.94
                parameters['packet_size_text'] = 10#11
                parameters['text_guard_init'] = 1 #cambie esto
                """
        
                """
                #Text
                parameters['use_rectangles'] = True
                parameters['rec_width'] = 42.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['cluster_width'] = 28.0
                parameters['cluster_lines'] = 1
                parameters['cluster_width_after_rec'] = 28.0
                parameters['cluster_lines_after_rec'] = 1
                parameters['cluster_left_margin'] = 9
                parameters['cluster_line_length'] = 594
                parameters['custom_space_rules_rec'] = False
                parameters['asymmetric_lines_after_rec'] = False
                parameters['extra_cluster_line'] = True
                parameters['yellow_shade_text'] = 0.94
                parameters['packet_size_text'] = 11
                parameters['text_guard_init'] = False
                """
                
                #Blank        
                parameters['line_length'] = 10
                parameters['line_offset'] = 27.0 #Could be adjusted to 21.0
                parameters['short_alignment'] = "left"
                parameters['guard_init'] = 1
                parameters['blank_total'] = 781
                parameters['yellow_shade_blank'] = 0.94
                parameters['packet_size_blank'] = 25
                
        elif(key == 1): #Epson_L4150
        
                parameters['guard_end'] = True
                
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = True
                parameters['rec_width'] = 40#35#33#35.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['rec_width2'] = 56#60.0
                parameters['rec_left_margin2'] = 9 #550
                parameters['rec_line_length2'] = 3 #53

                parameters['yellow_shade_text'] = 0.99
                parameters['packet_size_text'] = 10#11
                parameters['text_guard_init'] = 0
                """
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = False
                parameters['rec_width'] = 24.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['cluster_width'] = 42.0
                parameters['cluster_lines'] = 3
                parameters['cluster_width_after_rec'] = 42.0
                parameters['cluster_lines_after_rec'] = 3
                parameters['cluster_left_margin'] = 56.8
                parameters['cluster_line_length'] = 500
                parameters['custom_space_rules_rec'] = False
                parameters['asymmetric_lines_after_rec'] = False
                parameters['extra_cluster_line'] = False
                parameters['yellow_shade_text'] = 0.99
                parameters['packet_size_text'] = 12
                parameters['text_guard_init'] = 0
                """
                
                #Blank        
                parameters['line_length'] = 50
                parameters['line_offset'] = 24.0
                parameters['short_alignment'] = "right"
                parameters['guard_init'] = 0
                parameters['yellow_shade_blank'] = 0.97
                parameters['packet_size_blank'] = 32
                
        elif(key == 2): #HP_Photosmart_D110
        
                parameters['guard_end'] = True
                
                #Text
                parameters['use_rectangles'] = False
                parameters['cluster_width2'] = 28#30#25#25#30#34 #28
                parameters['cluster_lines2'] = 15 #16 #12
                parameters['cluster_left_margin2'] = 9
                parameters['cluster_line_length2'] = 594
                parameters['cluster_width'] = 42#45
                parameters['cluster_lines'] = 12#19#12#14#5#14#15#15
                parameters['cluster_left_margin'] = 400
                parameters['cluster_line_length'] = 1
                parameters['yellow_shade_text'] = 0.99#0.98 
                parameters['extra_cluster_line'] = False
                parameters['packet_size_text'] = 10#9#8#10
                #parameters['text_total'] = 700 #750
                parameters['text_guard_init'] = 0
                
                """
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = False
                parameters['rec_width'] = 25.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['cluster_width'] = 32.0
                parameters['cluster_lines'] = 10
                #parameters['cluster_width_after_rec'] = 21.0
                #parameters['cluster_lines_after_rec'] = 5
                parameters['cluster_left_margin'] = 9
                parameters['cluster_line_length'] = 594
                parameters['extra_cluster_line'] = False
                parameters['yellow_shade_text'] = 0.99
                parameters['packet_size_text'] = 15
                parameters['custom_space_rules_rec'] = True
                parameters['cluster_width_after_rec_before_cluster'] = 23.0
                parameters['cluster_width_after_rec_before_rec'] = 31.0
                parameters['cluster_lines_after_rec_before_cluster'] = 5
                parameters['cluster_lines_after_rec_before_rec'] = 5
                parameters['asymmetric_lines_after_rec'] = False
                parameters['text_guard_init'] = 0
                """
        
                #Blank        
                parameters['line_length'] = 100
                parameters['line_offset'] = 25.0
                parameters['short_alignment'] = "center"
                parameters['guard_init'] = 0
                parameters['yellow_shade_blank'] = 0.99
                parameters['packet_size_blank'] = 30
                
        elif(key == 3): #HP_Deskjet_1115
        
                parameters['guard_end'] = False
                
                #Text
                parameters['use_rectangles'] = False
                parameters['cluster_width2'] = 32#16#28#30#25#25#30#34 #28 or 24.5
                parameters['cluster_lines2'] = 15#7#16 #12
                parameters['cluster_left_margin2'] = 9
                parameters['cluster_line_length2'] = 594
                parameters['cluster_width'] = 32#16#42#45
                parameters['cluster_lines'] = 15#7#19#12#14#5#14#15#15
                parameters['cluster_left_margin'] = 601
                parameters['cluster_line_length'] = 2
                parameters['yellow_shade_text'] = 0.975#0.98 
                parameters['extra_cluster_line'] = False
                parameters['packet_size_text'] = 10#9#8#10
                #parameters['text_total'] = 700 #750
                parameters['text_guard_init'] = 1
                """
                parameters['guard_end'] = True
                
                #Text
                parameters['use_rectangles'] = False
                parameters['cluster_width2'] = 25#28#30#25#25#30#34 #28
                parameters['cluster_lines2'] = 5 #16 #12
                parameters['cluster_left_margin2'] = 9
                parameters['cluster_line_length2'] = 594
                parameters['cluster_width'] = 40#42#45
                parameters['cluster_lines'] = 12#19#12#14#5#14#15#15
                parameters['cluster_left_margin'] = 601
                parameters['cluster_line_length'] = 2
                parameters['yellow_shade_text'] = 0.975#0.98 
                parameters['extra_cluster_line'] = False
                parameters['packet_size_text'] = 10#9#8#10
                #parameters['text_total'] = 700 #750
                parameters['text_guard_init'] = 3
                """
                """
                #Text
                parameters['rec_width'] = 25 #minimum 25
                parameters['cluster_width'] = 45#45.0 #50.0
                parameters['cluster_lines'] = 0#3
                parameters['cluster_width_after_rec'] = 55#50#75.0
                parameters['cluster_lines_after_rec'] = 0
                parameters['cluster_left_margin'] = 56.8#56.8
                parameters['cluster_line_length'] = 500#500
                parameters['custom_space_rules_rec'] = False
                parameters['extra_cluster_line'] = False
                parameters['yellow_shade_text'] = 0.98 
                parameters['packet_size_text'] = 15
                #parameters['text_total'] = 700
                """
                """
                #Text
                parameters['rec_width'] = 35#32 #minimum 25
                parameters['cluster_width'] = 50#40#45.0 #50.0
                parameters['cluster_lines'] = 10#3
                #parameters['cluster_width_after_rec'] = 65#50#75.0
                #parameters['cluster_lines_after_rec'] = 1
                parameters['cluster_left_margin'] = 9#56.8
                parameters['cluster_line_length'] = 594#500
                parameters['extra_cluster_line'] = False
                parameters['yellow_shade_text'] = 0.98 
                parameters['packet_size_text'] = 15
                parameters['custom_space_rules_rec'] = True
                parameters['cluster_width_after_rec_before_cluster'] = 50
                parameters['cluster_width_after_rec_before_rec'] = 70
                parameters['cluster_lines_after_rec_before_cluster'] = 0
                parameters['cluster_lines_after_rec_before_rec'] = 1
                parameters['asymmetric_lines_after_rec'] = True
                #parameters['text_total'] = 700
                """
                
                
                #Blank        
                parameters['line_length'] = 10
                parameters['line_offset'] = 25.0
                parameters['short_alignment'] = "center"
                parameters['guard_init'] = 2
                parameters['yellow_shade_blank'] = 0.98
                parameters['packet_size_blank'] = 29 #Not sure about this one, still needs testing
                
        elif(key == 4): #HP_Envy
        
                parameters['guard_end'] = True
        
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = True
                parameters['rec_width'] = 24#25#30#35.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['rec_width2'] = 100#95#90#60.0
                parameters['rec_left_margin2'] = 590 #550
                parameters['rec_line_length2'] = 13 #53

                parameters['yellow_shade_text'] = 0.98
                parameters['packet_size_text'] = 10#11
                parameters['text_guard_init'] = 0
                
                #Blank        
                parameters['line_length'] = 10
                parameters['line_offset'] = 27.0 #Could be adjusted to 21.0
                parameters['short_alignment'] = "left"
                parameters['guard_init'] = 1
                parameters['blank_total'] = 781
                parameters['yellow_shade_blank'] = 0.94
                parameters['packet_size_blank'] = 25
                
        elif(key == 5): #Test
                
                parameters['guard_end'] = True
        
                #Text
                parameters['use_rectangles'] = True
                parameters['use_only_rectangles'] = True
                parameters['rec_width'] = 33#35.0
                parameters['rec_left_margin'] = 9
                parameters['rec_line_length'] = 594
                parameters['rec_width2'] = 56#60.0
                parameters['rec_left_margin2'] = 590 #550
                parameters['rec_line_length2'] = 13 #53

                parameters['yellow_shade_text'] = 0.94
                parameters['packet_size_text'] = 10#11
                parameters['text_guard_init'] = 0
                
                #Blank        
                parameters['line_length'] = 10
                parameters['line_offset'] = 27.0 #Could be adjusted to 21.0
                parameters['short_alignment'] = "left"
                parameters['guard_init'] = 1
                parameters['blank_total'] = 781
                parameters['yellow_shade_blank'] = 0.94
                parameters['packet_size_blank'] = 25
               
        """ 
        Template for new printers, add your printer name in printer_name_list
       
        elif(key == 4): #Printer name
        
                parameters['guard_end'] = True
                
                #Text
                parameters['rec_width'] = 25.0
                parameters['cluster_width'] = 32.0
                parameters['cluster_lines'] = 10
                parameters['cluster_width_after_rec'] = 21.0
                parameters['cluster_lines_after_rec'] = 5
                parameters['cluster_left_margin'] = 9
                parameters['cluster_line_length'] = 594
                parameters['custom_space_rules_rec'] = False
                parameters['extra_cluster_line'] = False
                parameters['yellow_shade_text'] = 0.99
                parameters['packet_size_text'] = 15
        
                #Blank        
                parameters['line_length'] = 100
                parameters['line_offset'] = 25.0
                parameters['short_alignment'] = "center"
                parameters['guard_init'] = 0
                parameters['yellow_shade_blank'] = 0.99
                parameters['packet_size_blank'] = 30
        """
                
        return parameters
        
def get_parity_bit(pattern):
        parity = 0
        for i,bitidx in enumerate(pattern):
                parity += int(bitidx)
                
                if(i == len(pattern)-1):
                        parity %= 2

        return parity


textmod = False
raw_mode = False
info_bits = False
show_image = False
manchester = False
printer_name_list = ['Canon_MG2410', 'Epson_L4150', 'HP_Photosmart_D110', 'HP_Deskjet_1115', 'HP_Envy', 'Test'] #Add your printer name here

if len(sys.argv) < 2:
        print("Usage: testPrinter.py [OPTIONS] printer_name")
        print("Use this function to generate a bit pattern to inject into a PDF document. By default it prints non-text modulation, use -t otherwise. ")
        print("Current defined printers: ", printer_name_list)
        print("Possible options\n -p [arg] : use provided bit pattern\n -t : specify text modulation\n -s : line length sweep\n -S : offset sweep\n -i : display number of bits for specified printer\n -l : displays current defined printers\n -r : raw mode, used to specify bit patterns of any size without respecting established packet sizes\n -m : apply manchester encoding")
        exit()
        
if("-l" in sys.argv): #Special option
        print(printer_name_list)
        exit()


name = sys.argv[-1]

if(name not in printer_name_list):
        print("(ERROR) Printer has not been implemented. Current printer list:", printer_name_list)
        exit(1)


parameters = printer_parameters(printer_name_list.index(name))
parameters['name'] = name

total = 783.0 
"""
total is the upper vertical margin limit in the page, it depends on the size of the page, in this case it is for letter size
For a paper page in portrait mode, the x scale starts at the left edge and the y scale starts at the bottom of the page
It is important to check if the printer doesn't skip the first line or rectangle, for this modifying the total to be lower might help, or putting a "guard" line or rectangle first in the page that won't be part of the packet, just to make place for the next lines or rectangles.
"""

pattern = "1110001010111001001011010010111001001001" #Bit sequence example
preamble = "1010" #Preamble to all packets
max_length = 594 #Maximum line length with respect to the width of the page and its margins
overhead = 5

opts, args = getopt.getopt(sys.argv[1:], "SmsiItrp:")
for opt, arg in opts:
        if opt == '-t':
                textmod = True
        elif opt == '-p':
                pattern = str(arg)
        elif opt == '-r':
                raw_mode = True
        elif opt == '-m':
                manchester = True
                overhead = 3
        elif opt == '-i':
                info_bits = True
        elif opt == '-I':
                show_image = True
        elif opt == '-s':
                yellow_shade = parameters['yellow_shade_blank']
                print("q\n1.0 1.0", yellow_shade, "rg")
                SweepLength(parameters)
                print("f\nQ\n")
                exit()
        elif opt == '-S':
                yellow_shade = parameters['yellow_shade_blank']
                print("q\n1.0 1.0", yellow_shade, "rg")
                SweepOffset(parameters)
                print("f\nQ\n")
                exit()
                
                
if(info_bits):
        if(textmod):
                print(parameters['packet_size_text']-overhead)
        else:
                print(parameters['packet_size_blank']-overhead)
        exit()


if(textmod):
        
        yellow_shade = parameters['yellow_shade_text'] #this can go from 0 to 1.0, where 0 is completly yellow and 1.0 absence of yellow
        print("q\n1.0 1.0", yellow_shade, "rg") 
        
        if(not raw_mode): #modificar para manchester
                sz = parameters['packet_size_text']
                if(len(pattern) < sz-overhead):
                        print("(ERROR) Bit pattern should be greater than:", sz)
                        exit(1)
                
                parity = get_parity_bit(pattern[0:sz-overhead])
                packet = pattern[0:sz-overhead] + str(parity)
                
                if(manchester):
                        packet = to_manchester(packet)
                        
                text(parameters, preamble + packet)
        else:
                packet = pattern
                
                if(manchester):
                        packet = to_manchester(packet)
                text(parameters, packet)
else:
        
        yellow_shade = parameters['yellow_shade_blank']
        print("q\n1.0 1.0", yellow_shade, "rg")
        
        if(not raw_mode):
                sz = parameters['packet_size_blank']
                if(len(pattern) < sz-5):
                        print("(ERROR) Bit pattern should be greater than:", sz)
                        exit(1)
                parity = get_parity_bit(pattern[0:sz-5])
                blank(parameters, preamble + pattern[0:sz-5] + str(parity))
        else:
                blank(parameters, pattern)

print("f\nQ\n")




if(show_image):

    
    from os import environ
    import cv2

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

    cv2.imshow("Pattern", image_array)
    
    while True:
        key = cv2.waitKey(1)
        if key > 0:
            break
    cv2.destroyAllWindows()




