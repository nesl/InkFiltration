function [bits, limits] = peaks2bits(type, class, parameter, peaks_pre, peaks)

bits = [];
limits = [];

locs_diff = diff(peaks);

if(type == "Blank")
    
    idx = 1;
    preidx = 1;
    sum_locs = 0;

    for n=1:length(locs_diff)

        sum_locs = sum_locs + locs_diff(n);
        if preidx <= length(peaks_pre) && sum_locs > peaks_pre(preidx) %Determines packet boundaries
           limits(preidx) = idx;
           preidx = preidx + 1;
        end

       if class == 1 %This series of conditions check for special circumstances
           if locs_diff(n) > 25 && locs_diff(n) < 26
               locs_diff(n+1) = locs_diff(n+1) + locs_diff(n);
               continue;
           end
           
       elseif class == 2

           if locs_diff(n) > 48 && locs_diff(n) < 53
               bits(idx) = 1;
               idx = idx + 1;
               bits(idx) = 0;
               idx = idx + 1;
               continue;
           elseif locs_diff(n) >= 45 && locs_diff(n) < 48
               bits(idx) = 0;
               idx = idx + 1;
               continue;
           elseif locs_diff(n) >= 21 && locs_diff(n) < 22
               locs_diff(n+1) = locs_diff(n+1) + locs_diff(n);
               continue;
           end
           
       elseif class == 3
           
           if locs_diff(n) >= 55
               bits(idx) = 0;
               idx = idx + 1;
               bits(idx) = 1;
               idx = idx + 1;
               continue;
           end
       end
       
       if locs_diff(n)  < parameter.limitL2 && locs_diff(n) >= parameter.limitL1 
           bits(idx) = 0;
       elseif locs_diff(n) < parameter.limitH2 && locs_diff(n) >= parameter.limitH1
           bits(idx) = 1;
       elseif locs_diff(n) < parameter.limitI
           continue;
       else
           bits(idx) = -1;
       end
       idx = idx + 1;
    end
    
