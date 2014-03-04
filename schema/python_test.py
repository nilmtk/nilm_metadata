appliance = dict(
    on_power_threshold = 5,
    minimum_off_duration = 10,
    minimum_on_duration = 10
)

kitchen_appliance = appliance.copy()
kitchen_appliance.update({
    'category':'kitchen appliance',
    'distributions': {
        'room': 'kitchen:0.9'
    }
})
