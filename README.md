# ECE143-individual-project
Analysis of Ad-Hoc Communications Network

You have been asked to help with planning an ad-hoc communications network over a large
rectangular region. Each individual tower can monitor a rectangular subsection of a specific
width and height. The main problem is that none of the individual towers can provide
coverage for the entire region of interest. Communications towers are unreliable and are put
up independently and at random. You have no control over where or how big a tower’s
footprint is placed. Importantly, due to technical issues such as cross-talk, no individual
rectangular subsection can have multiple towers providing coverage for it. That is, there can
be no overlap between any pair of rectangular subsections provided by the two respective
towers. In any case, the desire is to maximize the coverage area of any available
communications tower.

The order of when the towers come online is important. Once a tower has acquired its
rectangular section, no subsequent tower can overlap that section. You may assume the
following for this problem:

● All rectangular sections have integer-based corners.

● All rectangular sections must be contained in the overall rectangular footprint.

● The height and width of each rectangular section is sampled from a uniform
distribution.

● Positions of the windows are also determined by uniform random distribution.

● All footprints must be rectangles (not general polygons).

● When a new tower comes online, if its coverage rectangle intersects the pre-existing
composite footprint, then that new tower’s coverage is trimmed such that its
maximum remaining coverage area is retained (see sequential diagram below).


Write a detailed Jupyter notebook that implements a solution to this problem such that the
user can supply the following overall size of desired coverage footprint and then determine
the following:

● Given an overall desired coverage footprint and a sequence of n communications
towers, what is the resulting resolved coverage?

● What is the total area of coverage relative to the desired total coverage area of the
original footprint? That is, are there any gaps in coverage?

● On average, how many communications towers are required before full coverage is
obtained?


Submission instructions

1. The deadline for the individual project is 3 weeks from the date of release. It is due
on 05/22/2018 at 4 A.M. This is a hard deadline, no extensions will be given out.

2. Please use a github repository to send in your submissions. Use a git tag to mark your
final submission. The latest tagged version before the deadline would be considered as
your final submission.

3. Your submission should consist of a one Jupyter notebook that can run out of the box,
along with any associated helper files. It should contain all reproducible code, written
using all the good practices suggested. You can either use modular or OOPs paradigm.

4. The notebook should be more than just a script. It should contain thoughtful
discussions on the problem, trade-offs, limitations details, and analysis. It should also
contain good visualizations and some examples of your results.
