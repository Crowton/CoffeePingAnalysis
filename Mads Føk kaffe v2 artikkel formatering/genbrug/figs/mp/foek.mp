beginfig(1)

def M(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-35.2mm)..tension 3.2..
  ($+2.0mm,@-27.0mm)..tension 3.2..
  ($+4.2mm,@-27.0mm)..tension 3.2..
  ($+4.2mm,@-28.8mm)..tension 3.2..
  ($+5.5mm,@-30.0mm)..tension 3.2..
  ($+7.6mm,@-26.8mm)..tension 3.2..
  ($+9.9mm,@-26.8mm)..tension 3.2..
  ($+10.4mm,@-35.5mm)..tension 3.2..
  ($+7.0mm,@-35.2mm)..tension 3.2..
  ($+8.0mm,@-30.4mm)..tension 3.2..
  ($+6.5mm,@-31.8mm)..tension 3.2..
  ($+5.2mm,@-31.2mm)..tension 3.2..
  ($+4.6mm,@-35.2mm)..tension 3.2..
  cycle;
enddef;

def A(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-35.2mm)..tension 3.2..
  ($+1.6mm,@-27.2mm)..tension 3.2..
  ($+4.0mm,@-27.4mm)..tension 3.2..
  ($+6.6mm,@-34.6mm)..tension 3.2..
  ($+3.6mm,@-35.0mm)..tension 3.2..
  ($+3.8mm,@-33.0mm)..tension 3.2..
  ($+2.4mm,@-33.2mm)..tension 3.2..
  ($+1.6mm,@-35.0mm)..tension 3.2..
  cycle;

  unfill
  ($+3.0mm,@-32.0mm)--
  ($+3.2mm,@-30.4mm)--
  ($+4.0mm,@-31.4mm)--
  cycle;

enddef;

def D(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-35.0mm)..tension 3.2..
  ($+0.2mm,@-32.8mm)..tension 3.2..
  ($+0.8mm,@-32.8mm)..tension 3.2..
  ($+1.8mm,@-29.4mm)..tension 3.2..
  ($-0.2mm,@-29.2mm)..
  ($+2.8mm,@-27.2mm)..
  ($+5.0mm,@-27.8mm)..
  ($+8.0mm,@-31.8mm)..
  ($+3.0mm,@-35.4mm)..tension 3.2..
  cycle;

  unfill
  ($+3.6mm,@-33.0mm)--
  ($+4.2mm,@-30.2mm)..
  ($+5.0mm,@-31.8mm)..
  cycle;

enddef;

def S(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-32.8mm)..tension 3.2..
  ($+1.2mm,@-32.2mm)..tension 3.2..
  ($+3.4mm,@-33.4mm)..
  ($+5.0mm,@-33.0mm)..tension 3.2..
  ($+3.0mm,@-31.8mm)..
  ($+0.4mm,@-30.0mm)..tension 3.2..
  ($+2.2mm,@-27.2mm)..tension 3.2..
  ($+5.4mm,@-26.6mm)..tension 3.2..
  ($+7.4mm,@-29.0mm)..tension 3.2..
  ($+4.4mm,@-30.2mm)..tension 3.2..
  ($+4.4mm,@-29.4mm)..tension 3.2..
  ($+3.0mm,@-30.0mm)..
  ($+3.6mm,@-31.2mm)..{down}
  ($+8.0mm,@-33.4mm){down}..{left}
  ($+3.0mm,@-35.4mm)..
  cycle;
enddef;

def F(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-35.8mm)..tension 3.2..
  ($+1.2mm,@-31.2mm)..tension 3.2..
  ($-2.0mm,@-30.2mm)..tension 3.2..
  ($+0.0mm,@-29.4mm)..tension 3.2..
  ($+7.0mm,@-27.6mm)..tension 3.2..
  ($+7.0mm,@-29.4mm)..tension 3.2..
  ($+4.0mm,@-29.8mm)..tension 3.2..
  ($+4.0mm,@-31.2mm)..tension 3.2..
  ($+6.4mm,@-30.6mm)..tension 3.2..
  ($+6.6mm,@-31.4mm)..tension 3.2..
  ($+4.0mm,@-32.0mm)..tension 3.2..
  ($+3.6mm,@-35.8mm)..tension 3.2..
  cycle;
enddef;

def OE(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+1.0mm,@-37.6mm)..tension 3.2..
  ($+4.4mm,@-32.0mm)..tension 3.2..
  ($+8.0mm,@-26.8mm)..tension 3.2..
  ($+10.0mm,@-27.4mm)..tension 3.2..
  ($+8.8mm,@-29.8mm)..
  ($+8.4mm,@-33.0mm)..
  ($+5.6mm,@-34.4mm)..tension 3.2..
  ($+4.2mm,@-37.8mm)..tension 3.2..
  cycle;

  fill
  ($+2.8mm,@-34.6mm)..tension 3.2..
  ($+0.4mm,@-34.4mm)..tension 3.2..
  ($-0.6mm,@-33.6mm)..tension 3.2..
  ($+0.4mm,@-30.8mm)..tension 3.2..
  ($+5.0mm,@-28.2mm)..tension 3.2..
  ($+8.0mm,@-29.2mm)..tension 3.2..
  ($+7.0mm,@-31.0mm)..tension 3.2..
  ($+4.4mm,@-30.0mm)..
  ($+2.4mm,@-31.4mm)..
  ($+3.0mm,@-33.4mm)..tension 3.2..
  ($+5.0mm,@-33.4mm)..tension 3.2..
  cycle;
enddef;

def K(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-35.8mm)..tension 3.2..
  ($+0.8mm,@-33.2mm)..tension 3.2..
  ($+1.0mm,@-28.0mm)..tension 3.2..
  ($+2.8mm,@-27.9mm)..tension 3.2..
  ($+3.2mm,@-30.6mm)..tension 3.2..
  ($+6.6mm,@-28.6mm)..tension 3.2..
  ($+6.8mm,@-27.2mm)..tension 3.2..
  ($+9.6mm,@-28.4mm)..tension 3.2..
  ($+6.6mm,@-30.8mm)..tension 3.2..
  ($+9.0mm,@-34.2mm)..tension 3.2..
  ($+5.6mm,@-36.4mm)..tension 3.2..
  ($+5.0mm,@-32.4mm)..tension 3.2..
  ($+3.0mm,@-32.4mm)..tension 3.2..
  ($+3.4mm,@-36.0mm)..tension 3.2..
  cycle;
enddef;

def plif(expr $) =
  numeric @;
  @ = 65.0mm;
  fill
  ($+0.0mm,@-29.0mm){up}..
  ($-0.1mm,@-28mm)..
  ($-0.7mm,@-26.2mm)..
  ($+0.9mm,@-26mm){right}..
  ($+1.3mm,@-26.4mm){dir -60}..
  cycle;
enddef;

%M(24.2mm);
%A(35.4mm);
%D(41.8mm);
%S(48.0mm);
F(59.0mm);
OE(64.6mm);
K(73.4mm);

endfig
end.
