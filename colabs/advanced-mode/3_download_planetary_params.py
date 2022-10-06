#@title <font face="Helvetica" class="button" color='#702020'>&lt;- Click to download Planetary data for HAT-P-32 b</font> { vertical-output: true }

##############################################################

importCustomStyles()

display(HTML('<p class="bookend">START: Download planetary parameters</p>'))

display(HTML('<ul class="step3">'))
display(HTML('<li class="step3">Connecting with NASA Exoplanet Archive</li>'))

#target=input("Please enter the name of your exoplanet target: ")
target="HAT-P-32 b"
targ = NASAExoplanetArchive(planet=target)
target = targ.planet_info()[0]

display(HTML('<li class="step3">Found target ' + target + ' in the NASA Exoplanet Archive</li>'))

planetary_params = ""
if not targ.resolve_name():
  print("Sorry, can't find your target in the Exoplanet Archive.  Unfortunately, this")
  print("isn't going to work until I can find it.  Please re-run this cell, trying")
  print("different formats for your target name, until the target is located.")
  print("Looking it up in the NASA Exoplanet Archive at https://exoplanetarchive.ipac.caltech.edu/")
  print("might help you know where to put the spaces and hyphens and such.")
else:
  p_param_string = targ.planet_info(fancy=True)
  planetary_params = "\"planetary_parameters\": "+p_param_string
  p_param_dict = json.loads(p_param_string)
  planetary_params = fix_planetary_params(p_param_dict)
  display(HTML('<li class="step3">Loading NASA Exoplanet Archive planetary parameters for ' + target + '</li><br />'))
  print(planetary_params)

  display(HTML('<li class="step3">Planetary parameters saved to memory</li>'))

display(HTML('</ul>'))

display(HTML('<p class="bookend">DONE: Download planetary parameters. <b>You may move on to the next step.</b></p>'))
