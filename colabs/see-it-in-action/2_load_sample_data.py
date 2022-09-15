#@title <font face="Helvetica" class="button" color='#702020'>&lt;- Click to load sample data for Hat-p-32 b</font>
#%%capture step_capture --no-display

importCustomStyles()

display(HTML('<p class="bookend">START: Loading sample data</p>'))

display(HTML('<ul class="step2">'))
display(HTML('<li class="step2">Ensuring sample data is loaded'))


#
# Delete existing sample data by changing to `rebuild = "true"`
#
rebuild = "false"  
if rebuild == "true":
  if os.path.isdir("/content/EXOTIC/exotic-in-action"):
    %rm -rf /content/EXOTIC/exotic-in-action
    print("'Rebuild' flag is 'true'... Removing old data at /content/EXOTIC/exotic-in-action")

#
# Download sample files if necessary
#
sample_data_source = "https://github.com/rzellem/EXOTIC_sampledata.git"
sample_data_target_parent = "/content/EXOTIC/exotic-in-action"
sample_data_target_folder = "/content/EXOTIC/exotic-in-action/sample-data"
sample_data_target_child = "/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017"
if os.path.isdir(sample_data_target_child):
  display(HTML('<li class="step2">Skipping... Sample data already loaded for Hat-p-32 b</li>'))

else:
  display(HTML('Downloading data from ' + sample_data_source + '</li>'))
  !git clone {sample_data_source} {sample_data_target_folder}
  #!git clone {https://github.com/rzellem/EXOTIC_sampledata.git /content/EXOTIC/exotic-in-action/sample-data
  #!git clone https://github.com/alienlifeform/exotic.git /content/EXOTIC/exotic-in-action
  display(HTML('<li class="step2">Sample data successfully loaded for Hat-p-32 b</li>'))

#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017
numfiles = !ls {sample_data_target_child} | grep -ci FITS

print('You have ' + str(numfiles[0]) + ' telescope image (.FITS) files</li>')

display(HTML('</ul>'))
display(HTML('<p class="bookend">DONE: Loading sample data. <b>You may move on to the next step.</b></p>'))

# to mount the user's Google Drive... the original way
#drive.mount('/content/drive', force_remount=True)
