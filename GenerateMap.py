import random

def generate_event(track_length):
    
    #This is where the event happens
    point = random.uniform(0, track_length)
    #This decides the event type
    event_type = random.choice(['speed boost', 'obstacle'])
    #This determines the magnitude of the effect
    effect = random.uniform(1.0, 5.0)
    #This will determine whether time is taken away or added to your time
    time_impact = effect if event_type == 'obstacle' else -effect
    #Return dictionary
    return {
        'point': point,
        'type': event_type,
        'time_impact': time_impact
    }
def calculate_average_time(track_length, seconds_per_unit = 1.0):
    return seconds_per_unit * track_length

def generate_map(track_length, seconds_per_unit = 1.0, num_events = 10):
    events = [generate_event(track_length) for _ in range(num_events)]
    normal_time = calculate_average_time(track_length, seconds_per_unit)
    total_time_change = sum(event['time impact'] for event in events)
    final_time = normal_time + total_time_change
    
    return {
        'length': track_length,
        'events': events,
        'final_time': final_time
    }
    
    
    
    



