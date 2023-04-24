# Circles packing problem solver

There are set of circles that need to be packed in circle, placed in $(0, 0)$, in such way, that any of cirlces overlap and are inside main circle.

## Condition
$$
\begin{cases}
  (x_i-x_j)^2 + (y_i-y_j)^2 \ge (r_1+r_2)^2, &&\forall i,j \\
  x_i^2+y_i^2 + r_i \le R, &&\forall i \\
\end{cases}
$$

$$
R \to \min
$$

where $(x_i, y_i)$ coordinate of center of given circle, $r_i$ - radius (same for $j$), $R$ - radius of main circle.
