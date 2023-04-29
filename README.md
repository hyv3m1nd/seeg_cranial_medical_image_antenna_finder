# seeg_cranial_medical_image_antenna_finder

## The scenario  
An epileptic patient gets a Stereoelectroencephalography (SEEG) to identify the part of the brain that causes the seizures.  
As part of this procedure, multiple antennae are inserted into the brain to measure brain activity.  
The brain activities are then mapped to the location in the brain where the corresponding antenna was at.  
The problem is that the location of the antennae can only be determined through CT scan, and the antennae cause lots of artifact, making it difficult to accurately determine the antennae positions with respect to the brain.  

## The solution  
The antennae always shines the brightest on a CT scan (~3000 hounsfield units). The artifacts come next, at around 1000-2000 hounsfield units. The rest of the anatomical structures follow.  
An exponential scale is therefore applied to the entire CT scan, bringing the artifacts to 1/100 the brightness of the actual antennae.  
A transposition matrix is generated from static bone structures to map the original antennae CT scan (where the bones are visible) to an MRI scan, where the brain shows up clearest.  
The transposition matrix is then applied to the exponentially rescared antennae scan to map the antennae onto the MRI.  
Another rescaling is applied to the antennae scan to bring the maximum brightness to 100, so it is in the same scale as the MRI scan. This step is required because when a commercial medical image viewers opens up the image, the default brightness range is set using the current image's statistics. This means that if the antennae are at ~3000 hounsfield units while the rest of the brain are at ~100, the entire skull shows up as black.  
After combining the antennae and the brain MRI, precise 3D models of the antennae, with labeled beads (which are segments that measure brain activities), are superimposed onto the image using the tips and entry points of each antennae as guides.  
A trained radiologist reads the bead labels off the combined image to determine the precise locations where each measurement occurs.  
A proprietary software analyzes the results.  

## Special thanks
To Scott Collins for bringing the issues to me, handling all the image processing and transpositions, and discussing potential solutions with me,  
To Dr. Wael Asaad, for explaining the problem, SEEG, and related analyses and for vetting our solution, 
To many medical students and residents who identified cases we prototyped with.

This code was written in 2021.
