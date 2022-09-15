#@title <font face="Helvetica" class="button" color='#702020'>&lt;- Click to download Planetary parameters for Hat-p-32 b</font> { vertical-output: true }

##############################################################

def fix_planetary_params (p_param_dict):
  for param in p_param_dict.keys():
    if param == "Target Star RA" or param == "Target Star Dec" or param == "Planet Name" or param == "Host Star Name" or param == "Argument of Periastron (deg)":
      continue
    val = p_param_dict[param]
    if val == 0.0 or np.isnan(float(val)):
      if param == "Orbital Eccentricity (0 if null)":
        continue
      if param == "Ratio of Planet to Stellar Radius (Rp/Rs)":
        p_param_dict[param] = 0.151
      if param == "Ratio of Planet to Stellar Radius (Rp/Rs) Uncertainty":
        p_param_dict[param] = 0.151
        if p_param_dict["Host Star Name"] == "Qatar-6":
          p_param_dict[param] = 0.01
      print(f"\nIn the planetary parameters from the NASA Exoplanet Archive, \n\"{param}\" is listed as {val}.\n\n**** This might make EXOTIC crash. ****\n\nIf the parameter is *not* changed below, please edit it\nin the inits file before running EXOTIC.\n")
  p_param_string = json.dumps(p_param_dict)

  planetary_params = "\"planetary_parameters\": {\n"
  num_done, num_total = 0, len(p_param_dict.keys())
  for key, value in p_param_dict.items():
    num_done += 1
    if key == "Target Star RA" or key == "Target Star Dec" or key == "Planet Name" or key == "Host Star Name":
      planetary_params = planetary_params + str(f"    \"{key}\": \"{value}\",\n")
    else:
      if num_done < num_total:
        planetary_params = planetary_params + str(f"    \"{key}\": {value},\n")
      else:
        planetary_params = planetary_params + str(f"    \"{key}\": {value}\n")
  planetary_params = planetary_params + "}"

  return(planetary_params)

##############################################################

importCustomStyles()

display(HTML('<p class="bookend">START: Download planetary parameters</p>'))


#target=input("Please enter the name of your exoplanet target: ")
target="Hat-p-32 b"
targ = NASAExoplanetArchive(planet=target)
target = targ.planet_info()[0]

display(HTML('<ul class="step3">'))
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
  display(HTML('<li class="step3">Loading NASA Exoplanet Archive planetary parameters for ' + target + ':</li><br />'))
  print(planetary_params)

  display(HTML('<li class="step3">Planetary parameters saved to memory</li>'))

display(HTML('</ul>'))

display(HTML('<p class="bookend">DONE: Download planetary parameters. <b>You may move on to the next step.</b></p>'))
