import csv

desired_fields = ['winner_name', 'winner_global_id', 'loser_name', 'loser_global_id', 'winner_score', 'loser_score']
field_indices = {}

def isValid(line):
    if line[field_indices['winner_global_id']] == '0': return False
    if line[field_indices['loser_global_id']] == '0': return False
    if line[field_indices['loser_score']] == '-1': return False
    if line[field_indices['loser_score']] == '': return False
    if line[field_indices['winner_score']] == '0': return False
    if line[field_indices['winner_score']] == '': return False

    return True

with open('ultimate_sets_clean.csv', mode='w') as cleaned:
    with open('ultimate_sets.csv') as sets_data:
        data_reader = csv.reader(sets_data)
        headers = data_reader.next()
        for i, header in enumerate(headers):
            if header in desired_fields:
                field_indices[header] = i

        # write header to file
        writer = csv.DictWriter(cleaned, fieldnames=desired_fields)
        writer.writeheader()

        obj = {}
        # process each line
        for line in data_reader:
            if not isValid(line): continue
            for x in desired_fields:
                obj[x] = line[field_indices[x]]
            writer.writerow(obj)
