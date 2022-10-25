#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Load telescope images</b></font>

##############################################################
%%capture step_capture --no-display
# Comment the above statement out to see debugging information
##############################################################

##############################################################
#
# NOTE TO EXOTIC USER:
#
#   • To hide this code, double-click the title above ("Load telescope images"),
#     or click the arrow to the left of the title.
#
#   • Editing this code will only affect your local instance. 
#     Reload to revert your changes.
#
##############################################################

setupDisplay()

# Prepare user for loading of images
display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container_2a"></ul>'))
appendStepToContainer('.step_container_2a','Ensuring images are loaded...</li>')
showProgress(1) 

def clean_input_filepath(p):
  p = re.sub('^/content', '', p)
  p = re.sub('^/drive/MyDrive', '', p)
  p = re.sub('^/', '', p)
  return(p)

######################################################


expandableSectionCustom('<u>+ EXOTIC Inline Help:</u> How to Upload your .FITS images into Google Drive in way that EXOTIC can use them','<u>- Close EXOTIC Inline Help</u>','''
  <p><b>How to upload your .FITS images into Google Drive in way that EXOTIC can use them:</b></p>
  <blockquote>e.g. EXOTIC/HatP32Dec202017/</blockquote>
  
  <ol style="line-height:135%">
  <li>In another window, <a href="https://drive.google.com/drive/my-drive" target="newGoogleDrive">go to Google Drive</a>.</li>
  <li><u>In Google Drive</u>, <i>if you don't already have an EXOTIC folder</i>, right click on "My Drive" (in the left nav) and click New Folder. Name the folder "EXOTIC".</li>
  <li>Click the arrow next to "My Drive" to see the subfolders and click "EXOTIC".</li>
  <li><u>On your computer</u>, put your .FITS files into a single folder uniquely named for your observation (e.g. "HatP32Dec202017").</li>
  <li>From your filesystem, drag this folder into Google Drive where it says "Drop files here".</li>
  </ol>

  <p>You will use this path (e.g. "EXOTIC/HatP32Dec202017") when loading your images into EXOTIC.</p>
''')


expandableSectionCustom('<u>+ EXOTIC Inline Help:</u> How to find your .FITS images','<u>- Close EXOTIC Inline Help</u>','''
  <p><b>How to find your .FITS images:</b></p>
  
  <ol style="line-height:135%">
  <li>In the left nav, click on the folder icon.</li>
  <li>Navigate to your images, likely in /drive/MyDrive/ or /content/drive/MyDrive/.</li>
  <li>Right-click on the folder with your .FITS images and click "Copy Path".</li>
  </ol>

  <p>You will use this path (e.g. "EXOTIC/HatP32Dec202017" or "/content/drive/MyDrive/EXOTIC/HatP32Dec202017") when loading your images into EXOTIC.</p>
''')

