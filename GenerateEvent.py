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
    
    