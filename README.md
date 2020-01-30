This algorithm aims to cut a polytope into n equally sized areas using voronoi partitions
A weighting function is used to shift the centroids in a way that
big areas tend to get smaller and the other way around

Run the algorithm:
1. Install requirements: `pip install -r requirements.txt`
2. Execute example: `python example`

Known bugs:
Sometimes the initial seeds are set outside of the polygon which stops the algorithm.
