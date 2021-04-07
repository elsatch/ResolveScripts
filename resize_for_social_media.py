# This scripts takes a current timeline as input and creates two additional timelines in 9x16 and 1x1 for social media
# Tested on Davinci Resolve 17.1 under Windows 10 using original timeline resolution of 4k (3840x2160)

# Setting project name
projectName = "TestResize"

import imp
smodule = imp.load_dynamic('fusionscript', 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll')
resolve = smodule.scriptapp('Resolve')
pm = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
tl = proj.GetCurrentTimeline()

# Create Square Aspect Ratio timeline
tl.DuplicateTimeline("square")
squareTimeline = proj.GetTimelineByIndex(2)
squareTimeline.SetSetting("useCustomSettings","1")
squareTimeline.SetSetting("timelineResolutionHeight", "1080")
squareTimeline.SetSetting("timelineResolutionWidth", "1080")
squareTimeline.SetSetting("timelineInputResMismatchBehavior", "scaleToCrop")

tl.DuplicateTimeline("vertical")
verticalTimeline = proj.GetTimelineByIndex(3)
verticalTimeline.SetSetting("useCustomSettings","1")
verticalTimeline.SetSetting("timelineInputResMismatchBehavior", "scaleToCrop")
verticalTimeline.SetSetting("timelineResolutionHeight", "1920")
verticalTimeline.SetSetting("timelineResolutionWidth", "1080")

# Manual fastest way to deliver - use Cut Page - Quick Export - H.264 to get the correct resolution autodetected

# Let's automate rendering too!
# H.264 Master inherits the proper custom resolution from the timeline
proj.SetCurrentTimeline(proj.GetTimelineByIndex(2))
proj.LoadRenderPreset('H.264 Master')
# Resolve will ask for output location
# You can override it uncommenting next line
# proj.SetRenderSettings({'TargetDir': 'D:\DavinciOutuput'})
proj.SetRenderSettings({'CustomName': projectName + '-square'})
proj.AddRenderJob()

proj.SetCurrentTimeline(proj.GetTimelineByIndex(3))
proj.LoadRenderPreset('H.264 Master')
proj.SetRenderSettings({'CustomName': projectName + '-vertical'})
proj.AddRenderJob()
proj.StartRendering()

# Done!
