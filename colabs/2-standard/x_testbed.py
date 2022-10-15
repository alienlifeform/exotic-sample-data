setupDisplay()
display(HTML('<p>Either enter a telescope and target star, or type in the starchart image URL directly.'))


#### star image URL input ####

star_chart_url = widgets.Text(value='https://app.aavso.org/vsp/chart/X28247DI.png',
                         placeholder = 'https://app.aavso.org/vsp/chart/X28247DI.png',
                         description = 'AAVSO Star Chart image URL',
                         disabled    = False)

display(star_chart_url)

display(HTML('<p>or</p>'))

#### telescope dropdown ####

telescope = widgets.Dropdown(
    options=['Select a telescope', 'MicroObservatoryx', 'Exoplanet Watch .4 Meter'],
    value='Select a telescope',
    description='Telescope:',
)

def on_telescope_change(change):
  if change['type'] == 'change' and change['name'] == 'value':
    print("changed to %s" % change['new'])

telescope.observe(on_telescope_change)

display(telescope)

#### star target input ####

star_target = widgets.Text(value='Hat-P-32',
                         placeholder = 'Hat-P-32',
                         description = 'Target Star:',
                         disabled    = False)

display(star_target)


#### submit button ####

button = widgets.Button(description="Submit")

def on_telescope_submit_clicked(b):
  # Display the message within the output widget.
  if str(star_chart_url.value):
    if str(star_chart_url.value) == 'https://app.aavso.org/vsp/chart/X28247DI.png':
      display('X28247DI.png was selected ' + str(star_chart_url.value))
    else:
      display('X28247DI.png was not selected: ' + str(star_chart_url.value))
  elif str(telescope.value) and str(telescope.value):
    if str(telescope.value) == 'MicroObservatory':
      display('MicroObservatory was selected: ' + str(telescope.value))
    else:
      display('MicroObservatory was not selected: ' + str(telescope.value))
    
    if str(star_target.value) == 'Hat-P-32':
      display('Hat-P-32 was selected: ' + str(star_target.value))
    else:
      display('Hat-P-32 was not selected: ' + str(star_target.value))

button.on_click(on_telescope_submit_clicked)

display(button)

  