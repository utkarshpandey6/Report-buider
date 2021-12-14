

introduction_texts = [
    '''The trial was constituted with {number_of_entries} test entries and {number_of_checks} check varieties namely, {check_varieties} and conducted over {number_of_location} locations i.e., {locations}. Location wise results are discussed below and fibre yield data are presented in table [Your Table]'''
]

national = [
    '''{location}: {f_test} difference was observed among the entries, based on pooled analysis over locations. ''',
    '''{location}: Analysis of data at national level revealed {f_test} difference among the entries. ''',
    '''{location}: Based on pooled analysis over locations {f_test} difference among the entries was observed. '''
]

national_type2 = [
    '''{location}: In the year {year}, {f_test} difference was observed among the entries. ''',
    '''{location}: Analysis of data at national level in the year {year}, revealed {f_test} difference among the entries. '''
]

national_type2_without_location = [
    '''In the year {year}, {f_test} difference was observed among the entries. ''',
    '''Analysis of data at national level in the year {year}, revealed {f_test} difference among the entries. '''
]


location_texts = [
    '''{location}: The trial was sown on {sowing_date} at this centre and harvested on {harvesting_date} when the crop was {age} old. {f_test} difference was observed among entries. ''',
    '''{location}: Sowing of the trial was done on {sowing_date} and the crop was harvested after {age} on {harvesting_date}. {f_test} difference was observed among the entries. ''',
    '''{location}: The experiment was laid on {sowing_date} and harvested after {age} on {harvesting_date}. Differences among entries was {f_test}. '''
]

best_entries_text_when_better_than_checks = [
    '''Test entry {best_entry} recorded highest fibre yield {best_entry_value} followed by {other_best_entries} which were better than best check {best_checks}. ''',
    '''Test entry {best_entry} {best_entry_value} recorded highest fibre yield followed by {other_best_entries} over the best check {best_checks}. '''
]

best_entries_when_only_one_variety_is_better = [
    '''Test entry {best_entry} recorded high fibre yield {best_entry_value} than the best check {best_check} {best_check_value}. Followed by {other_best_entries}. '''
]

# best_entry = best_check
# best_entry_value = best_check_value
# other_entries = entries after best entry
best_entries_text_when_worse_than_checks = [
    '''Check variety {best_check} recorded high fibre yield {best_check_value} followed by {other_best_entries}. '''
]


mean_entries_start = [
    'Considering mean performance over years, ',
    'As per analysis of mean performance over years, ',
    'On the basis of pooled analysis over years, '
]

mean_entries_start_for_national_average = [
    '''Analysis of mean over locations and years mean (grand mean), ''',
    '''Considering pooled analysis over locations and years mean (grand mean), ''',
    '''Based on pooled analysis of data over locations and years (grand mean), '''
]

mean_entries_end = [
    '''{f_test} differences among entries was observed.''',
    '''Entries were {f_test}.''',
    '''Differences among entries was {f_test}.'''
]
