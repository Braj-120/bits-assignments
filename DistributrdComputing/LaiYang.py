def LaiYangSim(configuration):
    processes = configuration["processes"]
    total_number_of_seconds = configuration["total_number_of_seconds"]
    print(f"Process map is: {processes}\n")

    globalstate = {}
    for i in range(1, total_number_of_seconds + 1):
        globalstate[i] = processes

    print(f"Initial global state is: {globalstate}\n")

    i = 1
    newglobalstate = []
    for key in processes:
        newlist = []
        newlist.extend([i, processes[key], key])
        newglobalstate.append(newlist)
        i = i + 1

    #print(f"New global state: {newgstate}\n")

    messages = configuration["messages"]

    # Updating the global state
    for timer in range(2, total_number_of_seconds + 1):
        for p in list(processes):
            for message in messages:
                if message["sender"] == p and timer - 1 == message["sender_timestamp"]:
                    globalstate[timer][p] = globalstate[timer - 1][p] - message["transfer_value"]

                elif (message["receiver"] == p and timer - 1 == message["receiver_timestamp"]):
                    globalstate[timer][p] = globalstate[timer - 1][p] + message["transfer_value"]
                else:
                    globalstate[timer][p] = globalstate[timer - 1][p]
            # un comment this if you want to view the intermediate states
            # print(gstate[timer][p], timer, p) 
            newlist = []
            newlist.extend([timer, globalstate[timer][p], p])
            newglobalstate.append(newlist)

    print(f"Updated global state: {newglobalstate}\n")

    # Color marking scheme
    init_red = configuration["init_red"]
    red_processes = {}
    restred = 999
    for message in messages:
        if (message["sender"] == init_red[0] and message["sender_timestamp"] >= init_red[1]):
            message["color"] = "red"
            if message["receiver_timestamp"] < restred:
                restred = message["receiver_timestamp"]
                temp_key = message["receiver"]
                red_processes[temp_key] = restred
    for i in red_processes:
        for message in messages:
            if (message["sender"] == i and message["sender_timestamp"] >= red_processes[i]):
                message["color"] = "red"

    print(f"Updated messages are: {messages}\n")

    messages_red = list(filter(lambda x : x['color'] == 'red', messages))
    gsnapshots = []
    for red_message in messages_red:
        gsnapshot = {"red_times": []}
        for state in newglobalstate:
            if state[2] == red_message['sender'] and state[0] == red_message['sender_timestamp']:
                gsnapshot[state[2]] = state[1]
                gsnapshot["red_times"].append(state[0])
            elif state[2] == red_message['receiver'] and state[0] == red_message['receiver_timestamp']:
                gsnapshot[state[2]] = state[1]
                gsnapshot["red_times"].append(state[0])
        gsnapshots.append(gsnapshot)

    print(f"Snapshots taken when messages are red: {gsnapshots}\n")

    messages_white = list(filter(lambda x : x['color'] == 'white' , messages))
    for snapshot in gsnapshots:
        redtimes = snapshot['red_times']
        processes = list(snapshot.keys())[1:]
        CijSent = 0
        CijRecv = 0
        CjiRecv = 0
        CjiSent = 0

        for m in messages:
            if(m['sender'] == processes[0] and m['receiver'] == processes[1] and m['sender_timestamp'] < redtimes[0]):
                CijSent += m['transfer_value']
            if(m['sender'] == processes[0] and m['receiver'] == processes[1] and m['receiver_timestamp'] < redtimes[1]):
                CijRecv += m['transfer_value']
            if(m['sender'] == processes[1] and m['receiver'] == processes[0] and m['sender_timestamp'] < redtimes[1]):
                CjiSent += m['transfer_value']
            if(m['sender'] == processes[1] and m['receiver'] == processes[0] and m['receiver_timestamp'] < redtimes[0]):
                CjiRecv += m['transfer_value']
        
        final_value  = 0
        final_value += snapshot[processes[0]]
        print(f'Value of {processes[0]} ' + str(snapshot[processes[0]]))
        final_value += snapshot[processes[1]]
        print(f'Value of {processes[1]} ' + str(snapshot[processes[1]]))
        final_value += CijSent - CijRecv
        print(f'Value of messages CijSent - CijRecv ' + str(CijSent - CijRecv))
        final_value += CjiSent - CjiRecv
        print(f'Value of messages CjiSent - CjiRecv ' + str(CjiSent - CjiRecv))

        print(f"Value of {processes[0]} + Value of {processes[1]} + Value of messages in transit = {final_value}\n")

if __name__ == "__main__":
    #Use these to change the values of the processes and messages and tweek them as needed.
    config = {
        "processes": {"p1": 200, "p2": 800},
        "messages": [
            {
                "sender": "p1",
                "sender_timestamp": 1,
                "receiver": "p2",
                "receiver_timestamp": 2,
                "transfer_value": 20,
                "color": "white",
            },
            {
                "sender": "p1",
                "sender_timestamp": 2,
                "receiver": "p2",
                "receiver_timestamp": 6,
                "transfer_value": 30,
                "color": "white",
            },
            {
                "sender": "p1",
                "sender_timestamp": 3,
                "receiver": "p2",
                "receiver_timestamp": 5,
                "transfer_value": 10,
                "color": "white",
            },
            {
                "sender": "p2",
                "sender_timestamp": 4,
                "receiver": "p1",
                "receiver_timestamp": 6,
                "transfer_value": 30,
                "color": "white",
            },
            {
                "sender": "p2",
                "sender_timestamp": 7,
                "receiver": "p1",
                "receiver_timestamp": 8,
                "transfer_value": 20,
                "color": "white",
            },
        ],
        # Configure which process becomes red at which timestamp
        "init_red": ["p1", 3],
        "total_number_of_seconds": 9,  # No of intervals / rounds
    }

    LaiYangSim(config)