elseif(type == "Text")
    temp_sum = 0;
    counter = 0;
    num_lo_pot = 0;
    num_hi_pot = 0;
    flag41 = 0;

    idx = 1;
    num_hi = 0;
    num_lo = 0;
    first_hi = 1;
    preidx = 1;
    last_hi = 0;

    for n=1:length(locs_diff)

    
       if preidx <= length(peaks_pre) && peaks(n) > peaks_pre(preidx) %Determines packet boundaries and adds some extra bits
           bits = add_bit(bits, 1);
           bits = add_bit(bits, -1);
           bits = add_bit(bits, 1);
           preidx = preidx + 1;
       end
        
        

        if class == 2
           if locs_diff(n) >= 43 && locs_diff(n) < 45 || locs_diff(n) >= 31 && locs_diff(n) < 35
               locs_diff(n) = parameter.limitL1;
           elseif n+1 <= length(locs_diff) && ((locs_diff(n) >= 21 && locs_diff(n) < 22) || ((locs_diff(n) >= 10 && locs_diff(n) < parameter.limitL1) && (locs_diff(n+1) >= 10 && locs_diff(n+1) < parameter.limitL1)))
               locs_diff(n+1) = locs_diff(n+1) + locs_diff(n);
               continue;
           end
           %{
        elseif class == 3
            if locs_diff(n) >= 10 && locs_diff(n) < 30
                locs_diff(n) = parameter.limitL1;
            end
           %}
        elseif class == 4

           if(locs_diff(n) < 19 && locs_diff(n) > 6)               
               counter = counter + 1;
               temp_sum = temp_sum + locs_diff(n);
                
               if counter == 2 && locs_diff(n) >= 13
                   locs_diff(n) = temp_sum;
                   temp_sum = 0;
                   counter = 0;
               elseif counter == 3
                   if locs_diff(n) >= 13
                       counter = 1;
                       locs_diff(n-1) = temp_sum - locs_diff(n);
                       temp_sum = locs_diff(n);
                   else
                       locs_diff(n) = temp_sum;
                       temp_sum = 0;
                       counter = 0;
                   end
               else
                   locs_diff(n) = 0;
               end

           elseif(locs_diff(n) <= 3)
               continue
           elseif(n -1 > 0 && locs_diff(n) <= 6 && locs_diff(n) > 3)
               locs_diff(n-1) = locs_diff(n-1) + locs_diff(n);
           else
               locs_diff(n) = locs_diff(n) + temp_sum;
               temp_sum = 0;
               counter = 0;
           end
        
       end

       if locs_diff(n) >= parameter.limitH1 && locs_diff(n) < parameter.limitH2
           
           if class == 4 || class == 3
               if class == 4
                   if (class == 4 && locs_diff(n) >= 36)
                       if num_lo > 0 && num_hi_pot == 0
                           num_hi_pot = 1;
                           continue
                       end
                   end
                   if num_lo_pot
                        bits = add_bit(bits, 0);
                        num_lo_pot = 0;
                   end
                   if num_hi_pot
                       num_hi = num_hi + 1;
                       num_hi_pot = 0;
                   end
           
                elseif class == 3 
                   
                   if num_lo > 0 && num_hi_pot == 0
                       num_hi_pot = 1;
                       continue
                   end
                   if num_hi_pot
                       num_hi = num_hi + 1;
                      
                       num_lo = num_lo + 1;

                       if ~mod(num_lo,2)
                           bits = add_bit(bits, 0);
                       end
                       num_lo = 0;
                      
                       num_hi_pot = 0;
                   end
                   
                   if locs_diff(n) < 41
                       flag41 = flag41 + 1;
                       if flag41 == 1
                           continue
                       else
                           if flag41 == 2
                               num_hi = num_hi +1;
                               if ~mod(num_hi,2)
                                    bits = add_bit(bits, 1);
                                    first_hi = 0;
                               end
                           end
                       end
                   else
                       if flag41 == 1
                           bits = add_bit(bits, 0);
                       end
                       flag41 = 0;
                   end
               end
               
               num_lo = 0;
               num_hi = num_hi +1;
               if ~mod(num_hi,2)
                    bits = add_bit(bits, 1);
                    first_hi = 0;
               end
              
               
           else
           
               num_lo = 0;
               num_hi = num_hi +1;
               if num_hi >= parameter.hi_limit && first_hi
                    bits = add_bit(bits, 1);
                    first_hi = 0;
               end
               last_hi = 1;
           end

       elseif locs_diff(n) >= parameter.limitL1 && locs_diff(n) < parameter.limitL2
           
           if class == 4
               if num_hi > 0
                   num_lo_pot = 1;
               else
                   num_lo_pot = 0;
               end

               num_hi_pot = 0;
           elseif class == 3
               num_lo_pot = 0;
               if num_hi_pot
                   num_lo = num_lo + 1;
                   if ~mod(num_lo,2)
                       bits = add_bit(bits, 0);
                   end
               end
               if flag41 == 1
                   num_hi = num_hi +1;
                   if ~mod(num_hi,2)
                        bits = add_bit(bits, 1);
                   end
               end
               flag41 = 0;
               
           end
           num_hi_pot = 0;
           first_hi = 1;
           num_lo = num_lo + 1;

           %{
           if class == 3
               if locs_diff(n) > 100
                    num_lo = num_lo + 1;
               end

               if last_hi
                   if num_lo > 2
                       bits(idx) = 0;
                       idx = idx + 1;
                       num_lo = num_lo -2;
                       last_hi = 0;
                   end
               else
                   if ~mod(num_lo,2)
                       bits(idx) = 0;
                       idx = idx + 1;
                   end
               end
           %}
           
           if ~mod(num_lo,2)
                bits = add_bit(bits, 0);
           end
           

           num_hi = 0;
       end
    end
end

end

function bits = add_bit(bits, type)
persistent idx;

if isempty(bits)
    idx = 1;
end

bits(idx) = type;
idx = idx + 1;

end