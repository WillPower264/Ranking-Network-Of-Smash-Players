import csv

desired_fields = ['winner_name', 'winner_global_id', 'loser_name', 'loser_global_id', 'winner_score', 'loser_score']
field_indices = {}
players = {}

# check if entry has valid data
def isValid(line):
    if line[field_indices['winner_global_id']] == '0': return False
    if line[field_indices['loser_global_id']] == '0': return False
    if line[field_indices['loser_score']] == '-1': return False
    if line[field_indices['loser_score']] == '': return False
    if line[field_indices['winner_score']] == '0': return False
    if line[field_indices['winner_score']] == '': return False
    return True

# save players and their ids
def savePlayers(line):
    winner_id = int(line[field_indices['winner_global_id']])
    loser_id = int(line[field_indices['loser_global_id']])
    winner_name = line[field_indices['winner_name']]
    loser_name = line[field_indices['loser_name']]
    
    # save winner
    if winner_id not in players:
        players[winner_id] = [winner_name]
    elif winner_name not in players[winner_id]:
        players[winner_id].append(winner_name)
    
    # save loser
    if loser_id not in players:
        players[loser_id] = [loser_name]
    elif loser_name not in players[loser_id]:
        players[loser_id].append(loser_name)
    
# read the data from file
with open('ultimate_sets.csv') as sets_data:
    with open('ultimate_sets_clean.csv', mode='w') as cleaned:
        # find where desired fields are in file
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
            savePlayers(line)
            for x in desired_fields:
                obj[x] = line[field_indices[x]]
            writer.writerow(obj)

# write player and id information
with open('ultimate_player_ids.csv', mode='w') as player_ids:
    # write header to file
    writer = csv.DictWriter(player_ids, fieldnames=['id', 'player'])
    writer.writeheader()
    for player_id in sorted(players.keys()):
        obj = {'id': player_id, 'player': ' [or] '.join(players[player_id])}
        writer.writerow(obj)