# Ask for inputs until we find .fits files
fits_files_found = False
while not fits_files_found:
  # Ask for inputs until we find ANY files
  uploaded_files_found = False
  #appendStepToContainer('.step_container_2a','A valid Google Drive filepath should not include /drive/MyDrive/')
  while not uploaded_files_found:
    input_filepath = input('Enter path to .FITS images in Google Drive (i.e. "EXOTIC/HatP32Dec202017"): ')
    #display(HTML(f'<p class="output">input_filepath={input_filepath}</p>'))
    cleaned_filepath = clean_input_filepath(input_filepath)
    #display(HTML(f'<p class="output">cleaned_filepath={cleaned_filepath}</p>'))
    if cleaned_filepath:
      verified_filepath = check_dir(os.path.join("/content/drive/My Drive/", cleaned_filepath))
      #display(HTML(f'<p class="output">verified_filepath={verified_filepath}</p>'))
      
      if verified_filepath:
        output_dir = verified_filepath + "_output/" 
        #display(HTML(f'<p class="output">output_dir={output_dir}</p>'))

        sorted_files = sorted(os.listdir(verified_filepath)); 
        #display(HTML(f'<p class="output">sortedFiles={sorted_files}</p>'))

        if sorted_files:
          uploaded_files_found = True # exit inner loop and continue
        else:
          display(HTML(f'<p class="error">Failed to find files at {verified_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))
      else:
        display(HTML(f'<p class="error">Failed to find a folder at /content/drive/My Drive/{cleaned_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))
    else:
      display(HTML(f'<p class="error">Filepath doesn\'t seem right: /content/drive/My Drive/{input_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))


  # Directory full of files found, look for .fits and inits.json
  uploaded_files = [f for f in sorted_files if os.path.isfile(os.path.join(verified_filepath, f))]
  fits_count, inits_count, first_image = 0, 0, ""


  # Identify .FITS and inits.json files in user-submitted folder
  inits = []    # array of paths to any inits files found in the directory
  for f in uploaded_files:
    # Look for .fits images and keep count
    if re.search(r"\.f[itz]+s?\.?g?z?$", f, re.IGNORECASE):
      # Determine the first image
      if first_image == "":
        first_image = os.path.join(verified_filepath, f)
      fits_count += 1
    # Look for inits.json file(s)
    if re.search(r"\.json$", f, re.IGNORECASE):
      inits.append(os.path.join(verified_filepath, f))
  
  inits_count = len(inits)
  display(HTML(f'<p class="output"><br />Found {fits_count} image files and {inits_count} initialization files in the directory.</p>'))

  # Determine if folder has enough .FITS folders to move forward
  if fits_count >= 19:
    fits_files_found = True # exit outer loop and continue

    # Make the output directory if it does not exist already.
    if not os.path.isdir(output_dir):    
      os.mkdir(output_dir)
      display(HTML(f'<p class="output">Creating output_dir at {output_dir}</p>'))
    output_dir_for_shell = output_dir.replace(" ", "\ ")
  else: 
    display(HTML(f'<p class="error">Failed to find a significant number of .FITS files at {verified_filepath}</p>'))

# Read configuration from inits.json, if available
if inits_count == 1:                 # one inits file exists
  # Deal with inits.json file
  inits_file_path = os.path.join(verified_filepath, inits[0])
  inits_file_exists = True
  #display(HTML(f'<p class="output">Got an inits.json file here: {inits_file_path}</p>'))
  with open(inits_file_path) as i_file:
    display(HTML(f'<p class="output">Loading coordinates and input/output directories from inits file</p>'))
    inits_data = i_file.read()
    d = json.loads(inits_data)
    targ_coords = d["user_info"]["Target Star X & Y Pixel"]
    comp_coords = d["user_info"]["Comparison Star(s) X & Y Pixel"]
    input_dir = d["user_info"]["Directory with FITS files"]
    if input_dir != verified_filepath:
      display(HTML(f'<p class="error">The directory with fits files should be {verified_filepath} but your inits file says {input_dir}.</p>'))
      display(HTML('<p class="output">This may or may not cause problems.  Just letting you know.<p>'))
    display(HTML(f'<p class="output">Coordinates from your inits file:\ntarget: {targ_coords}\ncomps: {comp_coords}<p>'))
    output_dir = d["user_info"]["Directory to Save Plots"]
else:
  display(HTML(f'<p class="output">No valid inits.json file was found, we\'ll create it in the next step.<p>'))
  inits_file_exists = False

showProgress(1)
display(HTML('<p class="bookend">DONE: Loading telescope images</p>'))


######################################################

# Load planetary params if inits.json file does not yet exist
if not inits_file_exists:

  display(HTML('<p class="bookend">START: Download planetary parameters</p>'))

  planetary_params = ""
  while not planetary_params:
    target_is_valid = False
    while not target_is_valid:
      target=input('Please enter the name of your exoplanet target (i.e. "HAT-P-32 b"): ')
      if target != "":
        target_is_valid = True
      else:
        display(HTML(f'<p class="error">Exoplanet target may not be blank.</p>'))
        starchart_image_url_is_valid = False

    display(HTML('<br /><ul class="step_container_2b"></ul>'))
    appendStepToContainer('.step_container_2b','Searching NASA Exoplanet Archive for "' + target + '"...')

    targ = NASAExoplanetArchive(planet=target)
    #appendStepToContainer('.step_container_2','Loading planet info')
    target = targ.planet_info()[0]
    
    if not targ.resolve_name():
      appendStepToContainer('.step_container_2b','''
      Sorry, we can\'t find your target in the Exoplanet Archive.  Unfortunately, this
      isn't going to work until we can find it. Please try
      different formats for your target name, until the target is located.
      Looking it up in the NASA Exoplanet Archive at https://exoplanetarchive.ipac.caltech.edu/
      might help you know where to put the spaces and hyphens and such.
      ''')
      appendStepToContainer('.step_container_2b','''
      If your target is a candidate, you may need to create your own inits.json file and
      add it to the folder with your FITS images.
      ''')
    else:
      appendStepToContainer('.step_container_2b','Found target "' + target + '" in the NASA Exoplanet Archive')
      p_param_string = targ.planet_info(fancy=True)
      planetary_params = '"planetary_parameters": ' + p_param_string
      p_param_dict = json.loads(p_param_string)
      planetary_params = fix_planetary_params(p_param_dict)
      appendStepToContainer('.step_container_2b','Loading NASA Exoplanet Archive planetary parameters for ' + target)
      display(HTML(f'<pre class="output">{planetary_params}</pre>'))


  expandableSectionCustom('<u>+ EXOTIC Inline Help:</u> How to get an AAVSO Observer code','<u>- Close EXOTIC Inline Help</u>','''
    <p><b>How to get an AAVSO Observer code:</b></p>
    Follow the instructions at the <a href="https://www.aavso.org/new-observers#:~:text=If%20you%20do%20not%20yet,for%20%22Request%20an%20obscode%22." target="_blank">AAVSO "New Observers" page</a>.
  ''')

  # Prompt for AAVSO code
  aavso_obs_code = input("Enter your AAVSO Observer code or press enter to skip: ")
  if aavso_obs_code:
    sec_obs_code = input("Enter a secondary AAVSO Observer code or press enter to skip: ")
  else: 
    sec_obs_code = ""

  display(HTML('<p class="bookend">DONE: Download planetary parameters. <b>You may move on to the next step.</b></p>'))

else: 

  display(HTML('<p class="bookend">DONE: Inits.json file exists. <b>You may move on to step 4.</b></p>'))