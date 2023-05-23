# Circles packer (find local extreme)

There is a set of small circles that need to be packed in a circle, placed in $(0, 0)$, in such way that any of the circles would not overlap and would be inside the main circle. The program finds one of the local minima of the problem of packing circles into a circle of the minimum radius.

## Condition
$$
\begin{cases}
  (x_i-x_j)^2 + (y_i-y_j)^2 \ge (r_1+r_2)^2, &&\forall i,j (i \ne j) \\
  x_i^2+y_i^2 \le (R - r_i)^2, &&\forall i \\
\end{cases}
$$

$$
R \to \min
$$

where $(x_i, y_i)$ is the coordinate of the center of the given circle, $r_i$ - radius (same for $j$), $R$ - radius of the main circle.

## About used functions 

There are two main functions in the code: ```heuristic_packing``` and ```dichotomy_step_ralgo```. The first one finds the positions of the circles with some main radius (R), while the second one - improves the result. I strongly recommend using the second one in all cases because ```heuristic_packing``` does not always return "dense results", especially when the parameter ```number_of_iterations``` is small, so ```dichotomy_step_ralgo``` can improve it.

There are several params in ```heuristic_packing```:
* ```number_of_iterations``` - how many times solutions would be generated (return the best);
* ```number_of_flips``` - on each iteration several circles will be switched ```number_of_flips``` of times;
* ```radius_difference``` - would be switched only to circles whose radiuses' difference would be $\le$ ```radius_difference```.

There are several params in ```ralgb5``` that are used by ```dichotomy_step_ralgo```:
* ```x``` - start point vector (first n element is x coordinates of the circles, then n element is y coordinates of the circles, and the last element is  ```main_circle_radius```);
* ```alpha``` - space expansion coefficient;
* ```h``` - step size;
* ```q1``` - step reduction factor (recommended 1);
* ```epsx``` and ```epsg``` - precision for inside functions calculations (recommended to not change, otherwise, be aware that changing of this can cause inaccuracies);
* ```max_iterations``` - number of iterations for the algorithm (can be set as big numbers if you expect result improvements, but also affects time);
* ```radiuses``` - circles radiuses (be sure that passed radiuses match circles generated by ```heuristic_packing```).

> **Warning**
>
> If you manipulate with the params, be aware that it affects time of finding the answer and the result can not be 100% valid, so use ```is_valid_answer``` function.

## Example
### Without dichotomy step R-algo
<p align="center">
  <img src="./images/example.png">
</p>

### With dichotomy step R-algo
<p align="center">
  <img src="./images/example_with_ralgo.png">
</p>

## Used in the project:
* Python
* [Numpy](https://numpy.org/doc/stable/index.html)
* [Matplotlib](https://matplotlib.org/)
