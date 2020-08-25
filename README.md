```
How to run:
```
python runFits.py



```
What it does:
```
This framwork is used for W boson mass analysis:

- Calculate the <a href="https://www.codecogs.com/eqnedit.php?latex=\chi^{2}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\chi^{2}" title="\chi^{2}" /></a> value between data and simulation (templates), without correlation, defined as: <br />


          <a href="https://www.codecogs.com/eqnedit.php?latex=\chi^{2}=\sum_{i=1}^{N}&space;\frac{\left(n^{Data}_{i}-n^{Template}_{i}\right)^{2}}{(\sigma^{Data}_{n_{i}})^{2}&plus;(\sigma^{Template}_{n_{i}})^{2}}&space;," target="_blank"><img src="https://latex.codecogs.com/svg.latex?\chi^{2}=\sum_{i=1}^{N}&space;\frac{\left(n^{Data}_{i}-n^{Template}_{i}\right)^{2}}{(\sigma^{Data}_{n_{i}})^{2}&plus;(\sigma^{Template}_{n_{i}})^{2}}&space;," title="\chi^{2}=\sum_{i=1}^{N} \frac{\left(n^{Data}_{i}-n^{Template}_{i}\right)^{2}}{(\sigma^{Data}_{n_{i}})^{2}+(\sigma^{Template}_{n_{i}})^{2}} ," /></a>



- Calculate the <a href="https://www.codecogs.com/eqnedit.php?latex=\chi^{2}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\chi^{2}" title="\chi^{2}" /></a> value between the unfolded data and simulation (templates), with correlation, defined as: <br />

          <a href="https://www.codecogs.com/eqnedit.php?latex=\chi^{2}&space;=&space;(n^{Unf}_{Data}-n^{Unf}_{Template})^{T}&space;\cdot&space;(V_{Data}&space;&plus;&space;V_{Template})^{-1}&space;\cdot&space;(n^{Unf}_{Data}-n^{Unf}_{Template})," target="_blank"><img src="https://latex.codecogs.com/svg.latex?\chi^{2}&space;=&space;(n^{Unf}_{Data}-n^{Unf}_{Template})^{T}&space;\cdot&space;(V_{Data}&space;&plus;&space;V_{Template})^{-1}&space;\cdot&space;(n^{Unf}_{Data}-n^{Unf}_{Template})," title="\chi^{2} = (n^{Unf}_{Data}-n^{Unf}_{Template})^{T} \cdot (V_{Data} + V_{Template})^{-1} \cdot (n^{Unf}_{Data}-n^{Unf}_{Template})," /></a>

- Fit the <a href="https://www.codecogs.com/eqnedit.php?latex=\chi^{2}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\chi^{2}" title="\chi^{2}" /></a>  distribution: <br />
          <img width="514" alt="Screenshot 2020-08-25 at 11 21 42" src="https://user-images.githubusercontent.com/53044514/91157196-4d6a9d80-e6c5-11ea-9c7f-23d4f2741e33.png">


- Evaluate the statistical uncertaintiy on the measurement of W boson mass and the correponding correlation: <br />
      <img width="649" alt="Screenshot 2020-08-25 at 11 27 21" src="https://user-images.githubusercontent.com/53044514/91157704-f74a2a00-e6c5-11ea-9523-9a92defd5d4e.png">
          
- Calculate the total statistical uncertainty, taking into account the correlation, and making latex table: <br />
          <img width="703" alt="Screenshot 2020-08-25 at 11 29 32" src="https://user-images.githubusercontent.com/53044514/91157930-442e0080-e6c6-11ea-8f3a-abbe014c1147.png">
          
- Propagation of systematic uncertainties for the W boson measurement: <br />
          <img width="681" alt="Screenshot 2020-08-25 at 11 31 11" src="https://user-images.githubusercontent.com/53044514/91158120-7f303400-e6c6-11ea-8df6-6ed98801a53f.png">

