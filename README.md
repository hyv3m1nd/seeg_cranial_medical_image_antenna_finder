# seeg_cranial_medical_image_antenna_finder

## The scenario  
An epileptic patient gets a Stereoelectroencephalography (SEEG) to identify the part of the brain that causes the seizures.  
As part of this procedure, multiple antennae are inserted into the brain to measure brain activity.  
The brain activities are then mapped to the location in the brain where the corresponding antenna was at.  
The problem is that the location of the antennae can only be determined through CT scan, and the antennae cause lots of artifact, making it difficult to accurately determine the antennae positions with respect to the brain.  

## The solution  
### Isolating the antennae from the artifacts  
We observed that the antennae always shine brightest on a CT scan (~3000 hounsfield units). The artifacts come next, at around 1000-2000 hounsfield units. The rest of the anatomical structures follow.  
To isolate the antennae, an exponential scale is applied to the entire CT scan, bringing the artifacts to 1/100 the brightness of the actual antennae. All anatomical structures get scaled down to black.  
### Combining isolated antennae with anatomical structures  
The original CT scan is preserved and exists in the same coordinate system as the isolated antennae scan. We also have a MRI scan, which offers the clearest view of the brain but has a different coordinate system. The task is to generate a transposition matrix that transposes the CT scans onto the MRI scan.  
This matrix is generated by mapping static bone structures on the original CT scan (where the bones are visible) onto an MRI scan. It is then applied to the isolated antennae scan to map the antennae onto the MRI.  
The next task is to ensure both the anatomical structure and the antennae remain visible on a commercial medical image viewer.  
We cannot merge them directly, since we observed that:  
(1) A typical commercial viewer sets each image's default brightness scale based on the image's hounsfield unit statistics.  
(2) The antennae remain at ~3000 hounsfield units.  
(3) A typical MRI's brain structure is at ~100.  
Therefore, the brain would show up as black if the antennae scan and the MRI scan are merged directly.  
Our workaround is applying a linear scale to the antennae scan to bring the maximum brightness to 100 before the scans are merged.  
### Generating precise antennae labels  
The antennae have beads that measure brain activity.  
We made precise 3D models of each antenna model based on vendor dimension charts, with labeled beads.  
After combining the antennae and the brain MRI, precise 3D models corresponding to each used antenna model are superimposed onto the image using the tips and entry points of each antenna as guides.  
A trained radiologist reads the bead labels off the combined image to determine the precise locations where each measurement occurs.  
A proprietary software analyzes the results.  

## Special thanks
To **Scott Collins**, radiology technologist, for mentoring me on medical image processing and interpretation, bringing this issue to my attention, discussing potential solutions, providing the coding platform, developing the 3D models, handling all the image processing and transpositions, and producing the sample image,  
To **Wael Asaad**, M.D., for explaining the problem, SEEG procedure, and related analyses and for vetting our solution,  
To many **medical students** and **residents** who identified the cases we prototyped with.  
  
This code was written in 2021. It has been put in practice on a weekly basis.  
