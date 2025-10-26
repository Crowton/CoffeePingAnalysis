u = 12pt;

prologues:=2;

path p;
p = (.5u,0)..(u,.5u)..(.5u,u)..(0,.5u)..cycle;


beginfig(1);
  pickup pencircle scaled 2pt;
  draw p;
  draw (.5u,.5u)--(1.2u,1.2u) cutbefore p;
  draw (1.2u,1.2u)--(.8u,1.2u);
  draw (1.2u,1.2u)--(1.2u,.8u);
endfig;

beginfig(2);
  pickup pencircle scaled 2pt;
  draw p;
  draw (.5u,0)--(.5u,-.5u);
  draw (.25u,-.25u)--(.75u,-.25u);
endfig;

end.