function trig_sort = sort_triggers(cond, trig)


cond_sorted = sortrows(cond, 4);
min = cond_sorted(1,4);
for i = 1:length(cond)
    for j = 1:length(cond)
        if cond_sorted(i,4) == cond(j,4)
            trig_sort(i) = trig(j);
        end
    end
end


end

